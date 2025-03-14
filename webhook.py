from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Rota do webhook
@app.route('/api/webhook', methods=['POST'])
def receive_webhook():
    data = request.json
    if 'messages' in data:
        for message in data['messages']:
            number = message['key']['remoteJid'].split('@')[0]
            text = message.get('message', {}).get('conversation', '')

            if text:
                send_whatsapp_message(number, f"Você disse: {text}")

    return jsonify({"status": "received"}), 200

# Função para enviar mensagem pelo Evolution API
def send_whatsapp_message(number, text):
    url = f"https://{os.getenv('EVOLUTION_API_SERVER')}/message/sendText/{os.getenv('EVOLUTION_INSTANCE')}"
    headers = {
        'Content-Type': 'application/json',
        'apikey': os.getenv('EVOLUTION_API_KEY')
    }
    payload = {
        'number': number,
        'options': {
            'delay': 1000,
            'presence': 'composing'
        },
        'textMessage': {
            'text': text
        }
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

# Apenas para desenvolvimento local
if __name__ == '__main__':
    app.run(port=5000)
