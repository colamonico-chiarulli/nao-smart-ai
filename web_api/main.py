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
Last Modified: 	February 21st 2026, 11:54:00 am
Modified By: 	Rino Andriano <andriano@colamonicochiarulli.edu.it>
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
# from utils.gemini_chat_api import GeminiChatAPI
from utils.llm_chat_api import LLMChatAPI
from utils.stt import STT




def create_app():
    """
    " Crea e configura l'applicazione Flask
    " :return: Istanza dell'applicazione Flask configurata
    """
    app = Flask(__name__)
    CORS(app)  # Abilita CORS per tutte le routes

    # Crea l'istanza del gestore API
    # chat_api = GeminiChatAPI()
    chat_api = LLMChatAPI()

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

    @app.route("/stt/vosk/fast", methods=["POST"])
    def speech_to_text_vosk_fast():
        """
        Endpoint per Speech-to-Text con Vosk (offline) ottimizzato
        Accetta OGG (o altri formati), converte lato server e trascrive.
        """
        # Verifica presenza file audio
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'Nessun file audio fornito'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'success': False, 'error': 'Nome file non valido'}), 400

        # Estrai metadata opzionali per Smart Trim
        timing_metadata = {}
        if 'recording_start' in request.form:
            timing_metadata['recording_start'] = request.form['recording_start']
        if 'speech_detected' in request.form:
             timing_metadata['speech_detected'] = request.form['speech_detected']

        # Usa la nuova funzione transcribe_ogg
        success, result = stt.transcribe_ogg(audio_file, timing_metadata)
        
        if success:
            return jsonify({'success': True, **result}), 200
        else:
            status_code = 503 if 'instructions' in result else 200
            return jsonify({'success': False, **result}), status_code

    @app.route("/chat/voice", methods=["POST"])
    def chat_voice():
        """
        Endpoint combinato: STT + Chat LLM in una singola chiamata.
        Input: audio (file OGG/WAV), chat_id (opzionale)
        Output: Risposta LLM con trascrizione inclusa
        Include timing statistics se TIMING_ENABLED
        """
        # 1. Verifica presenza file audio (stesso controllo di /stt/vosk/fast)
        if 'audio' not in request.files:
            return jsonify({'success': False, 'error': 'Nessun file audio fornito'}), 400
        
        audio_file = request.files['audio']
        if audio_file.filename == '':
            return jsonify({'success': False, 'error': 'Nome file non valido'}), 400

        # 2. Estrai metadata opzionali per Smart Trim
        timing_metadata = {}
        if 'recording_start' in request.form:
            timing_metadata['recording_start'] = request.form['recording_start']
        if 'speech_detected' in request.form:
            timing_metadata['speech_detected'] = request.form['speech_detected']

        # Trascrizione audio -> testo (usa transcribe_ogg come /stt/vosk/fast)
        success, stt_result = stt.transcribe_ogg(audio_file, timing_metadata)
               
        if not success:
            status_code = 503 if 'instructions' in stt_result else 400
            return jsonify({'success': False, 'stage': 'stt', **stt_result}), status_code
        
        transcribed_text = stt_result.get('text', '').strip()
        if not transcribed_text:
            return jsonify({'success': False, 'error': 'Trascrizione vuota', 'stage': 'stt'}), 400

        # 3. Prepara i dati per handle_talk_action
        chat_data = {
            "action": "talk",
            "chat_id": request.form.get("chat_id"),  # Può essere None per nuove chat
            "message": transcribed_text
        }

        # 4. Chiama handle_talk_action e ottieni la risposta
        try:

            response, status_code = chat_api.handle_talk_action(chat_data)
            
            # 5. Arricchisci la risposta con i dati della trascrizione
            response_data = response.get_json()
            response_data['transcription'] = transcribed_text         
            return jsonify(response_data), status_code
        except Exception as e:
            chat_api.logger.log_error(f"Errore in chat/voice LLM: {str(e)}")
            return jsonify({
                'success': False, 
                'stage': 'llm',
                'error': str(e),
                 'transcription': transcribed_text
            }), 500
    

    
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
