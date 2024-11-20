'''
File:	/helpers/GeminiChatAPI.py
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright	(c)2024 Rino Andriano
Created Date: Wednesday, November 20th 2024, 6:37:29 pm
-----
Last Modified: 	November20th 2024 8:01:11 pm
Modified By: 	Rino Andriano <andriano@colamonicochiarulli.edu.it>
-----
@license	https://www.gnu.org/licenses/agpl-3.0.html AGPL 3.0
------------------------------------------------------------------------------
Classe GeminiChatAPI - per gestire le interazioni API con il modello Gemini
Le diverse azioni sono specificate nel campo action del JSON inviato.
/gemini/chat  azioni: talk, end, hystory
/gemini/admin azioni: list-chats, delete-chats
'''

import os
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from helpers.cleantext import clean_text
from helpers.colamonico_system import SYSTEM_INSTRUCTION 
from helpers.ChatLogger import ChatLogger
from flask import jsonify

class GeminiChatAPI:
    """
    " Classe per gestire le interazioni API con il modello Gemini
    """
    def __init__(self, logs_dir='logs'):
        """ Inizializza l'API per la gestione delle chat con Gemini
        " :param logs_dir: Directory per i log delle chat
        """
        # Logger interno alla classe
        self.logger = ChatLogger(logs_dir)
        
        # Carica le variabili d'ambiente
        self._load_environment()
        
        # Configura Gemini con l'API key
        genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))
        
        # Inizializza il modello Gemini
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_INSTRUCTION,
            safety_settings=self._get_safety_settings()
        )
        
        # Dizionario per memorizzare le chat attive
        self.active_chats = {}
    
    def _load_environment(self):
        """Carica le variabili d'ambiente dai file .env"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(current_dir, '..', 'conf', '.env')
        load_dotenv(dotenv_path)
        load_dotenv('/home/rino/python/conf/.env')
    
    def _get_safety_settings(self):
        """Configurazione delle impostazioni di sicurezza per Gemini"""
        return {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH
        }
    
    def handle_talk_action(self, data):
        """  Gestisce l'azione di conversazione (talk)
        "
        " :param data: Dizionario contenente i dati della richiesta
        " :return: Risposta JSON con l'esito della conversazione
        """
        
        # Estrai chat_id e messaggio
        chat_id = data.get('chat_id')
        message = data.get('message')
        
        # Validazione input
        if not message:
            return jsonify({"error": "Un messaggio è necessario per avviare la chat"}), 400
        
        # Gestisce la chat (nuova o esistente)
        if chat_id and chat_id in self.active_chats:
            chat = self.active_chats[chat_id]
        else:
            chat = self.model.start_chat()
            chat_id = str(id(chat))
            self.active_chats[chat_id] = chat
        
        # Log del messaggio in arrivo
        self.logger.log_chat_message(chat_id, "user", message)
        
        # Invia il messaggio e ottieni la risposta
        response = chat.send_message(message)
        
        # Pulisci e log della risposta
        cleaned_response = clean_text(response.text)
        self.logger.log_chat_message(chat_id, "model", cleaned_response)
        
        return jsonify({
            "chat_id": chat_id,
            "response": cleaned_response,
            "success": True
        })
    
    def handle_end_action(self, data):
        """ Termina una chat specifica
        "
        " :param data: Dizionario contenente i dati della richiesta
        " :return: Risposta JSON con l'esito della chiusura
        """
        
        chat_id = data.get('chat_id')
        if not chat_id:
            return jsonify({"error": "chat_id è necessaria per terminare una chat"}), 400
        
        if chat_id in self.active_chats:
            # Log chiusura chat
            self.logger.log_info(f"CHAT_CLOSED: {chat_id}")
            del self.active_chats[chat_id]
            return jsonify({
                "message": "Chat chiusa correttamente",
                "success": True
            })
        return jsonify({"error": "Chat non trovata"}), 404
    
    def handle_history_action(self, data):
        """  Recupera la storia di una chat specifica
        "
        " :param data: Dizionario contenente i dati della richiesta
        " :return: Risposta JSON con la cronologia della chat
        """

        chat_id = data.get('chat_id')
        if not chat_id:
            return jsonify({"error": "un chat_id è necessario per accedere alla storia"}), 400
        
        if chat_id in self.active_chats:
            chat = self.active_chats[chat_id]
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
    
    def handle_admin_list_chats(self):
        """ Recupera la cronologia completa di tutte le chat attive
        "   :return: Risposta JSON con la cronologia completa
        """
        
        full_history = []
        for chat_id, chat in self.active_chats.items():
            for message in chat.history:
                full_history.append({
                    "chat_id": chat_id,
                    "role": message.role,
                    "content": message.parts[0].text
                })
        
        return jsonify({
            "full-history": full_history,
            "success": True
        })
    
    def handle_admin_delete_chats(self):
        """  Cancella tutte le chat attive
        "    :return: Risposta JSON con l'esito dell'operazione
        """
        
        # Log cancellazione chat
        self.logger.log_info("DELETING ALL ACTIVE CHATS")
        
        # Azzera il dizionario delle chat attive
        self.active_chats.clear()
        return jsonify({"success": True})
