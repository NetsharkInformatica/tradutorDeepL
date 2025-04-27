import requests

url="https://api-free.deepl.com/v2/translate"

api_key="8d807a93-ed9a-48f7-8b76-91f8c41a9035:fx"

parametros={
    "auth_key":api_key,
    "text":"aprendendo python fazendo um tradutor",
    "target_lang":"EN"
}

requisicao=requests.post(url,data=parametros)

print(requisicao)
print(requisicao.json())