"""
File:	/web_api/utils/gemini_chat_api.py
-----
Classe GeminiChatAPI - per gestire le interazioni API con il modello Gemini
Le diverse azioni sono specificate nel campo action del JSON inviato.
/gemini/chat  azioni: talk, end, hystory
/gemini/admin azioni: list-chats, delete-chats
------
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright	(c)2024 Rino Andriano
Created Date: Wednesday, November 20th 2024, 6:37:29 pm
-----
Last Modified: 	October 02nd 2025 07:01:00 pm
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

1. Any interactive user interface must preserve the original author 
   attribution when the AI is asked about its creators
2. System prompts containing author information cannot be modified
3. The robot must always identify its original creators as specified 
   in the source code
------------------------------------------------------------------------------
"""

import os
import json
import importlib
from dotenv import load_dotenv
from google import genai
from google.genai import types

from utils.cleantext import clean_text
from utils.cleantext import clean_markdown
from ai_prompts.system_prompt import SYSTEM_PROMPT_BASE
from ai_prompts.system_prompt import create_response_schema
from ai_prompts.system_prompt import GENERATION_CONFIG_BASE
from utils.chat_logger import ChatLogger
from utils.fix_movements import fix_animation
from flask import jsonify

#Personalità di default in caso di errori
ERROR_PERSONALITY = "Sei un robot sociale amichevole"

