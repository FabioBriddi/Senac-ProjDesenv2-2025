"""
Processador para CSVs de Analytics/Streams das DSPs
"""
import pandas as pd
import numpy as np
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import logging
import sys
import os

# Adiciona o diretório pai ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.database.models import get_session, Artist, Analytics, CSVImport

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AnalyticsCSVProcessor:
    """Processador especializado para CSVs de Analytics/Streams"""
    
    def __init__(self):
        self.session = get_session()
        self.upload_dir = Path("data/uploads")
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Lista de DSPs conhecidas
        self.known_dsps = [
            'Spotify', 'Apple Music', 'YouTube Music', 'Amazon Music',
            'Deezer', 'Tidal', 'SoundCloud', 'Pandora', 'YouTube',
            'Facebook', 'Instagram', 'TikTok', 'Snapchat'
        ]
    
    def process_analytics_csv(self, filepath: str, artist_name: str = "AllMark") -> Dict:
        """
        Processa CSV de analytics/streams
        
        Args:
            filepath: Caminho do arquivo CSV
            artist_name: Nome do artista (padrão: AllMark)
            
        Returns:
            Dicionário com resultado do processamento
        """
        logger.info(f"Processando arquivo: {filepath}")
        
        # Registra importação
        import_record = CSVImport(
            filename=Path(filepath).name,
            distributor="general",
            import_type="analytics",
            status="processing"
        )
        self.session.add(import_record)
        self.session.commit()
        
        try:
            # Lê o CSV
            df = pd.read_csv(filepath, encoding='utf-8')
            logger.info(f"CSV carregado: {len(df)} linhas, {len(df.columns)} colunas")
            logger.info(f"Colunas encontradas: {df.columns.tolist()}")
            
            # Obtém ou cria o artista
            artist = self.session.query(Artist).filter_by(name=artist_name).first()
            if not artist:
                artist = Artist(name=artist_name)
                self.session.add(artist)
                self.session.commit()
                logger.info(f"Artista '{artist_name}' criado")
            
            # Identifica colunas de data (formato: "8 set", "9 set", etc)
            date_columns = [col for col in df.columns if col != 'DSP']
            logger.info(f"Colunas de data identificadas: {date_columns}")
            
            # Processa dados
            rows_success = 0
            rows_error = 0
            
            for _, row in df.iterrows():
                dsp = row['DSP']
                
                for date_col in date_columns:
                    try:
                        # Parse da data (formato: "DD mes")
                        date_obj = self._parse_date(date_col, 2024)  # Assume ano atual
                        
                        # Valor de streams
                        streams = row[date_col]
                        if pd.isna(streams) or streams == 0:
                            continue
                        
                        # Verifica se já existe registro para esta data/DSP
                        existing = self.session.query(Analytics).filter_by(
                            artist_id=artist.id,
                            dsp=dsp,
                            date=date_obj
                        ).first()
                        
                        if existing:
                            # Atualiza streams
                            existing.streams = int(streams)
                            logger.debug(f"Atualizado: {dsp} - {date_obj} - {streams} streams")
                        else:
                            # Cria novo registro
                            analytics = Analytics(
                                artist_id=artist.id,
                                dsp=dsp,
                                date=date_obj,
                                streams=int(streams),
                                revenue=self._estimate_revenue(dsp, int(streams)),
                                territory="Global"
                            )
                            self.session.add(analytics)
                            logger.debug(f"Adicionado: {dsp} - {date_obj} - {streams} streams")
                        
                        rows_success += 1
                        
                    except Exception as e:
                        logger.error(f"Erro ao processar {dsp} - {date_col}: {e}")
                        rows_error += 1
            
            # Commit das alterações
            self.session.commit()
            
            # Atualiza registro de importação
            import_record.status = "completed"
            import_record.rows_processed = len(df) * len(date_columns)
            import_record.rows_success = rows_success
            import_record.rows_error = rows_error
            self.session.commit()
            
            # Estatísticas
            result = {
                'status': 'success',
                'file': Path(filepath).name,
                'artist': artist_name,
                'rows_processed': len(df) * len(date_columns),
                'rows_success': rows_success,
                'rows_error': rows_error,
                'dsps': df['DSP'].unique().tolist(),
                'date_range': f"{date_columns[0]} - {date_columns[-1]}",
                'total_streams': df[date_columns].sum().sum()
            }
            
            logger.info(f"Processamento concluído: {result}")
            return result
            
        except Exception as e:
            logger.error(f"Erro no processamento: {e}")
            
            # Atualiza registro de importação com erro
            import_record.status = "error"
            import_record.error_message = str(e)
            self.session.commit()
            
            return {
                'status': 'error',
                'message': str(e)
            }
        finally:
            self.session.close()
    
    def _parse_date(self, date_str: str, year: int = 2024) -> date:
        """
        Converte string de data para objeto date
        
        Args:
            date_str: String no formato "DD mes" (ex: "8 set")
            year: Ano a ser usado
            
        Returns:
            Objeto date
        """
        # Mapeamento de meses em português
        month_map = {
            'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4, 'mai': 5, 'jun': 6,
            'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12
        }
        
        parts = date_str.strip().split()
        if len(parts) == 2:
            day = int(parts[0])
            month = month_map.get(parts[1].lower(), 9)  # Default setembro
            return date(year, month, day)
        
        # Fallback para data atual
        return date.today()
    
    def _estimate_revenue(self, dsp: str, streams: int) -> float:
        """
        Estima receita baseada no DSP e número de streams
        
        Args:
            dsp: Nome do DSP
            streams: Número de streams
            
        Returns:
            Receita estimada em USD
        """
        # Valores médios por stream (em USD)
        # Fonte: Estimativas da indústria
        revenue_per_stream = {
            'Spotify': 0.003,
            'Apple Music': 0.007,
            'YouTube Music': 0.002,
            'YouTube': 0.001,
            'Amazon Music': 0.004,
            'Deezer': 0.006,
            'Tidal': 0.012,
            'SoundCloud': 0.003,
            'Pandora': 0.002,
            'Facebook': 0.004,
            'Instagram': 0.003,
            'TikTok': 0.003,
            'Snapchat': 0.002
        }
        
        rate = revenue_per_stream.get(dsp, 0.003)  # Default
        return round(streams * rate, 2)
    
    def get_analytics_summary(self, artist_name: str = "AllMark") -> Dict:
        """
        Obtém resumo dos analytics de um artista
        
        Args:
            artist_name: Nome do artista
            
        Returns:
            Dicionário com resumo
        """
        try:
            artist = self.session.query(Artist).filter_by(name=artist_name).first()
            if not artist:
                return {'error': f'Artista {artist_name} não encontrado'}
            
            analytics = self.session.query(Analytics).filter_by(artist_id=artist.id).all()
            
            if not analytics:
                return {
                    'artist': artist_name,
                    'total_streams': 0,
                    'total_revenue': 0,
                    'dsps': []
                }
            
            # Agrupa por DSP
            dsp_summary = {}
            for record in analytics:
                if record.dsp not in dsp_summary:
                    dsp_summary[record.dsp] = {
                        'streams': 0,
                        'revenue': 0,
                        'days': 0
                    }
                dsp_summary[record.dsp]['streams'] += record.streams
                dsp_summary[record.dsp]['revenue'] += record.revenue
                dsp_summary[record.dsp]['days'] += 1
            
            return {
                'artist': artist_name,
                'total_streams': sum(r.streams for r in analytics),
                'total_revenue': round(sum(r.revenue for r in analytics), 2),
                'total_records': len(analytics),
                'dsps': dsp_summary,
                'date_range': {
                    'start': min(r.date for r in analytics).isoformat() if analytics else None,
                    'end': max(r.date for r in analytics).isoformat() if analytics else None
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao obter resumo: {e}")
            return {'error': str(e)}
        finally:
            self.session.close()


# Teste direto do processador
if __name__ == "__main__":
    processor = AnalyticsCSVProcessor()
    
    # Teste com arquivo de exemplo
    test_file = "data/uploads/AnalyticsStreamsbyDsp776805455820250916.csv"
    
    if Path(test_file).exists():
        result = processor.process_analytics_csv(test_file, "AllMark")
        print("Resultado do processamento:")
        print(result)
        
        # Obtém resumo
        summary = processor.get_analytics_summary("AllMark")
        print("\nResumo dos Analytics:")
        print(summary)
    else:
        print(f"Arquivo {test_file} não encontrado")