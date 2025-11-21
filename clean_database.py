"""
Script para limpar/gerenciar o banco de dados
Salvar na RAIZ do projeto
"""
from src.database.models import get_session, Artist, Album, Track, Analytics, CSVImport, init_database
from datetime import datetime
import sys

def show_current_data():
    """Mostra os dados atuais no banco"""
    session = get_session()
    
    print("\n" + "="*50)
    print("DADOS ATUAIS NO BANCO")
    print("="*50)
    
    # Artistas
    artists = session.query(Artist).all()
    print(f"\n📤 ARTISTAS ({len(artists)} total):")
    for artist in artists:
        analytics_count = session.query(Analytics).filter_by(artist_id=artist.id).count()
        print(f"   ID {artist.id}: {artist.name} - {analytics_count} registros de analytics")
    
    # Analytics
    total_analytics = session.query(Analytics).count()
    print(f"\n📊 ANALYTICS: {total_analytics} registros totais")
    
    # Por DSP
    from sqlalchemy import func
    dsp_stats = session.query(
        Analytics.dsp, 
        func.count(Analytics.id).label('count'),
        func.sum(Analytics.streams).label('total_streams')
    ).group_by(Analytics.dsp).all()
    
    if dsp_stats:
        print("\n   Por DSP:")
        for dsp, count, streams in dsp_stats:
            print(f"   - {dsp}: {count} registros, {streams:,} streams")
    
    # Importações
    imports = session.query(CSVImport).all()
    print(f"\n📁 IMPORTAÇÕES: {len(imports)} arquivos processados")
    for imp in imports:
        print(f"   - {imp.filename} ({imp.status}) - {imp.rows_success} registros")
    
    session.close()

def clean_all_data():
    """Limpa TODOS os dados do banco"""
    session = get_session()
    
    try:
        # Confirma antes de deletar
        print("\n⚠️  ATENÇÃO: Isso vai DELETAR TODOS os dados do banco!")
        confirm = input("Digite 'SIM' para confirmar: ")
        
        if confirm.upper() != 'SIM':
            print("❌ Operação cancelada")
            return
        
        # Deleta todos os registros
        deleted_analytics = session.query(Analytics).delete()
        deleted_tracks = session.query(Track).delete()
        deleted_albums = session.query(Album).delete()
        deleted_artists = session.query(Artist).delete()
        deleted_imports = session.query(CSVImport).delete()
        
        session.commit()
        
        print("\n✅ Banco limpo com sucesso!")
        print(f"   - {deleted_analytics} registros de analytics deletados")
        print(f"   - {deleted_tracks} tracks deletadas")
        print(f"   - {deleted_albums} álbuns deletados")
        print(f"   - {deleted_artists} artistas deletados")
        print(f"   - {deleted_imports} importações deletadas")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao limpar banco: {e}")
    finally:
        session.close()

def clean_sample_data_only():
    """Limpa apenas dados de exemplo/teste"""
    session = get_session()
    
    try:
        # Deleta apenas registros do arquivo de exemplo
        sample_import = session.query(CSVImport).filter(
            CSVImport.filename.like('%sample%')
        ).first()
        
        if sample_import:
            print("\n🧹 Limpando dados de exemplo...")
            
            # Se quiser deletar apenas analytics de teste, pode filtrar por data ou outro critério
            # Por exemplo, deletar analytics com valores específicos de teste
            deleted = 0
            
            # Deleta importações de exemplo
            deleted_imports = session.query(CSVImport).filter(
                CSVImport.filename.like('%sample%')
            ).delete()
            
            session.commit()
            print(f"✅ {deleted_imports} importações de exemplo removidas")
        else:
            print("ℹ️ Nenhum dado de exemplo encontrado")
            
    except Exception as e:
        session.rollback()
        print(f"❌ Erro: {e}")
    finally:
        session.close()

def clean_duplicates():
    """Remove registros duplicados de analytics"""
    session = get_session()
    
    try:
        # Encontra e remove duplicatas (mantém apenas o mais recente)
        from sqlalchemy import func
        
        # Agrupa por artist_id, dsp, date e encontra duplicatas
        duplicates = session.query(
            Analytics.artist_id,
            Analytics.dsp,
            Analytics.date,
            func.count(Analytics.id).label('count'),
            func.max(Analytics.id).label('keep_id')
        ).group_by(
            Analytics.artist_id,
            Analytics.dsp,
            Analytics.date
        ).having(func.count(Analytics.id) > 1).all()
        
        if duplicates:
            print(f"\n🔍 Encontradas {len(duplicates)} combinações com duplicatas")
            
            deleted_count = 0
            for artist_id, dsp, date, count, keep_id in duplicates:
                # Deleta todos exceto o mais recente
                deleted = session.query(Analytics).filter(
                    Analytics.artist_id == artist_id,
                    Analytics.dsp == dsp,
                    Analytics.date == date,
                    Analytics.id != keep_id
                ).delete()
                deleted_count += deleted
            
            session.commit()
            print(f"✅ {deleted_count} registros duplicados removidos")
        else:
            print("✅ Nenhuma duplicata encontrada")
            
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao remover duplicatas: {e}")
    finally:
        session.close()

def reset_to_clean_state():
    """Reseta o banco para um estado limpo com apenas o artista AllMark"""
    session = get_session()
    
    try:
        print("\n🔄 Resetando banco de dados...")
        
        # Limpa tudo
        session.query(Analytics).delete()
        session.query(Track).delete()
        session.query(Album).delete()
        session.query(Artist).delete()
        session.query(CSVImport).delete()
        
        # Recria apenas o artista AllMark
        artist = Artist(
            name="AllMark",
            country="Brasil",
            genre="Pop/Rock",
            biography="Artista brasileiro de música pop/rock"
        )
        session.add(artist)
        session.commit()
        
        print("✅ Banco resetado com sucesso!")
        print(f"   - Artista '{artist.name}' criado (ID: {artist.id})")
        print("   - Pronto para novas importações")
        
    except Exception as e:
        session.rollback()
        print(f"❌ Erro ao resetar: {e}")
    finally:
        session.close()

def main():
    """Menu principal"""
    while True:
        print("\n" + "="*50)
        print("GERENCIADOR DE BANCO DE DADOS")
        print("="*50)
        print("\n1. Ver dados atuais")
        print("2. Limpar TODOS os dados")
        print("3. Limpar apenas dados de exemplo")
        print("4. Remover registros duplicados")
        print("5. Resetar banco (mantém apenas AllMark)")
        print("0. Sair")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == "1":
            show_current_data()
        elif choice == "2":
            clean_all_data()
        elif choice == "3":
            clean_sample_data_only()
        elif choice == "4":
            clean_duplicates()
        elif choice == "5":
            reset_to_clean_state()
        elif choice == "0":
            print("\n👋 Até logo!")
            break
        else:
            print("❌ Opção inválida")

if __name__ == "__main__":
    # Se passar argumento direto, executa sem menu
    if len(sys.argv) > 1:
        if sys.argv[1] == "--reset":
            reset_to_clean_state()
        elif sys.argv[1] == "--clean":
            clean_all_data()
        elif sys.argv[1] == "--show":
            show_current_data()
        elif sys.argv[1] == "--duplicates":
            clean_duplicates()
    else:
        main()