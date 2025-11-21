"""
Configurações centralizadas do sistema
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import json

# Carrega variáveis de ambiente
load_dotenv()

# Diretórios base
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
UPLOAD_DIR = DATA_DIR / "uploads"
CSV_DIR = DATA_DIR / "csv"
CONFIG_FILE = BASE_DIR / "config.json"

# Criar diretórios se não existirem
for dir_path in [DATA_DIR, UPLOAD_DIR, CSV_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# Criar subdiretórios para cada distribuidora
for dist in ["fuga", "orchard", "vydia"]:
    (UPLOAD_DIR / dist).mkdir(exist_ok=True)
    (CSV_DIR / dist).mkdir(exist_ok=True)


class Config:
    """Classe de configuração do sistema"""
    
    def __init__(self):
        self.config_file = CONFIG_FILE
        self.config = self.load_config()
    
    def load_config(self) -> dict:
        """Carrega configurações do arquivo ou cria padrão"""
        if self.config_file.exists():
            with open(self.config_file, 'r') as f:
                return json.load(f)
        else:
            # Configurações padrão
            default_config = {
                "app": {
                    "name": "Music Distribution API Manager",
                    "version": "1.0.0",
                    "debug": os.getenv("DEBUG", "False").lower() == "true"
                },
                "fuga": {
                    "enabled": False,
                    "endpoint": "https://api.fugamusic.com",
                    "api_key": os.getenv("FUGA_API_KEY", ""),
                    "api_secret": os.getenv("FUGA_API_SECRET", ""),
                    "rate_limit": 60,
                    "timeout": 30,
                    "auto_sync": True
                },
                "orchard": {
                    "enabled": False,
                    "endpoint": "https://api.theorchard.com",
                    "client_id": os.getenv("ORCHARD_CLIENT_ID", ""),
                    "client_secret": os.getenv("ORCHARD_CLIENT_SECRET", ""),
                    "rate_limit": 100,
                    "timeout": 30,
                    "auto_sync": True
                },
                "vydia": {
                    "enabled": False,
                    "endpoint": "https://api.vydia.com",
                    "api_token": os.getenv("VYDIA_API_TOKEN", ""),
                    "account_id": os.getenv("VYDIA_ACCOUNT_ID", ""),
                    "rate_limit": 30,
                    "timeout": 30,
                    "auto_sync": False
                },
                "database": {
                    "type": "sqlite",
                    "path": str(DATA_DIR / "music_distribution.db")
                },
                "sync": {
                    "interval_hours": 6,
                    "batch_size": 100,
                    "retry_attempts": 3,
                    "retry_delay": 60
                },
                "export": {
                    "formats": ["csv", "excel", "json"],
                    "default_format": "csv",
                    "include_metadata": True
                }
            }
            
            # Salva configuração padrão
            self.save_config(default_config)
            return default_config
    
    def save_config(self, config: dict = None):
        """Salva configurações no arquivo"""
        if config is None:
            config = self.config
        
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    def get(self, key: str, default=None):
        """Obtém valor de configuração usando notação de ponto"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default
        
        return value
    
    def set(self, key: str, value):
        """Define valor de configuração usando notação de ponto"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save_config()
    
    def get_api_config(self, distributor: str) -> dict:
        """Obtém configuração específica de uma distribuidora"""
        return self.config.get(distributor.lower(), {})
    
    def update_api_config(self, distributor: str, config: dict):
        """Atualiza configuração de uma distribuidora"""
        dist = distributor.lower()
        if dist in self.config:
            self.config[dist].update(config)
            self.save_config()
    
    def is_api_configured(self, distributor: str) -> bool:
        """Verifica se uma API está configurada"""
        config = self.get_api_config(distributor)
        
        if distributor.lower() == "fuga":
            return bool(config.get("api_key") and config.get("api_secret"))
        elif distributor.lower() == "orchard":
            return bool(config.get("client_id") and config.get("client_secret"))
        elif distributor.lower() == "vydia":
            return bool(config.get("api_token") and config.get("account_id"))
        
        return False
    
    def get_enabled_apis(self) -> list:
        """Retorna lista de APIs habilitadas"""
        enabled = []
        for api in ["fuga", "orchard", "vydia"]:
            if self.config.get(api, {}).get("enabled", False):
                enabled.append(api)
        return enabled
    
    def get_sync_status(self) -> dict:
        """Retorna status de sincronização"""
        status = {}
        for api in ["fuga", "orchard", "vydia"]:
            api_config = self.config.get(api, {})
            status[api] = {
                "enabled": api_config.get("enabled", False),
                "configured": self.is_api_configured(api),
                "auto_sync": api_config.get("auto_sync", False)
            }
        return status


# Instância global de configuração
config = Config()

# Constantes úteis
APP_NAME = config.get("app.name")
APP_VERSION = config.get("app.version")
DEBUG_MODE = config.get("app.debug")

# Mapeamento de distribuidoras
DISTRIBUTOR_NAMES = {
    "fuga": "Fuga Music",
    "orchard": "The Orchard",
    "vydia": "Vydia"
}

# Formatos de arquivo suportados
SUPPORTED_AUDIO_FORMATS = [".mp3", ".wav", ".flac", ".m4a", ".aac"]
SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".gif", ".bmp"]
SUPPORTED_DATA_FORMATS = [".csv", ".xlsx", ".xls", ".json"]

# Colunas padrão para CSVs
DEFAULT_CSV_COLUMNS = {
    "tracks": ["track_id", "title", "artist", "album", "duration", "isrc", "upc", "release_date"],
    "albums": ["album_id", "title", "artist", "upc", "release_date", "track_count", "label"],
    "artists": ["artist_id", "name", "country", "genre", "biography"],
    "sales": ["date", "track_id", "territory", "store", "quantity", "revenue", "currency"]
}

# Limites do sistema
MAX_UPLOAD_SIZE = 100 * 1024 * 1024  # 100MB
MAX_BATCH_SIZE = 1000
DEFAULT_PAGE_SIZE = 50

# Status codes
STATUS_PENDING = "pending"
STATUS_PROCESSING = "processing"
STATUS_COMPLETED = "completed"
STATUS_ERROR = "error"
STATUS_WARNING = "warning"