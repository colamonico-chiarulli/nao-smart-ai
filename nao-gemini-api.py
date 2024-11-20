'''
File:	/nao-gemini-api.py
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright (C) 2024-2026 Rino Andriano, Vito Trifone Gargano
Created Date: Saturday, November 9th 2024, 6:37:29 pm
-----
Last Modified: 	November 19th 2024 7:01:11 pm
Modified By: 	Rino Andriano <andriano@colamonicochiarulli.edu.it>
-----
@license	https://www.gnu.org/licenses/agpl-3.0.html AGPL 3.0
------------------------------------------------------------------------------
REST API - per una caht con NAO Robot e Gemini
Usa un singolo endpoint /api/chat con metodo POST per tutte le operazioni. 
Le diverse azioni sono specificate nel campo action del JSON inviato.
le azioni sono: start, end, hystory
'''

import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from helpers.cleantext import clean_text
from helpers.colamonico_system import SYSTEM_INSTRUCTION 
from helpers.ChatLogger import ChatLogger

# Carica le variabili d'ambiente
current_dir = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(current_dir, 'conf', '.env')
load_dotenv(dotenv_path)
load_dotenv('/home/rino/python/conf/.env')

# Configura Gemini con la tua API key
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# Inizializza il modello Gemini
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=SYSTEM_INSTRUCTION,
    safety_settings={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH
    }
)

app = Flask(__name__)
CORS(app)  # Abilita CORS per tutte le routes

# Dizionario per memorizzare le chat attive
active_chats = {}


# Crea un'istanza del logger ed imposto la cartella ./logs
logger = ChatLogger('logs')

@app.route('/chat', methods=['POST'])
def handle_chat():
    data = request.json
    if not data or 'action' not in data:
        return jsonify({"error": "È richiesta un'azione"}), 400
    
    action = data['action']
    
    try:
        if action == "talk":
            # Inizia una nuova chat o continua una esistente
            chat_id = data.get('chat_id')
            message = data.get('message')
            
            if not message:
                return jsonify({"error": "Un messaggio è necessario per avviare la chat"}), 400
            
            if chat_id and chat_id in active_chats:
                chat = active_chats[chat_id]
            else:
                chat = model.start_chat()
                chat_id = str(id(chat))
                active_chats[chat_id] = chat
            
            # Log incoming message
            logger.log_chat_message(chat_id, "user", message)
            
            response = chat.send_message(message)
            
            # Log response message
            cleaned_response = clean_text(response.text)
            logger.log_chat_message(chat_id, "model", cleaned_response)
            
            return jsonify({
                "chat_id": chat_id,
                "response": cleaned_response,
                "success": True
            })
            
        elif action == "end":
            # Termina una chat
            chat_id = data.get('chat_id')
            if not chat_id:
                return jsonify({"error": "chat_id è necessaria per terminare una chat"}), 400
                
            if chat_id in active_chats:
                # Log chat closure
                logger.log_info(f"CHAT_CLOSED: {chat_id}")
                del active_chats[chat_id]
                return jsonify({
                    "message": "Chat chiusa correttamente",
                    "success": True
                })
            return jsonify({"error": "Chat non trovata"}), 404
            
        elif action == "history":
            # Ottieni la cronologia della chat
            chat_id = data.get('chat_id')
            if not chat_id:
                return jsonify({"error": "un chat_id è necessario per accedere alla storia"}), 400
                
            if chat_id in active_chats:
                chat = active_chats[chat_id]
                history = [
                    {
                        "role": message.role,
                        "content": message.parts[0].text
                    }
                    for message in chat.history
                ]
                return jsonify({
                    "chat_id": chat_id,
                    "history": history,
                    "success": True
                })
            return jsonify({"error": "Chat non trovata"}), 404
            
        else:
            return jsonify({"error": f"Azione sconosciuta: {action}"}), 400
            
    except Exception as e:
        logger.log_error(f"Errore nlla gestione della chat: {str(e)}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500
        
@app.route('/admin', methods=['POST'])
def handle_admin():
    data = request.json
    if not data or 'action' not in data:
        return jsonify({"error": "È richiesta un'azione"}), 400
    
    action = data['action']
    
    try:
        if action == "list-chats":
            full_history = []
            for chat_id, chat in active_chats.items():
                for message in chat.history:
                    full_history.append(
                        {
                            "chat_id": chat_id,
                            "role": message.role,
                            "content": message.parts[0].text
                        })                    
            return jsonify({
                    "full-history": full_history,
                    "success": True
            })
            
        elif action == "delete-chats":
            # Log chat deletion
            logger.log_info("DELETING ALL ACTIVE CHATS")
            # Azzera il Dizionario per memorizzare le chat attive
            active_chats.clear()
            return jsonify({"success": True})
        
        else:
            return jsonify({"error": f"Azione sconosciuta: {action}"}), 400
            
    except Exception as e:
        logger.log_error(f"Error in admin handling: {str(e)}")
        return jsonify({
            "error": str(e),
            "success": False
        }), 500                

if __name__ == '__main__':
    ##############################
    # DEBUG
    ##############################

    #app.run(host="127.0.0.1", port=5003, debug=True)

    ##############################
    # PRODUCTION GUNICORN
    ##############################
    app.run()
