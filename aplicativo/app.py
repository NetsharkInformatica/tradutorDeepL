from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

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

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Obter dados do formulário
        text_to_translate = request.form.get('text', '')
        target_lang = request.form.get('language', 'EN')
        
        # Chamar a API DeepL
        params = {
            "auth_key": DEEPL_API_KEY,
            "text": text_to_translate,
            "target_lang": target_lang
        }
        
        response = requests.post(DEEPL_API_URL, data=params)
        
        if response.status_code == 200:
            translated_text = response.json()['translations'][0]['text']
        else:
            translated_text = f"Erro na tradução: {response.status_code} - {response.text}"
        
        return render_template('index.html', 
                            languages=LANGUAGES, 
                            translated_text=translated_text,
                            original_text=text_to_translate,
                            selected_lang=target_lang)
    
    return render_template('index.html', languages=LANGUAGES)

@app.route('/translate', methods=['POST'])
def translate():
    # Versão para AJAX/JSON
    data = request.get_json()
    text_to_translate = data.get('text', '')
    target_lang = data.get('language', 'EN')
    
    params = {
        "auth_key": DEEPL_API_KEY,
        "text": text_to_translate,
        "target_lang": target_lang
    }
    
    response = requests.post(DEEPL_API_URL, data=params)
    
    if response.status_code == 200:
        return jsonify({
            'status': 'success',
            'translated_text': response.json()['translations'][0]['text']
        })
    else:
        return jsonify({
            'status': 'error',
            'message': f"Erro na tradução: {response.status_code}",
            'details': response.text
        }), 400

if __name__ == '__main__':
    app.run(debug=True)