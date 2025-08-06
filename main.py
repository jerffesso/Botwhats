from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Coloque sua API KEY e INSTANCE ID da Z-API
API_KEY = '9CDFB6C199E6DDBB55C38269'
INSTANCE_ID = '3E5488211720F1DB97EC823C7623CF8E'

URL_API_ZAPI = f'https://api.z-api.io/instances/{INSTANCE_ID}/token/{API_KEY}/send-messages'

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("📩 Mensagem recebida:", data)

    try:
        phone = data['message']['from']
        message = data['message']['body'].strip().lower()

        # Mensagem de boas-vindas
        texto_resposta = (
            "👋 Olá! Seja bem-vindo à SD Móveis Projetados.\n\n"
            "Escolha uma opção para continuar:\n"
            "1️⃣ Falar com um atendente\n"
            "2️⃣ Ver portfólio\n"
            "3️⃣ Informações sobre orçamento"
        )

        payload = {
            "phone": phone,
            "message": texto_resposta
        }

        # Envia a mensagem de resposta
        response = requests.post(URL_API_ZAPI, json=payload)
        print("✅ Resposta enviada:", response.status_code, response.text)

    except Exception as e:
        print("❌ Erro ao processar a mensagem:", e)

    return jsonify({'status': 'ok'})

@app.route('/', methods=['GET'])
def home():
    return "✅ Bot WhatsApp está rodando!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
