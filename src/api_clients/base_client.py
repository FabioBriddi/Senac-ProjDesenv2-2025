"""
Base client for music distribution APIs
"""
import requests
from typing import Dict, Any, Optional, List
from datetime import datetime
import json
import time
from pathlib import Path
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseAPIClient:
    """Classe base para todos os clientes de API de distribuidoras"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        """
        Inicializa o cliente base
        
        Args:
            name: Nome da distribuidora
            config: Configurações da API
        """
        self.name = name
        self.base_url = config.get('endpoint', '')
        self.api_key = config.get('api_key', '')
        self.api_secret = config.get('api_secret', '')
        self.rate_limit = config.get('rate_limit', 60)  # requests por minuto
        self.timeout = config.get('timeout', 30)
        self.session = requests.Session()
        self.last_request_time = 0
        self.request_count = 0
        
        # Configurar headers padrão
        self.session.headers.update({
            'User-Agent': f'MusicDistributionAPI/{name}/1.0',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
        
        # Diretórios para cache e logs
        self.cache_dir = Path(f"data/cache/{name.lower()}")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        
    def _rate_limit_check(self):
        """Verifica e aplica rate limiting"""
        current_time = time.time()
        
        # Reset contador a cada minuto
        if current_time - self.last_request_time > 60:
            self.request_count = 0
            self.last_request_time = current_time
        
        # Verifica se excedeu o limite
        if self.request_count >= self.rate_limit:
            sleep_time = 60 - (current_time - self.last_request_time)
            if sleep_time > 0:
                logger.info(f"Rate limit atingido. Aguardando {sleep_time:.1f} segundos...")
                time.sleep(sleep_time)
                self.request_count = 0
                self.last_request_time = time.time()
        
        self.request_count += 1
        
    def _make_request(self, method: str, endpoint: str, 
                     params: Optional[Dict] = None, 
                     data: Optional[Dict] = None,
                     headers: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Faz uma requisição HTTP com tratamento de erros
        
        Args:
            method: Método HTTP (GET, POST, PUT, DELETE)
            endpoint: Endpoint da API
            params: Parâmetros de query
            data: Dados do corpo da requisição
            headers: Headers adicionais
            
        Returns:
            Resposta da API em formato dict
        """
        self._rate_limit_check()
        
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        
        # Merge headers
        request_headers = self.session.headers.copy()
        if headers:
            request_headers.update(headers)
        
        try:
            logger.info(f"[{self.name}] {method} {url}")
            
            response = self.session.request(
                method=method,
                url=url,
                params=params,
                json=data,
                headers=request_headers,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            
            # Tentar fazer parse do JSON
            if response.content:
                return response.json()
            return {}
            
        except requests.exceptions.Timeout:
            logger.error(f"[{self.name}] Timeout na requisição para {url}")
            raise TimeoutError(f"Timeout ao acessar {self.name}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"[{self.name}] Erro na requisição: {str(e)}")
            raise ConnectionError(f"Erro ao conectar com {self.name}: {str(e)}")
            
        except json.JSONDecodeError:
            logger.error(f"[{self.name}] Resposta não é JSON válido")
            return {'raw_response': response.text}
    
    def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """Requisição GET"""
        return self._make_request('GET', endpoint, params=params)
    
    def post(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Requisição POST"""
        return self._make_request('POST', endpoint, data=data)
    
    def put(self, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """Requisição PUT"""
        return self._make_request('PUT', endpoint, data=data)
    
    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Requisição DELETE"""
        return self._make_request('DELETE', endpoint)
    
    def test_connection(self) -> bool:
        """
        Testa a conexão com a API
        
        Returns:
            True se a conexão foi bem sucedida
        """
        try:
            # Este método deve ser sobrescrito pelas classes filhas
            # com o endpoint correto de teste
            self.get('/health')
            return True
        except Exception as e:
            logger.error(f"[{self.name}] Falha no teste de conexão: {str(e)}")
            return False
    
    def get_cache_file(self, cache_key: str) -> Optional[Path]:
        """
        Retorna o caminho do arquivo de cache
        
        Args:
            cache_key: Chave do cache
            
        Returns:
            Path do arquivo de cache se existir
        """
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            # Verifica se o cache não está muito antigo (24 horas)
            file_age = time.time() - cache_file.stat().st_mtime
            if file_age < 86400:  # 24 horas
                return cache_file
        return None
    
    def save_to_cache(self, cache_key: str, data: Any):
        """
        Salva dados no cache
        
        Args:
            cache_key: Chave do cache
            data: Dados para salvar
        """
        cache_file = self.cache_dir / f"{cache_key}.json"
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def load_from_cache(self, cache_key: str) -> Optional[Any]:
        """
        Carrega dados do cache
        
        Args:
            cache_key: Chave do cache
            
        Returns:
            Dados do cache ou None se não existir
        """
        cache_file = self.get_cache_file(cache_key)
        if cache_file:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None
    
    # Métodos abstratos que devem ser implementados pelas classes filhas
    def authenticate(self) -> bool:
        """Autentica com a API"""
        raise NotImplementedError(f"authenticate() deve ser implementado por {self.__class__.__name__}")
    
    def get_tracks(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Obtém lista de faixas"""
        raise NotImplementedError(f"get_tracks() deve ser implementado por {self.__class__.__name__}")
    
    def get_albums(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Obtém lista de álbuns"""
        raise NotImplementedError(f"get_albums() deve ser implementado por {self.__class__.__name__}")
    
    def get_artists(self, limit: int = 100, offset: int = 0) -> List[Dict]:
        """Obtém lista de artistas"""
        raise NotImplementedError(f"get_artists() deve ser implementado por {self.__class__.__name__}")
    
    def get_sales_report(self, start_date: datetime, end_date: datetime) -> Dict:
        """Obtém relatório de vendas"""
        raise NotImplementedError(f"get_sales_report() deve ser implementado por {self.__class__.__name__}")
    
    def upload_track(self, track_data: Dict, audio_file: bytes) -> Dict:
        """Faz upload de uma faixa"""
        raise NotImplementedError(f"upload_track() deve ser implementado por {self.__class__.__name__}")