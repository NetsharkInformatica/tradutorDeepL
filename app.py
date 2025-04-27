import requests

url="https://api-free.deepl.com/v2/translate"

api_key="semchave"

parametros={
    "auth_key":api_key,
    "text":"aprendendo python fazendo um tradutor",
    "target_lang":"EN"
}

requisicao=requests.post(url,data=parametros)

print(requisicao)
print(requisicao.json())