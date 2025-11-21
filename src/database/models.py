"""
Modelos do banco de dados para o sistema
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Date, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime
import os

Base = declarative_base()

# Configuração do banco de dados
DATABASE_URL = "sqlite:///data/music_distribution.db"
engine = create_engine(DATABASE_URL, echo=False)


class Artist(Base):
    """Modelo para artistas"""
    __tablename__ = 'artists'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False, unique=True)
    country = Column(String(100))
    genre = Column(String(100))
    biography = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    tracks = relationship("Track", back_populates="artist")
    albums = relationship("Album", back_populates="artist")
    analytics = relationship("Analytics", back_populates="artist")


class Album(Base):
    """Modelo para álbuns"""
    __tablename__ = 'albums'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.id'))
    upc = Column(String(50), unique=True)
    release_date = Column(Date)
    label = Column(String(200))
    genre = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    artist = relationship("Artist", back_populates="albums")
    tracks = relationship("Track", back_populates="album")


class Track(Base):
    """Modelo para faixas/músicas"""
    __tablename__ = 'tracks'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    artist_id = Column(Integer, ForeignKey('artists.id'))
    album_id = Column(Integer, ForeignKey('albums.id'))
    isrc = Column(String(50), unique=True)
    duration = Column(Integer)  # em segundos
    genre = Column(String(100))
    release_date = Column(Date)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relacionamentos
    artist = relationship("Artist", back_populates="tracks")
    album = relationship("Album", back_populates="tracks")
    analytics = relationship("Analytics", back_populates="track")


class Analytics(Base):
    """Modelo para analytics de streams"""
    __tablename__ = 'analytics'
    
    id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.id'))
    track_id = Column(Integer, ForeignKey('tracks.id'), nullable=True)
    dsp = Column(String(100), nullable=False)  # Digital Service Provider
    date = Column(Date, nullable=False)
    streams = Column(Integer, default=0)
    revenue = Column(Float, default=0.0)
    territory = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relacionamentos
    artist = relationship("Artist", back_populates="analytics")
    track = relationship("Track", back_populates="analytics")


class CSVImport(Base):
    """Modelo para controlar importações de CSV"""
    __tablename__ = 'csv_imports'
    
    id = Column(Integer, primary_key=True)
    filename = Column(String(255), nullable=False)
    distributor = Column(String(50))
    import_type = Column(String(50))  # analytics, tracks, albums, etc
    rows_processed = Column(Integer, default=0)
    rows_success = Column(Integer, default=0)
    rows_error = Column(Integer, default=0)
    status = Column(String(20))  # pending, processing, completed, error
    error_message = Column(Text)
    imported_at = Column(DateTime, default=datetime.utcnow)
    imported_by = Column(String(100))


# Criar tabelas
Base.metadata.create_all(engine)

# Criar sessão
Session = sessionmaker(bind=engine)


def get_session():
    """Retorna uma nova sessão do banco de dados"""
    return Session()


def init_database():
    """Inicializa o banco de dados com dados padrão"""
    session = get_session()
    
    try:
        # Verifica se já existe o artista AllMark
        artist = session.query(Artist).filter_by(name="AllMark").first()
        if not artist:
            artist = Artist(
                name="AllMark",
                country="Brasil",
                genre="Pop/Rock",
                biography="Artista brasileiro de música pop/rock"
            )
            session.add(artist)
            session.commit()
            print(f"Artista AllMark criado com ID: {artist.id}")
        else:
            print(f"Artista AllMark já existe com ID: {artist.id}")
            
        return artist
        
    except Exception as e:
        session.rollback()
        print(f"Erro ao inicializar banco: {e}")
        raise
    finally:
        session.close()


if __name__ == "__main__":
    # Teste de criação do banco
    init_database()
    print("Banco de dados criado com sucesso!")