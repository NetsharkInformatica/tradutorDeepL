import streamlit as st
import requests

# Configurações da API DeepL
DEEPL_API_URL = "https://api-free.deepl.com/v2/translate"
DEEPL_API_KEY = "minha chave aqui"  # Substitua pela sua chave real

# Idiomas suportados pela DeepL (versão free)
LANGUAGES = {
    'BG': 'Búlgaro',
    'CS': 'Tcheco',
    'DA': 'Dinamarquês',
    'DE': 'Alemão',
    'EL': 'Grego',
    'EN': 'Inglês',
    'ES': 'Espanhol',
    'ET': 'Estoniano',
    'FI': 'Finlandês',
    'FR': 'Francês',
    'HU': 'Húngaro',
    'IT': 'Italiano',
    'JA': 'Japonês',
    'LT': 'Lituano',
    'LV': 'Letão',
    'NL': 'Holandês',
    'PL': 'Polonês',
    'PT': 'Português',
    'RO': 'Romeno',
    'RU': 'Russo',
    'SK': 'Eslovaco',
    'SL': 'Esloveno',
    'SV': 'Sueco',
    'ZH': 'Chinês'
}

def translate_text(text, target_lang):
    """Função para traduzir texto usando a API DeepL"""
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text,
        "target_lang": target_lang
    }
    
    response = requests.post(DEEPL_API_URL, data=params)
    response.raise_for_status()
    
    return response.json()['translations'][0]['text']

# Configuração da página
st.set_page_config(
    page_title="Tradutor DeepL",
    page_icon="🌐",
    layout="wide"
)

# Título da aplicação
st.title("🌐 Tradutor DeepL")
st.markdown("---")

# Layout em colunas
col1, col2 = st.columns(2)

with col1:
    st.subheader("Texto para traduzir")
    input_text = st.text_area(
        "Digite o texto que deseja traduzir:",
        height=300,
        placeholder="Digite seu texto aqui...",
        label_visibility="collapsed"
    )

with col2:
    st.subheader("Texto traduzido")
    output_text = st.text_area(
        "Tradução aparecerá aqui:",
        height=300,
        disabled=True,
        label_visibility="collapsed"
    )

# Controles
st.markdown("---")
col_controls1, col_controls2, col_controls3 = st.columns([1, 2, 1])

with col_controls1:
    if st.button("Limpar", use_container_width=True):
        input_text = ""
        output_text = ""
        st.rerun()

with col_controls2:
    selected_lang = st.selectbox(
        "Idioma de destino:",
        options=[f"{name} ({code})" for code, name in LANGUAGES.items()],
        index=5  # Inglês como padrão
    )

with col_controls3:
    translate_btn = st.button("Traduzir", type="primary", use_container_width=True)

# Lógica de tradução
if translate_btn and input_text:
    with st.spinner("Traduzindo..."):
        try:
            # Extrai o código do idioma (últimas 2 letras antes do parêntese fechando)
            lang_code = selected_lang[-3:-1]
            
            translated_text = translate_text(input_text, lang_code)
            
            # Atualiza o texto traduzido
            st.session_state.translated_text = translated_text
            st.rerun()
            
        except requests.exceptions.RequestException as e:
            st.error(f"Erro ao conectar com a API DeepL: {str(e)}")
        except Exception as e:
            st.error(f"Ocorreu um erro inesperado: {str(e)}")

# Atualiza o texto traduzido na área de saída
if 'translated_text' in st.session_state:
    output_text = st.session_state.translated_text
    st.text_area(
        "Texto traduzido:",
        value=output_text,
        height=300,
        disabled=True,
        key="output_text_area",
        label_visibility="collapsed"
    )