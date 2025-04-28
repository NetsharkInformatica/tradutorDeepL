import tkinter as tk
from tkinter import ttk, messagebox
import requests

class DeepLTranslator:
    def __init__(self, root):
        self.root = root
        self.root.title("Tradutor DeepL")
        self.root.geometry("800x600")
        
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
        self.api_key = "minha chave aqui"  # Substitua pela sua chave real
        
        # Inicializar UI
        self.create_widgets()
        
    def create_widgets(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame para os campos de texto
        text_frame = ttk.Frame(main_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Campo de texto de entrada
        input_frame = ttk.LabelFrame(text_frame, text="Texto para traduzir", padding="5")
        input_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.input_text = tk.Text(input_frame, wrap=tk.WORD, height=15)
        self.input_text.pack(fill=tk.BOTH, expand=True)
        
        # Campo de texto de saída
        output_frame = ttk.LabelFrame(text_frame, text="Texto traduzido", padding="5")
        output_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.output_text = tk.Text(output_frame, wrap=tk.WORD, height=15, state=tk.DISABLED)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame de controles
        control_frame = ttk.Frame(main_frame)
        control_frame.pack(fill=tk.X, pady=10)
        
        # Seletor de idioma
        ttk.Label(control_frame, text="Idioma de destino:").pack(side=tk.LEFT, padx=5)
        
        self.language_combo = ttk.Combobox(control_frame, values=[f"{name} ({code})" for code, name in self.languages.items()])
        self.language_combo.pack(side=tk.LEFT, padx=5)
        self.language_combo.set("Inglês (EN)")
        
        # Botões
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(side=tk.RIGHT)
        
        clear_btn = ttk.Button(button_frame, text="Limpar", command=self.clear_text)
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        translate_btn = ttk.Button(button_frame, text="Traduzir", command=self.translate_text)
        translate_btn.pack(side=tk.LEFT, padx=5)
        
        # Barra de status
        self.status_var = tk.StringVar()
        self.status_var.set("Pronto")
        
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN)
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)
    
    def translate_text(self):
        # Obter texto de entrada
        text = self.input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Aviso", "Por favor, insira um texto para traduzir.")
            return
        
        # Obter código do idioma selecionado
        lang_selected = self.language_combo.get()
        lang_code = lang_selected[-3:-1]  # Extrai o código (ex: "EN" de "Inglês (EN)")
        
        # Atualizar status
        self.status_var.set("Traduzindo...")
        self.root.update()
        
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
            
            # Exibir texto traduzido
            self.output_text.config(state=tk.NORMAL)
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", translated_text)
            self.output_text.config(state=tk.DISABLED)
            
            self.status_var.set("Tradução concluída com sucesso!")
            
        except requests.exceptions.RequestException as e:
            messagebox.showerror("Erro", f"Erro ao conectar com a API DeepL:\n{str(e)}")
            self.status_var.set("Erro na tradução")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro inesperado:\n{str(e)}")
            self.status_var.set("Erro inesperado")
    
    def clear_text(self):
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)
        self.status_var.set("Campos limpos")

if __name__ == '__main__':
    root = tk.Tk()
    app = DeepLTranslator(root)
    root.mainloop()