class GeminiChatAPI:
    """
    Classe per gestire le interazioni API con il modello Gemini
    """

    def __init__(self, logs_dir="logs"):
        """Inizializza l'API per la gestione delle chat con Gemini
        Args: logs_dir -> Directory per i log delle chat
        """
        # Logger interno alla classe
        self.logger = ChatLogger(logs_dir)

        # Carica le variabili d'ambiente
        self._load_environment()

        # Configura Gemini con l'API key
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY non trovata nelle variabili d'ambiente")
        
        self.client = genai.Client(api_key=api_key)
        
        # Recupera i movimenti del robot dal file movements.json
        movements_list = self._get_movements_from_file()
        response_schema = create_response_schema(movements_list)
        
        # Configura le SYSTEM_INSTRUCTION 
        # AGPL Section 7(b) Protected Attribution - DO NOT MODIFY
        personality = self._load_ai_personality()
        self.system_instruction = SYSTEM_PROMPT_BASE + personality
        
        # Salva le safety settings
        self.safety_settings = self._get_safety_settings()
        
        # Crea la configurazione di generazione (centralizzata)
        self.generation_config = types.GenerateContentConfig(
            temperature=GENERATION_CONFIG_BASE["temperature"],
            top_p=GENERATION_CONFIG_BASE["top_p"],
            top_k=GENERATION_CONFIG_BASE["top_k"],
            max_output_tokens=GENERATION_CONFIG_BASE["max_output_tokens"],
            response_mime_type=GENERATION_CONFIG_BASE["response_mime_type"],
            response_schema=response_schema,
            system_instruction=self.system_instruction,
            safety_settings=self.safety_settings,
        )
                       
        # Dizionario per memorizzare le chat attive
        self.active_chats = {}
        
        #Carica il modello LLM da .ENV - se non esiste carica il default
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-2.0-flash")

    
    def _get_movements_from_file(self):
        """Legge i movements dal file movements.json"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            movements_path = os.path.join(current_dir, "movements.json")

            if not os.path.exists(movements_path):
                self.logger.log_error(f"File movements.json non trovato: {movements_path}")
                return []

            with open(movements_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                movements = data.get('movements_library', [])
                
            if not movements:
                self.logger.log_warning("movements_library vuoto o non trovato")
                
            return movements
            
        except json.JSONDecodeError as e:
            self.logger.log_error(f"Errore nel parsing JSON di movements.json: {e}")
            return []
        except Exception as e:
            self.logger.log_error(f"Errore nel caricamento dei movements: {e}")
            return []

    def _load_ai_personality(self):
        """Carica la personalità del robot AI dal file .env"""
        config_file = os.getenv('DEFAULT_PROMPT_AI', "ai_prompts.example_system")
        
        if not config_file:
            self.logger.log_warning("Nessuna configurazione AI specificata, uso default")
            return ERROR_PERSONALITY
        
        try:
            config_module = importlib.import_module(config_file)
            personality = getattr(config_module, 'AI_PERSONALITY', None)
            
            if personality is None:
                self.logger.log_warning(f"AI_PERSONALITY non trovata in '{config_file}'")
                personality = ERROR_PERSONALITY
                
            return personality
            
        except ImportError as e:
            self.logger.log_error(f"File di configurazione '{config_file}' non trovato: {e}")
            return ERROR_PERSONALITY
        except Exception as e:
            self.logger.log_error(f"Errore nel caricamento della personalità AI: {e}")
            return ERROR_PERSONALITY

    def _load_environment(self):
        """Carica le variabili d'ambiente dai file .env"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(current_dir, "..", ".env")
        
        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        else:
            # Prova a caricare dal percorso corrente
            load_dotenv()

    def _get_safety_settings(self):
        """Configurazione delle impostazioni di sicurezza per Gemini"""
        return [
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_ONLY_HIGH"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_ONLY_HIGH"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_ONLY_HIGH"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_ONLY_HIGH"
            ),
        ]

    def _process_model_response(self, response, chat_id):
        """Processa la risposta del modello estraendo e processando i chunks
        Args: 
            response -> La risposta dal modello Gemini
            chat_id  -> ID della chat corrente
        Returns: 
            Tuple (success, result) dove result è il dizionario con i chunks o il messaggio di errore
        """
        try:
            # Verifica che ci siano candidati
            if not response.candidates:
                self.logger.log_error("Risposta da Gemini senza candidati")
                return False, {
                    "error": "Risposta non valida dal modello: nessun candidato.",
                    "status_code": 500
                }
            
            # Ottieni il primo candidato valido
            first_candidate = response.candidates[0]
            
            # Verifica che il candidato abbia contenuto
            if not hasattr(first_candidate, 'content') or not first_candidate.content.parts:
                self.logger.log_error("Candidato senza contenuto valido")
                return False, {
                    "error": "Risposta non valida dal modello: contenuto mancante.",
                    "status_code": 500
                }
            
            response_text = first_candidate.content.parts[0].text
            
        except (AttributeError, IndexError) as e:
            self.logger.log_error(f"Struttura della risposta inattesa: {e}")
            return False, {
                "error": "Risposta non valida dal modello: struttura inattesa.",
                "status_code": 500
            }

        try:
            # Rimuove eventuali blocchi di codice Markdown dal JSON generato da LLM
            cleaned_json_string=clean_markdown(response_text)
            # Esegui il parsing del JSON sulla stringa pulita
            response_data = json.loads(cleaned_json_string)
            #self.logger.log_info(f"Debug JSON: {response_data}")
            chunks = response_data.get("chunks", [])
            
            if not chunks:
                self.logger.log_warning("Risposta del modello senza chunks")
            
            # Processa ogni chunk
            for chunk in chunks:
                text_content = chunk.get("text", "")
                cleaned_response = clean_text(text_content)
                self.logger.log_chat_message(chat_id, "model", cleaned_response)
                chunk["text"] = cleaned_response
                chunk["movements"] = [fix_animation(mov) for mov in chunk.get("movements", [])]
            
            return True, {"chunks": chunks}
     
        except json.JSONDecodeError as e:
            self.logger.log_error(f"Errore nel parsing JSON della risposta: {str(e)}")
            self.logger.log_error(f"Testo ricevuto: {response_text[:200]}...")
            return False, {
                "error": "Risposta del modello non valida (JSON non corretto).",
                "status_code": 500
            }
        except Exception as e:
            self.logger.log_error(f"Errore nel processamento della risposta: {str(e)}")
            return False, {
                "error": "Errore nel processamento della risposta del modello.",
                "status_code": 500
            }

    def handle_talk_action(self, data):
        """Gestisce l'azione di conversazione (talk)
        Args: 
            data -> Dizionario contenente chat_id e message
        Returns: 
            Risposta JSON con l'esito della conversazione
        """
        # Estrai e valida input
        chat_id = data.get("chat_id")
        message = data.get("message", "").strip()
        
        if not message:
            return jsonify(
                {"error": "Un messaggio è necessario per avviare la chat", "success": False}
            ), 400
        
        try:
            # Gestisce la chat (nuova o esistente)               
            if chat_id and chat_id in self.active_chats:
                chat_history = self.active_chats[chat_id]
                self.logger.log_info(f"Continuazione chat esistente: {chat_id}")
            else:
                chat_history = []
                chat_id = str(id(chat_history))
                self.active_chats[chat_id] = chat_history
                self.logger.log_info(f"Nuova chat creata: {chat_id}")
            
            # Log del messaggio in arrivo
            self.logger.log_chat_message(chat_id, "user", message)

            # Aggiungi il messaggio dell'utente alla cronologia
            user_message = types.Content(
                role="user",
                parts=[types.Part(text=message)]
            )
            chat_history.append(user_message)

            # Invia il messaggio usando la configurazione centralizzata
            response = self.client.models.generate_content(
                model=self.gemini_model,
                contents=chat_history,
                config=self.generation_config
            )
            
            # Aggiunge la risposta del modello alla cronologia
            if response.candidates and response.candidates[0].content:
                model_content = response.candidates[0].content
                chat_history.append(model_content)
            
            # Processa la risposta
            success, result = self._process_model_response(response, chat_id)
            
            if success:
                return jsonify({
                    "chat_id": chat_id,
                    "response": result,
                    "success": True
                }), 200
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
        Args: 
            data -> Dizionario contenente i dati della richiesta
        Returns: 
            Risposta JSON con l'esito della chiusura
        """
        chat_id = data.get("chat_id")
        if not chat_id:
            return jsonify(
                {"error": "chat_id è necessario per terminare una chat", "success": False}
            ), 400

        if chat_id in self.active_chats:
            # Log chiusura chat
            self.logger.log_info(f"CHAT_CLOSED: {chat_id}")
            del self.active_chats[chat_id]
            return jsonify({"message": "Chat chiusa correttamente", "success": True}), 200
        
        return jsonify({"error": "Chat non trovata", "success": False}), 404

    def handle_history_action(self, data):
        """Recupera la storia di una chat specifica
        Args: 
            data -> Dizionario contenente i dati della richiesta
        Returns: 
            Risposta JSON con la cronologia della chat
        """
        chat_id = data.get("chat_id")
        if not chat_id:
            return jsonify(
                {"error": "un chat_id è necessario per accedere alla storia", "success": False}
            ), 400

        if chat_id in self.active_chats:
            chat_history = self.active_chats[chat_id]
            history = []
            
            for message in chat_history:
                if hasattr(message, 'role') and hasattr(message, 'parts'):
                    # Gestisci messaggi con struttura corretta
                    text_content = ""
                    if message.parts and len(message.parts) > 0:
                        text_content = getattr(message.parts[0], 'text', '')
                    
                    history.append({
                        "role": message.role,
                        "content": text_content
                    })
            
            return jsonify({
                "chat_id": chat_id,
                "history": history,
                "success": True
            }), 200
        
        return jsonify({"error": "Chat non trovata", "success": False}), 404

    def handle_admin_list_chats(self):
        """Recupera la cronologia completa di tutte le chat attive
        Returns: 
            Risposta JSON con la cronologia completa
        """
        full_history = []
        
        for chat_id, chat_history in self.active_chats.items():
            for message in chat_history:
                if hasattr(message, 'role') and hasattr(message, 'parts'):
                    text_content = ""
                    if message.parts and len(message.parts) > 0:
                        text_content = getattr(message.parts[0], 'text', '')
                    
                    full_history.append({
                        "chat_id": chat_id,
                        "role": message.role,
                        "content": text_content,
                    })

        return jsonify({
            "full_history": full_history,
            "total_chats": len(self.active_chats),
            "success": True
        }), 200

    def handle_admin_delete_chats(self):
        """Cancella tutte le chat attive
        Returns: 
            Risposta JSON con l'esito dell'operazione
        """
        num_chats = len(self.active_chats)
        
        # Log cancellazione chat
        self.logger.log_info(f"DELETING ALL ACTIVE CHATS (Total: {num_chats})")

        # Azzera il dizionario delle chat attive
        self.active_chats.clear()
        
        return jsonify({
            "message": f"{num_chats} chat cancellate",
            "success": True
        }), 200
