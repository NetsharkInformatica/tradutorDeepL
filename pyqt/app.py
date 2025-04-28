import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                             QLabel, QTextEdit, QComboBox, QPushButton, QWidget,
                             QMessageBox, QStatusBar)
from PyQt5.QtCore import Qt
import requests

class DeepLTranslator(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela principal
        self.setWindowTitle("Tradutor DeepL")
        self.setGeometry(100, 100, 800, 600)
        
        # Idiomas suportados pela DeepL (versão free)
        self.languages = {
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
        
        # Configurações da API
        self.api_url = "https://api-free.deepl.com/v2/translate"
        self.api_key = "8d807a93-ed9a-48f7-8b76-91f8c41a9035:fx"  # Substitua pela sua chave real
        
        # Inicializar UI
        self.init_ui()
        
    def init_ui(self):
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Layout para os campos de texto
        text_layout = QHBoxLayout()
        
        # Campo de texto de entrada
        input_group = QVBoxLayout()
        input_label = QLabel("Texto para traduzir:")
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Digite o texto que deseja traduzir...")
        input_group.addWidget(input_label)
        input_group.addWidget(self.input_text)
        text_layout.addLayout(input_group)
        
        # Campo de texto de saída
        output_group = QVBoxLayout()
        output_label = QLabel("Texto traduzido:")
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("A tradução aparecerá aqui...")
        output_group.addWidget(output_label)
        output_group.addWidget(self.output_text)
        text_layout.addLayout(output_group)
        
        main_layout.addLayout(text_layout)
        
        # Controles
        controls_layout = QHBoxLayout()
        
        # Seletor de idioma
        language_label = QLabel("Idioma de destino:")
        self.language_combo = QComboBox()
        for code, name in self.languages.items():
            self.language_combo.addItem(f"{name} ({code})", code)
        self.language_combo.setCurrentText("Inglês (EN)")
        
        # Botão de tradução
        translate_btn = QPushButton("Traduzir")
        translate_btn.clicked.connect(self.translate_text)
        
        # Botão para limpar
        clear_btn = QPushButton("Limpar")
        clear_btn.clicked.connect(self.clear_text)
        
        # Adicionar controles ao layout
        controls_layout.addWidget(language_label)
        controls_layout.addWidget(self.language_combo)
        controls_layout.addStretch()
        controls_layout.addWidget(clear_btn)
        controls_layout.addWidget(translate_btn)
        
        main_layout.addLayout(controls_layout)
        
        # Barra de status
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Pronto")
        
    def translate_text(self):
        # Obter texto de entrada
        text = self.input_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Aviso", "Por favor, insira um texto para traduzir.")
            return
        
        # Obter idioma selecionado
        lang_code = self.language_combo.currentData()
        
        # Atualizar barra de status
        self.status_bar.showMessage("Traduzindo...")
        QApplication.processEvents()  # Atualizar a UI
        
        try:
            # Fazer requisição para a API DeepL
            params = {
                "auth_key": self.api_key,
                "text": text,
                "target_lang": lang_code
            }
            
            response = requests.post(self.api_url, data=params)
            response.raise_for_status()  # Levanta exceção para erros HTTP
            
            # Processar resposta
            translated_text = response.json()['translations'][0]['text']
            self.output_text.setPlainText(translated_text)
            self.status_bar.showMessage("Tradução concluída com sucesso!", 3000)
            
        except requests.exceptions.RequestException as e:
            QMessageBox.critical(self, "Erro", f"Erro ao conectar com a API DeepL:\n{str(e)}")
            self.status_bar.showMessage("Erro na tradução", 3000)
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro inesperado:\n{str(e)}")
            self.status_bar.showMessage("Erro inesperado", 3000)
    
    def clear_text(self):
        self.input_text.clear()
        self.output_text.clear()
        self.status_bar.showMessage("Campos limpos", 2000)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Configurar estilo (opcional)
    app.setStyle('Fusion')
    
    translator = DeepLTranslator()
    translator.show()
    
    sys.exit(app.exec_())