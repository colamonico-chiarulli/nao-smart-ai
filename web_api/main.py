"""
File:	/web_api/main.py
-----
REST API - gestisce le rotte di GeminiChatAPI per una caht con NAO Robot e Gemini
Usa due endpoint con metodo POST per tutte le operazioni.
Le diverse azioni sono specificate nel campo action del JSON inviato.
/gemini/chat  azioni: talk, end, hystory
/gemini/admin azioni: list-chats, delete-chats
-----
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright (C) 2024-2026 Rino Andriano, Vito Trifone Gargano
Created Date: Saturday, November 9th 2024, 6:37:29 pm
-----
Last Modified: 	October 10th 2025, 19:00:00 pm
Modified By: 	Nuccio Gargano <v.gargano@colamonicochiarulli.edu.it>
-----
@license	https://www.gnu.org/licenses/agpl-3.0.html AGPL 3.0

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
    
Additional Terms under Section 7(b):

The following attribution requirements apply to this work:

1. Copyright notices and author attribution in source code files
   cannot be removed or altered.
2. Any interactive user interface must preserve and display
   author attribution (Copyright, authors, project name).
3. System prompts containing author information cannot be modified
4. Public demonstrations, publications and derivative works
   must credit the original authors.

For full Additional Terms see the LICENSE file.
------------------------------------------------------------------------------
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from utils.gemini_chat_api import GeminiChatAPI
from utils.stt import STT


def create_app():
    """
    " Crea e configura l'applicazione Flask
    " :return: Istanza dell'applicazione Flask configurata
    """
    app = Flask(__name__)
    CORS(app)  # Abilita CORS per tutte le routes

    # Crea l'istanza del gestore API
    chat_api = GeminiChatAPI()

    # Inizializza sistema STT Vosk
    stt = STT(logger=chat_api.logger)
    
    # Stampa messaggio di errore se Vosk non è disponibile
    if not stt.is_available and stt.error_message:
        print(stt.error_message)


    @app.route("/chat", methods=["POST"])
    def handle_chat():
        """Endpoint per la gestione delle chat"""
        data = request.json
        if not data or "action" not in data:
            return jsonify({"error": "È richiesta un'azione"}), 400

        action = data["action"]

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
            return jsonify({"error": str(e), "success": False}), 500

    @app.route("/admin", methods=["POST"])
    def handle_admin():
        """Endpoint per le azioni di amministrazione"""
        data = request.json
        if not data or "action" not in data:
            return jsonify({"error": "È richiesta un'azione"}), 400

        action = data["action"]

        try:
            if action == "list-chats":
                return chat_api.handle_admin_list_chats()
            elif action == "delete-chats":
                return chat_api.handle_admin_delete_chats()
            else:
                return jsonify({"error": f"Azione sconosciuta: {action}"}), 400

        except Exception as e:
            chat_api.logger.log_error(f"Errore nell'admin handling: {str(e)}")
            return jsonify({"error": str(e), "success": False}), 500


    @app.route("/stt/vosk", methods=["POST"])
    def speech_to_text_vosk():
        """
        Endpoint per Speech-to-Text con Vosk (offline)
        Richiede un file audio WAV mono 16bit come 'audio' in multipart/form-data
        """
        return stt.handle_stt_request()
    
    @app.route("/stt/status", methods=["GET"])
    def stt_status():
        """
        Endpoint per verificare lo stato del server e motore STT
        """
        return jsonify(stt.get_status()), 200


    return app


app = create_app()

if __name__ == "__main__":
    ##############################
    # DEBUG
    ##############################
    # NAO Local
    # app.run(host="127.0.0.1", port=3030, debug=True)
    ##############################
    # PRODUCTION GUNICORN
    ##############################
    app.run()
