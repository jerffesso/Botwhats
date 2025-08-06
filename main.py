from flask import Flask, request, jsonify
import requests

# Substitua pelos seus dados reais
INSTANCE_ID = "3E5488211720F1DB97EC823C7623CF8E"
ZAPI_TOKEN = "9CDFB6C199E6DDBB55C38269"

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Recebido:", data)

    # 1. Acesso correto aos dados do webhook
    # A Z-API envia uma lista de eventos, precisamos pegar o primeiro
    try:
        event = data["events"][0]
        message_type = event["type"]
        numero = event["from"]
    except (KeyError, IndexError):
        # Se a estrutura não for a esperada, ignoramos
        return jsonify({"status": "ignorado"}), 200

    mensagem_padrao = """Olá! 👋 Seja bem-vindo(a) à SD Móveis Projetados.
Transformamos ambientes com móveis planejados sob medida.

Para agilizar seu atendimento, escolha uma opção:
1️⃣ Fazer um orçamento
2️⃣ Agendar uma visita técnica
3️⃣ Falar com um atendente"""

    resposta = ""
    if message_type == "chat":
        try:
            mensagem = event["body"].strip().lower() # Pega o texto e já converte para minúsculas
            
            if mensagem == "1":
                resposta = """📋 Perfeito! Para fazer um orçamento, por favor me informe:
- Nome completo
- Ambiente (cozinha, quarto, sala, escritório, etc.)
- Cidade e bairro
- Envie fotos ou medidas se tiver
Assim conseguimos preparar uma proposta inicial para você. 📝"""
            elif mensagem == "2":
                resposta = """📅 Ótimo! Para agendar uma visita técnica, me informe:
- Nome completo
- Endereço
- Melhor dia e horário
Nossa equipe entrará em contato para confirmar o agendamento."""
            elif mensagem == "3":
                resposta = """👤 Certo! Vou transferir você para um atendente.
Em instantes alguém da nossa equipe irá te responder. 🤝"""
            else:
                resposta = mensagem_padrao
        except KeyError:
            # Caso não haja a chave 'body' no evento de chat (o que é raro)
            resposta = mensagem_padrao
            
    # Mensagem padrão para outros tipos de mídia
    elif message_type in ["image", "audio", "video", "document"]:
        resposta = "Obrigado! Recebemos sua mídia, já vamos verificar. 😉"
        
    else:
        # Retorna se o tipo de mensagem não for tratado
        return jsonify({"status": "tipo não tratado"}), 200

    # 2. Envia a resposta de volta para a Z-API
    url = f"https://api.z-api.io/instances/{INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"
    payload = {
        "phone": numero,
        "message": resposta
    }
    
    # Adiciona tratamento de erro para a requisição
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status() # Lança um erro para status 4xx/5xx
        print("Resposta da Z-API:", response.json())
        return jsonify({"status": "mensagem enviada"}), 200
    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar mensagem: {e}")
        return jsonify({"status": "erro ao enviar"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
