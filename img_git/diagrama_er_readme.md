## 📊 Diagrama E-R

```mermaid
erDiagram
    sources {
        INTEGER id PK
        TEXT name
        TEXT type
        TEXT description
        INTEGER is_active
    }

    ingestions {
        INTEGER id PK
        INTEGER source_id FK
        TEXT file_name
        TEXT ingested_at
        INTEGER total_rows
    }

    stream_events {
        INTEGER id PK
        INTEGER ingestion_id FK
        TEXT artist_name
        TEXT track_title
        TEXT isrc
        TEXT upc
        TEXT service
        TEXT country
        TEXT stream_date
        INTEGER streams
    }

    device_daily_streams {
        INTEGER id PK
        INTEGER ingestion_id FK
        TEXT distributor
        TEXT device_name
        TEXT day_label
        INTEGER streams
    }

    api_connectors {
        INTEGER id PK
        TEXT name
        TEXT description
        TEXT base_url
        TEXT auth_type
        TEXT api_key
        TEXT api_secret
        TEXT client_id
        TEXT client_secret
        TEXT token_url
        TEXT additional_headers
        INTEGER is_active
        TEXT last_sync_at
        TEXT created_at
        TEXT updated_at
        TEXT notes
    }

    sources ||--o{ ingestions : "possui"
    ingestions ||--o{ stream_events : "gera"
    ingestions ||--o{ device_daily_streams : "gera"
```

### Descrição das Tabelas

| Tabela | Descrição |
|--------|-----------|
| `sources` | Fontes de dados (CSV artistas, CSV dispositivos) |
| `ingestions` | Registro de cada upload/importação de arquivo |
| `stream_events` | Dados de streaming por artista/faixa (granularidade fina) |
| `device_daily_streams` | Dados agregados por dispositivo/dia/distribuidora |
| `api_connectors` | Configuração de conectores de API (FUGA, Vydia, The Orchard) |

### Relacionamentos

| Origem | Destino | Cardinalidade | Descrição |
|--------|---------|---------------|-----------|
| `sources` | `ingestions` | 1:N | Uma fonte pode ter múltiplas ingestões |
| `ingestions` | `stream_events` | 1:N | Uma ingestão gera múltiplos eventos de streaming |
| `ingestions` | `device_daily_streams` | 1:N | Uma ingestão gera múltiplos registros diários |
| `api_connectors` | - | Independente | Tabela de configuração para integrações futuras |
