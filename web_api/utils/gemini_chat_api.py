"""
File:	/web_api/utils/gemini_chat_api.py
-----
Classe GeminiChatAPI - per gestire le interazioni API con il modello Gemini
Le diverse azioni sono specificate nel campo action del JSON inviato.
/gemini/chat  azioni: talk, end, hystory
/gemini/admin azioni: list-chats, delete-chats
------
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright (C) 2024-2026 Rino Andriano, Vito Trifone Gargano
Created Date: Wednesday, November 20th 2024, 6:37:29 pm
-----
Last Modified: 	January 16th 2025 6:01:11 pm
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

import os
from dotenv import load_dotenv
import google.generativeai as genai

from google.generativeai.types import HarmCategory, HarmBlockThreshold
from utils.cleantext import clean_text
from ai_prompts.system_prompt import SYSTEM_PROMPT_BASE
#from ai_prompts.system_prompt import SYSTEM_INSTRUCTION
from ai_prompts.system_prompt import GENERATION_CONFIG
from utils.chat_logger import ChatLogger
from utils.fix_movements import fix_animation
from flask import jsonify
import json
import importlib


# Crea la variabile 


class GeminiChatAPI:
    """
    " Classe per gestire le interazioni API con il modello Gemini
    """

    def __init__(self, logs_dir="logs"):
        """Inizializza l'API per la gestione delle chat con Gemini
        "  Args: logs_dir -> Directory per i log delle chat
        """
        # Logger interno alla classe
        self.logger = ChatLogger(logs_dir)

        # Carica le variabili d'ambiente
        self._load_environment()

        # Configura Gemini con l'API key
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        #Recupera i movimenti del robot dal file movements.json e li configura per il prompt AI
        movements_list = self._get_movements_from_file()      
        GENERATION_CONFIG["response_schema"].properties["chunks"].items.properties["movements"].items.enum = movements_list
  
        # Configura le SYSTEM_INSTRUCTION 
        # AGPL Section 7(b) Protected Attribution - DO NOT MODIFY
        personality = self._load_ai_personality()
        SYSTEM_INSTRUCTION = SYSTEM_PROMPT_BASE + personality
        
        # Inizializza il modello Gemini
        self.model = genai.GenerativeModel(
            model_name="gemini-2.0-flash",
            generation_config=GENERATION_CONFIG,
            system_instruction=SYSTEM_INSTRUCTION,
            safety_settings=self._get_safety_settings(),
        )
        
        # Dizionario per memorizzare le chat attive
        self.active_chats = {}
    
    def _get_movements_from_file(self):
        """Legge i movements dal file movements.json"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            movements_path = os.path.join(current_dir, "movements.json")

            with open(movements_path, 'r') as file:
                movements = json.load(file)['movements_library']
            return movements
        except Exception as e:
            print(f"Errore nel parsing dei movements: {e}")
            return []

    def _load_ai_personality(self):
        """Carica la personalità del robot Ai dal file .env"""
        config_file = os.getenv('DEFAULT_PROMPT_AI', "ai_prompts/example_system.py")
        
        if not config_file:
            return "Nessuna configurazione specificata"
        
        try:
            config_module = importlib.import_module(config_file)
            return getattr(config_module, 'AI_PERSONALITY', 'Personalità non trovata')
        except ImportError:
            return f"File di configurazione '{config_file}' non trovato"
        except AttributeError:
            return f"Variabile 'AI_PERSONALITY' non trovata in '{config_file}'"

    def _load_environment(self):
        """Carica le variabili d'ambiente dai file .env"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(current_dir, "..", ".env")
        load_dotenv(dotenv_path)

    def _get_safety_settings(self):
        """Configurazione delle impostazioni di sicurezza per Gemini"""
        return {
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_ONLY_HIGH,
        }

    def _process_model_response(self, response, chat_id):
        """Processa la risposta del modello estraendo e processando i chunks
        "    Args: response -> La risposta dal modello Gemini
        "          chat_id  -> ID della chat corrente
        " Returns: Tuple (success, result) dove result è il dizionario con i chunks o il messaggio di errore
        """
        try:
            # Ottieni il primo candidato (risposta) valido/a
            first_candidate = next(
                candidate for candidate in response.candidates
                if hasattr(candidate, 'content') and candidate.content.parts
            )
            response_text = first_candidate.content.parts[0].text
            
        except StopIteration:
            self.logger.log_error("Risposta da Gemini senza candidati validi.")
            return False, {
                "error": "Risposta non valida dal modello: nessun candidato valido.",
                "status_code": 500
            }
            
        except AttributeError:
            self.logger.log_error("Struttura della risposta di Gemini inattesa.")
            return False, {
                "error": "Risposta non valida dal modello: struttura inattesa.",
                "status_code": 500
            }

        try:
            # Parsing e processamento dei chunks
            response_data = json.loads(response_text)
            chunks = response_data.get("chunks", [])
            
            # Processa ogni chunk
            for chunk in chunks:
                cleaned_response = clean_text(chunk["text"])
                self.logger.log_chat_message(chat_id, "model", cleaned_response)
                chunk["text"] = cleaned_response
                chunk["movements"] = [fix_animation(mov) for mov in chunk.get("movements", [])]
            
            return True, {"chunks": chunks}
            
        except json.JSONDecodeError as e:
            self.logger.log_error(f"Errore nel parsing JSON: {str(e)}")
            return False, {
                "error": "Risposta del modello non valida (JSON non corretto).",
                "status_code": 500
            }

    def handle_talk_action(self, data):
        """Gestisce l'azione di conversazione (talk)
        "    Args: data -> Dizionario contenente chat_id e message
        " Returns: Risposta JSON con l'esito della conversazione
        """
        # Estrai e valida input
        chat_id = data.get("chat_id")
        message = data.get("message")
        
        if not message:
            return jsonify(
                {"error": "Un messaggio è necessario per avviare la chat"}
            ), 400
        
        try:
            # Gestisce la chat (nuova o esistente)
            if chat_id and chat_id in self.active_chats:
                chat = self.active_chats[chat_id]
            else:
                chat = self.model.start_chat()
                chat_id = str(id(chat))
                self.active_chats[chat_id] = chat
            
            # Log del messaggio in arrivo
            self.logger.log_chat_message(chat_id, "user", message)
            
            # Invia il messaggio e processa la risposta
            response = chat.send_message(message)
            success, result = self._process_model_response(response, chat_id)
            
            if success:
                return jsonify({
                    "chat_id": chat_id,
                    "response": result,
                    "success": True
                })
            else:
                return jsonify({
                    "error": result["error"],
                    "success": False
                }), result["status_code"]
                
        except Exception as e:
            self.logger.log_error(f"Errore nella gestione della chat: {str(e)}")
            return jsonify({
                "error": "Errore durante l'elaborazione della richiesta",
                "details": str(e),
                "success": False
            }), 500
            
    def handle_end_action(self, data):
        """Termina una chat specifica
        "   Args: data -> Dizionario contenente i dati della richiesta
        " Return: Risposta JSON con l'esito della chiusura
        """

        chat_id = data.get("chat_id")
        if not chat_id:
            return jsonify(
                {"error": "chat_id è necessaria per terminare una chat"}
            ), 400

        if chat_id in self.active_chats:
            # Log chiusura chat
            self.logger.log_info(f"CHAT_CLOSED: {chat_id}")
            del self.active_chats[chat_id]
            return jsonify({"message": "Chat chiusa correttamente", "success": True})
        return jsonify({"error": "Chat non trovata"}), 404

    def handle_history_action(self, data):
        """Recupera la storia di una chat specifica
        "   Args: data -> Dizionario contenente i dati della richiesta
        " Return: Risposta JSON con la cronologia della chat
        """

        chat_id = data.get("chat_id")
        if not chat_id:
            return jsonify(
                {"error": "un chat_id è necessario per accedere alla storia"}
            ), 400

        if chat_id in self.active_chats:
            chat = self.active_chats[chat_id]
            history = [
                {"role": message.role, "content": message.parts[0].text}
                for message in chat.history
            ]
            return jsonify({"chat_id": chat_id, "history": history, "success": True})
        return jsonify({"error": "Chat non trovata"}), 404

    def handle_admin_list_chats(self):
        """Recupera la cronologia completa di tutte le chat attive
        "   Return: Risposta JSON con la cronologia completa
        """

        full_history = []
        for chat_id, chat in self.active_chats.items():
            for message in chat.history:
                full_history.append(
                    {
                        "chat_id": chat_id,
                        "role": message.role,
                        "content": message.parts[0].text,
                    }
                )

        return jsonify({"full-history": full_history, "success": True})

    def handle_admin_delete_chats(self):
        """Cancella tutte le chat attive
        "    Return: Risposta JSON con l'esito dell'operazione
        """

        # Log cancellazione chat
        self.logger.log_info("DELETING ALL ACTIVE CHATS")

        # Azzera il dizionario delle chat attive
        self.active_chats.clear()
        return jsonify({"success": True})
