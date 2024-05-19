from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Obtener la API key de la variable de entorno
OLLAMA_API_KEY = os.getenv("OLLAMA_API_KEY")
OLLAMA_API_URL = "https://api.ollama.com/v1/chat"  # Asegúrate de que este sea el endpoint correcto

# Función para interactuar con la API de Ollama
def interact_with_ollama(user_message):
    headers = {
        "Authorization": f"Bearer {OLLAMA_API_KEY}",
        "Content-Type": "application/json"
    }
    
    data = {
        "message": user_message
    }
    
    response = requests.post(OLLAMA_API_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json().get("response")
    else:
        return "Lo siento, hubo un error al procesar tu solicitud."

# Ruta principal del chatbot
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400
    
    bot_reply = interact_with_ollama(user_message)
    
    return jsonify({"reply": bot_reply})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
