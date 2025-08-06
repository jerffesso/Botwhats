from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Substitua com seus próprios dados
ZAPI_TOKEN = "9CDFB6C199E6DDBB55C38269"
INSTANCE_ID = "3E5488211720F1DB97EC823C7623CF8E"

ZAPI_URL = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{ZAPI_TOKEN}/send-message"

def enviar_mensagem(numero, mensagem):
    payload = {
        "phone": numero,
        "message": mensagem
    }
    requests.post(ZAPI_URL, json=payload)

# Mensagens automáticas
mensagem_boas_vindas = (
    "Olá! 👋 Seja bem-vindo(a) à SD Móveis Projetados.\n"
    "Transformamos ambientes com móveis planejados sob medida.\n\n"
    "Para agilizar seu atendimento, escolha uma opção:\n"
    "1️⃣ Fazer um orçamento\n"
    "2️⃣ Agendar uma visita técnica\n"
    "3️⃣ Falar com um atendente"
)

mensagem_opcao_1 = (
    "Perfeito! Para fazer um orçamento, por favor me informe:\n"
    "- Nome completo\n"
    "- Ambiente (cozinha, quarto, sala, escritório, etc.)\n"
    "- Cidade e bairro\n"
    "- Envie fotos ou medidas se tiver\n"
    "Assim conseguimos preparar uma proposta inicial para você. 📝"
)

mensagem_opcao_2 = (
    "Ótimo! Para agendar uma visita técnica, me informe:\n"
    "- Nome completo\n"
    "- Endereço\n"
    "- Melhor dia e horário\n"
    "Nossa equipe entrará em contato para confirmar o agendamento. 📅"
)

mensagem_opcao_3 = (
    "Certo! Vou transferir você para um atendente.\n"
    "Em instantes alguém da nossa equipe irá te responder. 🤝"
)

@app.route("/", methods=["POST"])
def receber_mensagem():
    data = request.json
    if not data or "message" not in data or "from" not in data["message"]:
        return jsonify({"status": "ignorado"}), 200

    mensagem = data["message"]["text"]["body"].strip().lower()
    numero = data["message"]["from"]

    if mensagem == "1":
        enviar_mensagem(numero, mensagem_opcao_1)
    elif mensagem == "2":
        enviar_mensagem(numero, mensagem_opcao_2)
    elif mensagem == "3":
        enviar_mensagem(numero, mensagem_opcao_3)
    else:
        enviar_mensagem(numero, mensagem_boas_vindas)

    return jsonify({"status": "ok"}), 200

@app.route("/", methods=["GET"])
def home():
    return "Bot SD Móveis ativo!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
