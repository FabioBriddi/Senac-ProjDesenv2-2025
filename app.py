import streamlit as st
from pathlib import Path
import sys
import pandas as pd
import base64

# Adiciona o diretório src ao path
sys.path.append(str(Path(__file__).parent / "src"))

# Configuração da página
st.set_page_config(
    page_title="BRD Analytics",
    page_icon="images/logo_brd_nota.jpg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Função para carregar imagens
def load_image(image_path, format="jpeg"):
    """Carrega imagem e converte para base64"""
    try:
        with open(image_path, "rb") as f:
            data = base64.b64encode(f.read()).decode()
            return f"data:image/{format};base64,{data}"
    except:
        return None

# Carrega logos
logo_brd = load_image("images/logo_brd.png", "png")
logo_fuga = load_image("images/logo_fuga.jpg")
logo_orchard = load_image("images/logo_theorchard.jpg")
logo_vydia = load_image("images/logo_vydia.jpg")

# CSS customizado profissional - tema claro para apresentação
st.markdown("""
    <style>
    /* Background geral - limpo e claro */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Header principal com logo */
    .main-header-container {
        background: #ffffff;
        padding: 2rem 0;
        margin: -3rem -3rem 2rem -3rem;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        border-bottom: 3px solid #0f3460;
    }
    
    .main-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 25px;
    }
    
    .header-logo {
        height: 70px;
        width: auto;
    }
    
    .header-text {
        font-size: 3rem;
        font-weight: 700;
        color: #1a1a2e !important;
        letter-spacing: -0.5px;
        margin: 0;
    }
    
    /* Cards e containers */
    .element-container {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Estilo dos botões */
    .stButton>button {
        background-color: #0f3460;
        color: white !important;
        border: none;
        padding: 0.6rem 1.2rem;
        font-weight: 500;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #533483;
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(15, 52, 96, 0.2);
    }
    
    /* Cards de métricas */
    [data-testid="metric-container"] {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        padding: 1.2rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    
    [data-testid="metric-container"] label {
        color: #5a607b !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.75rem;
        letter-spacing: 0.5px;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        background: #f8f9fa;
        padding: 0.75rem;
        border-radius: 8px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        padding: 0 20px;
        background: #ffffff;
        border-radius: 6px;
        border: 1px solid #e0e0e0;
        font-weight: 500;
        color: #1a1a2e;
    }
    
    .stTabs [aria-selected="true"] {
        background: #0f3460;
        color: white !important;
        border-color: #0f3460;
    }
    
    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: #f8f9fa;
        border-right: 2px solid #e0e0e0;
    }
    
    section[data-testid="stSidebar"] h3 {
        color: #1a1a2e !important;
        font-size: 1.1rem;
        font-weight: 600;
        margin-top: 1rem;
    }
    
    /* Text elements */
    .stMarkdown {
        color: #1a1a2e;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #1a1a2e !important;
        font-weight: 600;
    }
    
    /* Select boxes */
    .stSelectbox > div > div {
        background: #ffffff;
        border: 1px solid #e0e0e0;
    }
    
    /* Text inputs */
    .stTextInput > div > div > input {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        color: #1a1a2e;
    }
    
    /* Number inputs */
    .stNumberInput > div > div > input {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        color: #1a1a2e;
    }
    
    /* Date inputs */
    .stDateInput > div > div > input {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        color: #1a1a2e;
    }
    
    /* Info boxes */
    .stInfo {
        background: #e3f2fd;
        border-left: 4px solid #0f3460;
        color: #0f3460;
    }
    
    /* Success messages */
    .stSuccess {
        background: #e8f5e9;
        border-left: 4px solid #4caf50;
        color: #1b5e20;
    }
    
    /* Error messages */
    .stError {
        background: #ffebee;
        border-left: 4px solid #f44336;
        color: #c62828;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: #f8f9fa;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        color: #1a1a2e !important;
    }
    
    /* DataFrames */
    .dataframe {
        background-color: #ffffff !important;
    }
    
    .dataframe th {
        background-color: #0f3460 !important;
        color: #ffffff !important;
        font-weight: 600;
        text-transform: uppercase;
        font-size: 0.8rem;
    }
    
    .dataframe td {
        color: #1a1a2e !important;
        border-bottom: 1px solid #f0f0f0;
    }
    
    /* File uploader */
    .stFileUploader > div {
        background: #f8f9fa;
        border: 2px dashed #d0d0d0;
        border-radius: 8px;
    }
    
    .stFileUploader > div:hover {
        border-color: #0f3460;
        background: #f0f0f0;
    }
    
    /* HR separators */
    hr {
        border: 0;
        height: 1px;
        background: #e0e0e0;
        margin: 2rem 0;
    }
    
    /* Footer */
    .footer {
        background: #f8f9fa;
        padding: 2rem;
        margin: 3rem -3rem -3rem -3rem;
        border-top: 2px solid #0f3460;
        text-align: center;
        color: #1a1a2e;
        font-weight: 500;
    }
    
    /* Plotly charts */
    .js-plotly-plot {
        background: #ffffff !important;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
    """, unsafe_allow_html=True)

# Header principal com logo
if logo_brd:
    st.markdown(f'''
        <div class="main-header-container">
            <div class="main-header">
                <img src="{logo_brd}" class="header-logo" alt="BRD Logo">
                <h1 class="header-text">BRD Analytics</h1>
            </div>
        </div>
    ''', unsafe_allow_html=True)
else:
    st.markdown('<div class="main-header-container"><h1 class="header-text">BRD Analytics</h1></div>', unsafe_allow_html=True)

# Sidebar para navegação
with st.sidebar:
    st.markdown("### Menu Principal")
    
    page = st.selectbox(
        "Navegação",
        ["Dashboard", "Configurações", "Relatórios", "Importação de Dados"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Seletor de distribuidora
    st.markdown("### Distribuidora")
    distributor = st.selectbox(
        "Selecione",
        ["Todas", "Fuga", "The Orchard", "Vydia"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.markdown("### Status do Sistema")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("APIs Ativas", "0")
    with col2:
        st.metric("Última Sync", "N/A")
    
    st.markdown("---")
    st.markdown("### Informações")
    st.text("Versão: 1.0.0")
    st.text("Build: 2025.01")

# Conteúdo principal baseado na página selecionada
if page == "Dashboard":
    # Dashboard principal
    st.markdown("## Dashboard Principal")
    
    # Importar módulos necessários para estatísticas
    try:
        from src.csv_processors.analytics_processor import AnalyticsCSVProcessor
        from src.database.models import init_database
        
        # Inicializa banco e obtém estatísticas
        init_database()
        processor = AnalyticsCSVProcessor()
        summary = processor.get_analytics_summary("AllMark")
        
        # Métricas principais
        st.markdown("### Métricas Gerais")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_streams = summary.get('total_streams', 0) if 'error' not in summary else 0
            st.metric(
                label="Total de Streams",
                value=f"{total_streams:,}",
                delta="AllMark"
            )
        
        with col2:
            total_revenue = summary.get('total_revenue', 0) if 'error' not in summary else 0
            st.metric(
                label="Receita Estimada",
                value=f"${total_revenue:,.2f}",
                delta="USD"
            )
        
        with col3:
            num_dsps = len(summary.get('dsps', {})) if 'error' not in summary else 0
            st.metric(
                label="Plataformas",
                value=str(num_dsps),
                delta="DSPs"
            )
        
        with col4:
            total_records = summary.get('total_records', 0) if 'error' not in summary else 0
            st.metric(
                label="Registros",
                value=str(total_records),
                delta="No banco"
            )
    except:
        # Se não houver dados, mostra métricas vazias
        st.markdown("### Métricas Gerais")
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total de Streams",
                value="0",
                delta="Sem dados"
            )
        
        with col2:
            st.metric(
                label="Receita Estimada",
                value="$0.00",
                delta="USD"
            )
        
        with col3:
            st.metric(
                label="Plataformas",
                value="0",
                delta="DSPs"
            )
        
        with col4:
            st.metric(
                label="Registros",
                value="0",
                delta="No banco"
            )
    
    st.markdown("---")
    
    # Seções para cada distribuidora
    st.markdown("### Status das Distribuidoras")
    tab1, tab2, tab3 = st.tabs(["Fuga Music", "The Orchard", "Vydia"])
    
    with tab1:
        col_logo, col_info = st.columns([1, 4])
        with col_logo:
            if logo_fuga:
                st.markdown(f'<img src="{logo_fuga}" style="width: 150px;">', unsafe_allow_html=True)
        with col_info:
            st.markdown("#### Fuga Music")
            col1, col2 = st.columns(2)
            with col1:
                st.info("**Status:** Não Configurado")
                st.metric("Faixas", "0")
                st.metric("Última Atualização", "N/A")
            with col2:
                st.text("Endpoint: api.fugamusic.com")
                st.metric("Álbuns", "0")
                st.metric("Taxa de Sucesso", "N/A")
    
    with tab2:
        col_logo, col_info = st.columns([1, 4])
        with col_logo:
            if logo_orchard:
                st.markdown(f'<img src="{logo_orchard}" style="width: 150px;">', unsafe_allow_html=True)
        with col_info:
            st.markdown("#### The Orchard")
            col1, col2 = st.columns(2)
            with col1:
                st.info("**Status:** Não Configurado")
                st.metric("Faixas", "0")
                st.metric("Última Atualização", "N/A")
            with col2:
                st.text("Endpoint: api.theorchard.com")
                st.metric("Álbuns", "0")
                st.metric("Taxa de Sucesso", "N/A")
    
    with tab3:
        col_logo, col_info = st.columns([1, 4])
        with col_logo:
            if logo_vydia:
                st.markdown(f'<img src="{logo_vydia}" style="width: 150px;">', unsafe_allow_html=True)
        with col_info:
            st.markdown("#### Vydia")
            col1, col2 = st.columns(2)
            with col1:
                st.info("**Status:** Não Configurado")
                st.metric("Faixas", "0")
                st.metric("Última Atualização", "N/A")
            with col2:
                st.text("Endpoint: api.vydia.com")
                st.metric("Álbuns", "0")
                st.metric("Taxa de Sucesso", "N/A")

elif page == "Configurações":
    st.markdown("## Configurações das APIs")
    
    # Tabs para cada distribuidora
    tab1, tab2, tab3 = st.tabs(["Fuga Music", "The Orchard", "Vydia"])
    
    with tab1:
        if logo_fuga:
            st.markdown(f'<img src="{logo_fuga}" style="width: 120px; margin-bottom: 20px;">', unsafe_allow_html=True)
        
        st.markdown("### Configurações - Fuga Music")
        with st.form("fuga_config"):
            col1, col2 = st.columns(2)
            with col1:
                api_key = st.text_input("API Key", type="password")
                api_secret = st.text_input("API Secret", type="password")
                endpoint = st.text_input("Endpoint", value="https://api.fugamusic.com")
            with col2:
                rate_limit = st.number_input("Rate Limit (req/min)", min_value=1, value=60)
                timeout = st.number_input("Timeout (segundos)", min_value=1, value=30)
                auto_sync = st.checkbox("Sincronização Automática", value=True)
            
            if st.form_submit_button("Salvar Configurações"):
                st.success("Configurações da Fuga salvas com sucesso!")
    
    with tab2:
        if logo_orchard:
            st.markdown(f'<img src="{logo_orchard}" style="width: 120px; margin-bottom: 20px;">', unsafe_allow_html=True)
        
        st.markdown("### Configurações - The Orchard")
        with st.form("orchard_config"):
            col1, col2 = st.columns(2)
            with col1:
                client_id = st.text_input("Client ID")
                client_secret = st.text_input("Client Secret", type="password")
                endpoint = st.text_input("Endpoint", value="https://api.theorchard.com")
            with col2:
                rate_limit = st.number_input("Rate Limit (req/min)", min_value=1, value=100)
                timeout = st.number_input("Timeout (segundos)", min_value=1, value=30)
                auto_sync = st.checkbox("Sincronização Automática", value=True)
            
            if st.form_submit_button("Salvar Configurações"):
                st.success("Configurações do Orchard salvas com sucesso!")
    
    with tab3:
        if logo_vydia:
            st.markdown(f'<img src="{logo_vydia}" style="width: 120px; margin-bottom: 20px;">', unsafe_allow_html=True)
        
        st.markdown("### Configurações - Vydia")
        with st.form("vydia_config"):
            col1, col2 = st.columns(2)
            with col1:
                api_token = st.text_input("API Token", type="password")
                account_id = st.text_input("Account ID")
                endpoint = st.text_input("Endpoint", value="https://api.vydia.com")
            with col2:
                rate_limit = st.number_input("Rate Limit (req/min)", min_value=1, value=30)
                timeout = st.number_input("Timeout (segundos)", min_value=1, value=30)
                auto_sync = st.checkbox("Sincronização Automática", value=False)
            
            if st.form_submit_button("Salvar Configurações"):
                st.success("Configurações do Vydia salvas com sucesso!")

elif page == "Relatórios":
    st.markdown("## Relatórios e Análises")
    
    # Filtros
    st.markdown("### Filtros")
    col1, col2, col3 = st.columns(3)
    with col1:
        report_type = st.selectbox(
            "Tipo de Relatório",
            ["Resumo Geral", "Por Distribuidora", "Comparativo", "Histórico"]
        )
    with col2:
        date_from = st.date_input("Data Inicial")
    with col3:
        date_to = st.date_input("Data Final")
    
    # Botão de gerar relatório
    if st.button("Gerar Relatório", type="primary"):
        with st.spinner("Gerando relatório..."):
            try:
                from src.csv_processors.analytics_processor import AnalyticsCSVProcessor
                from src.database.models import init_database
                
                init_database()
                processor = AnalyticsCSVProcessor()
                summary = processor.get_analytics_summary("AllMark")
                
                if 'error' not in summary and summary.get('total_streams', 0) > 0:
                    st.success("Relatório gerado com sucesso!")
                    
                    # Visualização com dados reais
                    import plotly.express as px
                    import plotly.graph_objects as go
                    
                    # Prepara dados para o gráfico
                    if summary.get('dsps'):
                        dsp_data = []
                        for dsp, data in summary['dsps'].items():
                            dsp_data.append({
                                'DSP': dsp,
                                'Streams': data['streams'],
                                'Receita': data['revenue']
                            })
                        
                        df = pd.DataFrame(dsp_data)
                        
                        # Gráfico de barras profissional
                        fig = go.Figure(data=[
                            go.Bar(
                                x=df['DSP'],
                                y=df['Streams'],
                                text=df['Streams'].apply(lambda x: f'{x:,.0f}'),
                                textposition='outside',
                                marker_color='#0f3460'
                            )
                        ])
                        fig.update_layout(
                            title="Streams por Plataforma",
                            xaxis_title="Plataforma",
                            yaxis_title="Número de Streams",
                            showlegend=False,
                            height=400,
                            template="plotly_white"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Gráfico de pizza para receita
                        fig2 = px.pie(
                            df, 
                            values='Receita', 
                            names='DSP',
                            title='Distribuição de Receita por DSP',
                            color_discrete_sequence=['#0f3460', '#16213e', '#1a1a2e', '#533483', '#764ba2']
                        )
                        st.plotly_chart(fig2, use_container_width=True)
                        
                        # Tabela de dados
                        st.markdown("### Dados Detalhados")
                        st.dataframe(df.style.format({
                            'Streams': '{:,.0f}',
                            'Receita': '${:,.2f}'
                        }), use_container_width=True)
                    else:
                        st.info("Importe dados de analytics primeiro para visualizar relatórios.")
                else:
                    st.info("Nenhum dado disponível. Importe arquivos CSV primeiro.")
                    
            except Exception as e:
                st.error(f"Erro ao gerar relatório: {str(e)}")
                st.info("Importe dados primeiro através da página de Importação de Dados.")

elif page == "Importação de Dados":
    st.markdown("## Importação de Dados")
    
    # Importar bibliotecas necessárias
    from pathlib import Path
    
    # Importar processador
    try:
        from src.csv_processors.analytics_processor import AnalyticsCSVProcessor
        from src.database.models import init_database, get_session, Analytics, Artist
        
        # Inicializa banco
        init_database()
        
        # Tabs para diferentes tipos de upload
        tab1, tab2, tab3 = st.tabs(["Analytics/Streams", "Catálogo", "Relatórios Financeiros"])
        
        with tab1:
            st.markdown("### Importar Analytics de Streams")
            
            # Informações sobre o formato
            with st.expander("Formato esperado do CSV"):
                st.info("""
                **Estrutura do arquivo CSV:**
                - Primeira coluna: `DSP` (nome da plataforma)
                - Demais colunas: Datas no formato `DD mes` (ex: "8 set", "9 set")
                - Valores: Número de streams para cada DSP/Data
                
                **Plataformas suportadas:**
                Spotify, Apple Music, YouTube Music, Amazon Music, Deezer, Tidal, SoundCloud, entre outras.
                """)
            
            # Upload
            uploaded_file = st.file_uploader(
                "Selecione o arquivo CSV de Analytics",
                type=['csv'],
                key="analytics_upload"
            )
            
            if uploaded_file:
                # Mostra preview
                df_preview = pd.read_csv(uploaded_file)
                st.markdown("### Preview do arquivo")
                st.dataframe(df_preview.head(10), use_container_width=True)
                
                # Reset do buffer do arquivo
                uploaded_file.seek(0)
                
                # Configurações de importação
                st.markdown("### Configurações de Importação")
                col1, col2 = st.columns(2)
                with col1:
                    artist_name = st.text_input("Nome do Artista", value="AllMark")
                with col2:
                    year = st.number_input("Ano dos dados", min_value=2020, max_value=2026, value=2025)
                
                if st.button("Processar Analytics", type="primary"):
                    with st.spinner(f"Processando {uploaded_file.name}..."):
                        # Salva arquivo temporariamente
                        temp_path = Path(f"data/uploads/temp_{uploaded_file.name}")
                        temp_path.parent.mkdir(parents=True, exist_ok=True)
                        
                        with open(temp_path, 'wb') as f:
                            f.write(uploaded_file.getbuffer())
                        
                        # Processa
                        processor = AnalyticsCSVProcessor()
                        result = processor.process_analytics_csv(str(temp_path), artist_name)
                        
                        if result['status'] == 'success':
                            st.success("Arquivo processado com sucesso!")
                            
                            # Mostra estatísticas
                            st.markdown("### Resumo da Importação")
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Total de Streams", f"{result.get('total_streams', 0):,}")
                            with col2:
                                st.metric("Registros Processados", result.get('rows_success', 0))
                            with col3:
                                st.metric("DSPs Encontradas", len(result.get('dsps', [])))
                            
                            # Mostra resumo
                            summary = processor.get_analytics_summary(artist_name)
                            if 'error' not in summary:
                                st.markdown("### Resumo dos Analytics")
                                
                                # Métricas gerais
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Total de Streams", f"{summary['total_streams']:,}")
                                with col2:
                                    st.metric("Receita Estimada", f"${summary['total_revenue']:,.2f}")
                                with col3:
                                    st.metric("Plataformas", len(summary.get('dsps', {})))
                                
                                # Detalhes por DSP
                                if summary.get('dsps'):
                                    st.markdown("### Breakdown por DSP")
                                    dsp_data = []
                                    for dsp, data in summary['dsps'].items():
                                        dsp_data.append({
                                            'DSP': dsp,
                                            'Streams': data['streams'],
                                            'Receita': data['revenue'],
                                            'Dias': data['days']
                                        })
                                    df_dsp = pd.DataFrame(dsp_data)
                                    st.dataframe(
                                        df_dsp.style.format({
                                            'Streams': '{:,.0f}',
                                            'Receita': '${:,.2f}'
                                        }), 
                                        use_container_width=True
                                    )
                        else:
                            st.error(f"Erro no processamento: {result.get('message', 'Erro desconhecido')}")
        
        with tab2:
            st.markdown("### Importar Catálogo de Músicas")
            st.info("Funcionalidade em desenvolvimento")
            st.markdown("""
            **Em breve você poderá importar:**
            - Lista de faixas (tracks)
            - Álbuns
            - Informações de artistas
            """)
        
        with tab3:
            st.markdown("### Importar Relatórios Financeiros")
            st.info("Funcionalidade em desenvolvimento")
            st.markdown("""
            **Em breve você poderá importar:**
            - Relatórios de vendas
            - Relatórios de royalties
            - Demonstrativos financeiros
            """)
            
    except ImportError as e:
        st.error(f"Erro ao importar módulos: {str(e)}")
        st.info("Certifique-se de que todos os arquivos estão no lugar correto e as dependências instaladas.")
    
    # Histórico de uploads
    st.markdown("---")
    st.markdown("### Histórico de Importações")
    
    # Mostra histórico real se houver dados
    try:
        from src.database.models import get_session, CSVImport
        session = get_session()
        imports = session.query(CSVImport).order_by(CSVImport.imported_at.desc()).limit(10).all()
        
        if imports:
            history_data = []
            for imp in imports:
                status_icon = "✓" if imp.status == 'completed' else "✗"
                history_data.append({
                    'Data': imp.imported_at.strftime('%Y-%m-%d %H:%M'),
                    'Arquivo': imp.filename,
                    'Tipo': imp.import_type,
                    'Status': f"{status_icon} {imp.status}",
                    'Registros': imp.rows_success
                })
            
            history_df = pd.DataFrame(history_data)
            st.dataframe(history_df, use_container_width=True)
        else:
            st.info("Nenhuma importação realizada ainda.")
            
        session.close()
    except:
        st.info("Nenhuma importação realizada ainda.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div class='footer'>
        <strong>BRD Analytics</strong> | Versão 1.0.0 | © 2025 BRD - Todos os direitos reservados
    </div>
    """,
    unsafe_allow_html=True
)