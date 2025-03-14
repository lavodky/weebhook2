from flask import Flask, request, jsonify

app = Flask(__name__)

# Armazena as mensagens recebidas
messages_received = []

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """Recebe mensagens do Evolution API e armazena para visualização"""
    data = request.json
    
    if "data" in data and "key" in data["data"]:
        message_data = data["data"]
        number = message_data["key"]["remoteJid"].split("@")[0]
        text = message_data.get("message", {}).get("conversation", "")

        # Armazena a mensagem recebida
        if text:
            messages_received.append({"number": number, "message": text})

        print(f"📥 Mensagem recebida de {number}: {text}")

    return jsonify({"status": "received"}), 200

@app.route('/messages', methods=['GET'])
def get_messages():
    """Exibe as mensagens recebidas"""
    return jsonify(messages_received)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
