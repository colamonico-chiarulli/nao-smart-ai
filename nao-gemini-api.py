'''
File:	/nao-gemini-api.py
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright (C) 2024-2026 Rino Andriano, Vito Trifone Gargano
Created Date: Saturday, November 9th 2024, 6:37:29 pm
-----
Last Modified: 	November20th 2024 8:01:11 pm
Modified By: 	Rino Andriano <andriano@colamonicochiarulli.edu.it>
-----
@license	https://www.gnu.org/licenses/agpl-3.0.html AGPL 3.0
------------------------------------------------------------------------------
REST API - gestisce le rotte di GeminiChatAPI per una caht con NAO Robot e Gemini
Usa due endpoint con metodo POST per tutte le operazioni. 
Le diverse azioni sono specificate nel campo action del JSON inviato.
/gemini/chat  azioni: talk, end, hystory
/gemini/admin azioni: list-chats, delete-chats
'''

from flask import Flask, request, jsonify
from flask_cors import CORS
from helpers.GeminiChatAPI import GeminiChatAPI

def create_app():
    """
    " Crea e configura l'applicazione Flask
    " :return: Istanza dell'applicazione Flask configurata
    """
    app = Flask(__name__)
    CORS(app)  # Abilita CORS per tutte le routes
    
    # Crea l'istanza del gestore API
    chat_api = GeminiChatAPI()
    
    @app.route('/chat', methods=['POST'])
    def handle_chat():
        """Endpoint per la gestione delle chat"""
        data = request.json
        if not data or 'action' not in data:
            return jsonify({"error": "È richiesta un'azione"}), 400
        
        action = data['action']
        
        try:
            if action == "talk":
                return chat_api.handle_talk_action(data)
            elif action == "end":
                return chat_api.handle_end_action(data)
            elif action == "history":
                return chat_api.handle_history_action(data)
            else:
                return jsonify({"error": f"Azione sconosciuta: {action}"}), 400
        
        except Exception as e:
            chat_api.logger.log_error(f"Errore nella gestione della chat: {str(e)}")
            return jsonify({
                "error": str(e),
                "success": False
            }), 500
    
    @app.route('/admin', methods=['POST'])
    def handle_admin():
        """Endpoint per le azioni di amministrazione"""
        data = request.json
        if not data or 'action' not in data:
            return jsonify({"error": "È richiesta un'azione"}), 400
        
        action = data['action']
        
        try:
            if action == "list-chats":
                return chat_api.handle_admin_list_chats()
            elif action == "delete-chats":
                return chat_api.handle_admin_delete_chats()
            else:
                return jsonify({"error": f"Azione sconosciuta: {action}"}), 400
        
        except Exception as e:
            chat_api.logger.log_error(f"Errore nell'admin handling: {str(e)}")
            return jsonify({
                "error": str(e),
                "success": False
            }), 500
    
    return app

app = create_app()

if __name__ == '__main__':

    ##############################
    # DEBUG
    ##############################
    #app.run(host="127.0.0.1", port=5003, debug=True)
    
    ##############################
    # PRODUCTION GUNICORN
    ##############################
    app.run()