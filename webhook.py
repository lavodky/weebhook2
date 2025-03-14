from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """Webhook recebe mensagem e chama a função de resposta"""
    data = request.json
    if "data" in data and "key" in data["data"]:
        number = data["data"]["key"]["remoteJid"].split("@")[0]
        send_whatsapp_message(number)  # Chama a função para responder
    return {"status": "received"}, 200
