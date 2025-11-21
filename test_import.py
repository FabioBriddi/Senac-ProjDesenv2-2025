"""
Script para testar importação de CSV de Analytics
Salvar na RAIZ do projeto
"""
from pathlib import Path
import pandas as pd
from src.csv_processors.analytics_processor import AnalyticsCSVProcessor
from src.database.models import init_database

def create_sample_csv():
    """Cria um CSV de exemplo baseado na estrutura fornecida"""
    
    # Dados de exemplo
    data = {
        'DSP': ['Spotify', 'Apple Music', 'YouTube Music', 'Amazon Music', 
                'Deezer', 'Tidal', 'SoundCloud', 'YouTube'],
        '8 set': [1234, 567, 890, 345, 123, 45, 678, 2345],
        '9 set': [1456, 678, 923, 456, 145, 67, 789, 2567],
        '10 set': [1678, 789, 1045, 567, 167, 89, 890, 2789],
        '11 set': [1890, 890, 1123, 678, 189, 123, 934, 3012],
        '12 set': [2012, 923, 1234, 789, 234, 145, 1012, 3234],
        '13 set': [2234, 1045, 1345, 890, 256, 167, 1123, 3456],
        '14 set': [2456, 1123, 1456, 934, 289, 189, 1234, 3678]
    }
    
    df = pd.DataFrame(data)
    
    # Salva o arquivo
    filepath = Path("data/uploads/sample_analytics.csv")
    filepath.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(filepath, index=False)
    
    print(f"✅ CSV de exemplo criado: {filepath}")
    return filepath

def main():
    """Função principal de teste"""
    
    print("=" * 50)
    print("TESTE DE IMPORTAÇÃO DE CSV DE ANALYTICS")
    print("=" * 50)
    
    # Inicializa banco de dados
    print("\n1. Inicializando banco de dados...")
    artist = init_database()
    print(f"   ✅ Banco inicializado")
    
    # Cria CSV de exemplo
    print("\n2. Criando CSV de exemplo...")
    csv_file = create_sample_csv()
    
    # Mostra preview do CSV
    print("\n3. Preview do CSV:")
    df = pd.read_csv(csv_file)
    print(df.to_string())
    
    # Processa o CSV
    print("\n4. Processando CSV...")
    processor = AnalyticsCSVProcessor()
    result = processor.process_analytics_csv(str(csv_file), "AllMark")
    
    if result['status'] == 'success':
        print("\n✅ PROCESSAMENTO CONCLUÍDO COM SUCESSO!")
        print(f"   - Arquivo: {result['file']}")
        print(f"   - Artista: {result['artist']}")
        print(f"   - Registros processados: {result['rows_processed']}")
        print(f"   - Sucesso: {result['rows_success']}")
        print(f"   - Erros: {result['rows_error']}")
        print(f"   - DSPs: {', '.join(result['dsps'])}")
        print(f"   - Período: {result['date_range']}")
        print(f"   - Total de Streams: {result['total_streams']:,}")
        
        # Obtém resumo
        print("\n5. Resumo dos Analytics:")
        summary = processor.get_analytics_summary("AllMark")
        
        if 'error' not in summary:
            print(f"   - Total de Streams: {summary['total_streams']:,}")
            print(f"   - Receita Estimada: ${summary['total_revenue']:,.2f}")
            print(f"   - Total de Registros: {summary['total_records']}")
            
            print("\n   Breakdown por DSP:")
            for dsp, data in summary['dsps'].items():
                print(f"   - {dsp}:")
                print(f"     • Streams: {data['streams']:,}")
                print(f"     • Receita: ${data['revenue']:,.2f}")
                print(f"     • Dias: {data['days']}")
    else:
        print(f"\n❌ ERRO: {result.get('message', 'Erro desconhecido')}")
    
    print("\n" + "=" * 50)
    print("TESTE CONCLUÍDO")
    print("=" * 50)

if __name__ == "__main__":
    main()