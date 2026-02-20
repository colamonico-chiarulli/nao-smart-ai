"""
File:	/web_api/utils/llm_chat_api.py
-----
Classe LLMChatAPI - per gestire le interazioni API con vari LLM tramite LiteLLM
Le diverse azioni sono specificate nel campo action del JSON inviato.
/gemini/chat  azioni: talk, end, hystory
/gemini/admin azioni: list-chats, delete-chats
------
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright (C) 2024-2026 Rino Andriano, Vito Trifone Gargano
Created Date: Wednesday, November 20th 2024, 6:37:29 pm
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

import os
import json
import re
import importlib
import random
from dotenv import load_dotenv
from litellm import completion
import litellm
from utils.cleantext import clean_text
from utils.cleantext import clean_markdown
from ai_prompts.system_prompt import SYSTEM_PROMPT_BASE
from ai_prompts.technical_prompt import TECHNICAL_INSTRUCTIONS
from ai_prompts.system_prompt import create_response_schema
from ai_prompts.system_prompt import GENERATION_CONFIG_BASE
from utils.chat_logger import ChatLogger
from utils.fix_movements import fix_animation
from flask import jsonify

#Personalità di default in caso di errori
ERROR_PERSONALITY = "Sei un robot sociale amichevole"

class LLMChatAPI:
    """
    Classe per gestire le interazioni API con vari LLM tramite LiteLLM
    """

    def __init__(self, logs_dir="logs"):
        """Inizializza l'API per la gestione delle chat con LLM
        Args: logs_dir -> Directory per i log delle chat
        """
        # Logger interno alla classe
        self.logger = ChatLogger(logs_dir)

        # Carica le variabili d'ambiente
        self._load_environment()

        # Configura il modello LLM
        self.llm_model = os.getenv("LLM_MODEL", "gemini/gemini-2.0-flash")
        
        # Gestione API Key Rotation
        self.api_keys = self._load_api_keys()
        self.current_key_index = 0
        
        # Recupera i movimenti e le azioni del robot dai file movements.json e actions.json
        movements_list = self._get_movements_from_file()
        # Carica la Mappa Azioni ---
        self.actions_map = self._get_actions_map_from_file()
        # Estrae solo le CHIAVI (es. ACT_DANCE_MACARENA_FLOOR) per lo schema dell'AI
        actions_keys_list = list(self.actions_map.keys())
        
        # Crea lo schema usando le chiavi (utile per il prompt di sistema)
        self.response_schema = create_response_schema(movements_list, actions_keys_list)
        
        # Configura le SYSTEM_INSTRUCTION 
        # AGPL Section 7(b) Protected Attribution - DO NOT MODIFY
        personality = self._load_ai_personality()
        self.system_instruction = SYSTEM_PROMPT_BASE + personality
        
        # Dizionario per memorizzare le chat attive
        # Struttura: {chat_id: [{"role": "user", "content": "..."}, ...]}
        self.active_chats = {}

        # Dizionario per memorizzare le personalità personalizzate per ogni chat
        # Formato: {chat_id: personality_name}
        self.chat_personalities = {}

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
        
    def _get_actions_map_from_file(self):
        """Legge la mappa delle azioni dal file actions_map.json"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            actions_path = os.path.join(current_dir, "actions_map.json")

            if not os.path.exists(actions_path):
                self.logger.log_error(f"File actions_map.json non trovato: {actions_path}")
                return {}

            with open(actions_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Restituisce il dizionario completo { "ACT_...": "path/..." }
                return data
                
        except json.JSONDecodeError as e:
            self.logger.log_error(f"Errore nel parsing JSON di actions_map.json: {e}")
            return {}
        except Exception as e:
            self.logger.log_error(f"Errore nel caricamento della actions map: {e}")
            return {}

    def _get_technical_instructions(self):
        """Genera le istruzioni tecniche formattate con la lista delle azioni"""
        # Prepara la lista delle azioni per il prompt
        actions_list_str = "\n".join(f"- {key}" for key in self.actions_map.keys())
        
        # Completa istruzioni tecniche iniettando la lista delle chiavi delle action
        # Usa replace perché il testo contiene JSON con parentesi graffe
        return TECHNICAL_INSTRUCTIONS.replace("{actions_list}", actions_list_str)

    def _load_ai_personality(self):
        """Carica la personalità del robot AI dal file .env"""
        config_file = os.getenv('DEFAULT_PROMPT_AI', "ai_prompts.example_system")
        
        personality = ERROR_PERSONALITY
        if config_file:
            try:
                config_module = importlib.import_module(config_file)
                loaded_personality = getattr(config_module, 'AI_PERSONALITY', None)
                if loaded_personality:
                    personality = loaded_personality
                else:
                    self.logger.log_warning(f"AI_PERSONALITY non trovata in '{config_file}'")
            except ImportError as e:
                self.logger.log_error(f"File di configurazione '{config_file}' non trovato: {e}")
            except Exception as e:
                self.logger.log_error(f"Errore nel caricamento della personalità AI: {e}")
        
        # FUSIONE: Unisce la personalità (caricata o default) con le istruzioni tecniche formattate
        # Questo avviene SEMPRE, garantendo che le technical instructions siano presenti
        full_personality = personality + "\n" + self._get_technical_instructions()
        return full_personality

    def _get_available_personalities(self):
        """
        Scansiona la cartella ai_prompts per trovare tutte le personalità disponibili
        Returns:
            list: Lista di nomi di personalità disponibili (senza suffisso _system)
        """
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            prompts_dir = os.path.join(current_dir, "..", "ai_prompts")

            if not os.path.exists(prompts_dir):
                self.logger.log_error(f"Cartella ai_prompts non trovata: {prompts_dir}")
                return []

            personalities = []
            for filename in os.listdir(prompts_dir):
                if filename.endswith("_system.py") and filename != "system_prompt.py":
                    # Rimuove "_system.py" dal nome file
                    personality_name = filename[:-10]  # len("_system.py") = 10
                    personalities.append(personality_name)

            return sorted(personalities)

        except Exception as e:
            self.logger.log_error(f"Errore nella scansione delle personalità: {e}")
            return []

    def _load_personality_by_name(self, personality_name):
        """
        Carica una personalità specifica dal nome
        Args:
            personality_name: Nome della personalità (senza _system)
        Returns:
            str: Testo della personalità o ERROR_PERSONALITY in caso di errore
        """
        module_name = f"ai_prompts.{personality_name}_system"

        try:
            config_module = importlib.import_module(module_name)
            personality = getattr(config_module, 'AI_PERSONALITY', None)

            if personality is None:
                self.logger.log_warning(f"AI_PERSONALITY non trovata in '{module_name}'")
                return ERROR_PERSONALITY
            
            # FUSIONE: Unisce la personalità specifica con le istruzioni tecniche formattate
            return personality + "\n" + self._get_technical_instructions()

        except ImportError as e:
            self.logger.log_error(f"Modulo personalità '{module_name}' non trovato: {e}")
            return None
        except Exception as e:
            self.logger.log_error(f"Errore nel caricamento personalità '{personality_name}': {e}")
            return None

    def _load_api_keys(self):
        """
        Carica le API keys dal file .env supportando chiavi multiple separate da virgola
        """
        # Determina quale variabile cercare in base al modello
        if "openrouter" in self.llm_model:
            env_var = "OPENROUTER_API_KEY"
        elif "gemini" in self.llm_model:
            env_var = "GOOGLE_API_KEY" # o GEMINI_API_KEY
        elif "gpt" in self.llm_model:
            env_var = "OPENAI_API_KEY"
        elif "claude" in self.llm_model:
            env_var = "ANTHROPIC_API_KEY"
        else:
            # Default fallback
            env_var = "OPENROUTER_API_KEY"
            
        keys_string = os.getenv(env_var, "")
        if not keys_string:
            self.logger.log_warning(f"Nessuna API Key trovata per {env_var}")
            return []
            
        # Divide per virgola e pulisce gli spazi
        keys = [k.strip() for k in keys_string.split(',') if k.strip()]
        self.logger.log_info(f"Caricate {len(keys)} API keys per {env_var}")
        return keys

    def _get_next_api_key(self):
        """Restituisce la prossima API key disponibile (Round Robin)"""
        if not self.api_keys:
            return None
            
        key = self.api_keys[self.current_key_index]
        # Aggiorna l'indice per la prossima chiamata
        self.current_key_index = (self.current_key_index + 1) % len(self.api_keys)
        return key

    def _load_environment(self):
        """Carica le variabili d'ambiente dai file .env"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(current_dir, "..", ".env")

        if os.path.exists(dotenv_path):
            load_dotenv(dotenv_path)
        else:
            # Prova a caricare dal percorso corrente
            load_dotenv()

    def _process_model_response(self, response_text, chat_id):
        """Processa la risposta del modello estraendo e processando i chunks
        Args: 
            response_text -> La risposta testuale dal modello (stringa JSON)
            chat_id  -> ID della chat corrente
        Returns: 
            Tuple (success, result) dove result è il dizionario con i chunks o il messaggio di errore
        """
        try:
            # Rimuove eventuali blocchi di codice Markdown dal JSON generato da LLM
            cleaned_json_string = clean_markdown(response_text)
            # Esegui il parsing del JSON sulla stringa pulita
            response_data = json.loads(cleaned_json_string)
            
            chunks = response_data.get("chunks", [])
            
            # --- TRADUZIONE AZIONE ---
            raw_action_key = response_data.get("action") 
            final_action_path = ""

            # Se la chiave esiste ed è diversa da NO_ACTION
            if raw_action_key and raw_action_key != "NO_ACTION":
                if raw_action_key in self.actions_map:
                    final_action_path = self.actions_map[raw_action_key]
                    self.logger.log_info(f"Azione mappata: {raw_action_key} -> {final_action_path}")
                else:
                    self.logger.log_warning(f"Chiave sconosciuta: {raw_action_key}")
            
            if not chunks:
                self.logger.log_warning("Risposta del modello senza chunks")
            
            # Processa ogni chunk
            for chunk in chunks:
                text_content = chunk.get("text", "")
                cleaned_response = clean_text(text_content)
                self.logger.log_chat_message(chat_id, "model", cleaned_response)
                chunk["text"] = cleaned_response
                chunk["movements"] = [fix_animation(mov) for mov in chunk.get("movements", [])]
            
            # Costruisce il risultato finale includendo l'azione se esiste
            result = {"chunks": chunks}
            if final_action_path:
                result["action"] = final_action_path

            return True, result
     
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

    def _detect_personality_change_command(self, message):
        """
        Rileva se il messaggio è un comando di cambio personalità
        Richiede sempre il prefisso "Comando di sistema" seguito da varianti linguistiche
        """
        # Lista di pattern supportati (tutti richiedono "comando di sistema" come prefisso)
        patterns = [
            r"comando\s+di\s+sistema\s+ora\s+sarai\s+(\w+)",                    # Originale
            r"switch\s+t[ou]\s+(\w+)",                                          # switch to
            r"abracadabra\s+diventa\s+(\w+)",                                   # abracadabra diventa
            r"magia magia\s+diventa\s+(\w+)",                                   # magia magia diventa
            r"comando\s+di\s+sistema\s+diventa\s+(\w+)",                        # "diventa X"
            r"comando\s+di\s+sistema\s+comportati\s+(?:come|da)\s+(\w+)",       # "comportati come/da X"
            r"comando\s+di\s+sistema\s+cambia\s+personalit[aà]\s+(?:in|a)\s+(\w+)",  # "cambia personalità in/a X"
            r"comando\s+di\s+sistema\s+ora\s+sei\s+(\w+)",                      # "ora sei X"
            r"comando\s+di\s+sistema\s+attiva\s+(?:la\s+)?personalit[aà]\s+(\w+)",   # "attiva (la) personalità X"
            r"comando\s+di\s+sistema\s+passa\s+(?:a|alla)\s+modalit[aà]\s+(\w+)",    # "passa a/alla modalità X"
        ]

        message_lower = message.lower()

        # Prova ogni pattern in ordine
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                personality_name = match.group(1)
                return True, personality_name

        return False, None

    def _change_chat_personality(self, chat_id, personality_name):
        """
        Cambia la personalità per una chat specifica e resetta lo storico
        Args:
            chat_id: ID della chat
            personality_name: Nome della personalità da attivare
        Returns:
            tuple: (success, message) con l'esito dell'operazione
        """
        # Verifica che la personalità esista
        available_personalities = self._get_available_personalities()

        if personality_name not in available_personalities:
            self.logger.log_warning(
                f"[PERSONALITY] Tentativo di cambio a personalità inesistente: {personality_name}"
            )
            return False, f"ERRORE cambio personalità non riuscito! Personalità '{personality_name}' non trovata. Disponibili: {', '.join(available_personalities)}"

        # Carica la personalità
        personality_text = self._load_personality_by_name(personality_name)

        if personality_text is None:
            return False, f"ERRORE cambio personalità non riuscito! Impossibile caricare '{personality_name}'"

        # Salva la personalità per questa chat
        self.chat_personalities[chat_id] = personality_name

        # RESET DELLO STORICO: Cancella la cronologia conversazione per evitare conflitti
        if chat_id in self.active_chats:
            old_history_length = len(self.active_chats[chat_id])
            self.active_chats[chat_id] = []
            self.logger.log_info(
                f"[PERSONALITY] Chat {chat_id}: Storico resettato ({old_history_length} messaggi cancellati)"
            )

        # Log del cambio
        self.logger.log_info(
            f"[PERSONALITY] Chat {chat_id}: Cambio personalità a '{personality_name}'"
        )

        return True, f"OK cambio personalità effettuato in {personality_name}"

    def _get_system_instruction_for_chat(self, chat_id):
        """
        Recupera la system instruction per una chat specifica
        """
        if chat_id in self.chat_personalities:
            personality_name = self.chat_personalities[chat_id]
            personality_text = self._load_personality_by_name(personality_name)

            if personality_text:
                return SYSTEM_PROMPT_BASE + personality_text
        
        return self.system_instruction

    def handle_talk_action(self, data):
        """Gestisce l'azione di conversazione (talk)
        Args:
            data -> Dizionario contenente chat_id e message
        Returns:
            Tuple (response_json, status_code, timing_ms) se TIMING_ENABLED
            Tuple (response_json, status_code) altrimenti
        """
        # Estrai e valida input
        chat_id = data.get("chat_id")
        message = data.get("message", "").strip()

        if not message:
            # ORIGINALE: ), 400
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

            # *** DETECTION COMANDO DI SISTEMA PER CAMBIO PERSONALITA ***
            is_personality_command, personality_name = self._detect_personality_change_command(message)

            if is_personality_command:
                # Gestisce il cambio personalità (include reset storico)
                success, response_message = self._change_chat_personality(chat_id, personality_name)

                # IMPORTANTE: Riassegna chat_history dopo il reset per evitare riferimenti obsoleti
                chat_history = self.active_chats[chat_id]

                # Crea una risposta sintetica in formato chunk
                if success:
                    chunks = [{
                        "text": response_message,
                        "movements": ["animations/Stand/Gestures/Yes_1"]
                    }]
                else:
                    chunks = [{
                        "text": response_message,
                        "movements": ["animations/Stand/Gestures/No_1"]
                    }]

                # Log della risposta sistema
                self.logger.log_info(f"[PERSONALITY] Risposta: {response_message}")

                # ORIGINALE: }), 200
                return jsonify({
                    "chat_id": chat_id,
                    "response": {"chunks": chunks},
                    "success": True,
                    "personality_changed": success
                }), 200

            # Recupera la system instruction corretta
            system_instruction = self._get_system_instruction_for_chat(chat_id)
            
            # Costruiamo il messaggio utente
            current_user_message = {"role": "user", "content": message}

            # Limita la history PASSATA agli ultimi 20 messaggi (10 scambi)
            # Facciamo lo slice PRIMA per garantire che il messaggio corrente sia sempre incluso
            max_past_messages = 20
            past_history_limited = chat_history[-max_past_messages:]
            
            # Prepara i messaggi per LiteLLM (System + Past History + Current Message)
            messages = [{"role": "system", "content": system_instruction}] + past_history_limited + [current_user_message]

            # Aggiungi il messaggio dell'utente alla cronologia COMPLETA (persistenza)
            chat_history.append(current_user_message)
            
            # Invia il messaggio usando LiteLLM
            try:
                # Ottieni la chiave per questa richiesta
                current_api_key = self._get_next_api_key()
                
                response = completion(
                    model=self.llm_model,
                    messages=messages,
                    api_key=current_api_key, # Passa esplicitamente la chiave ruotata
                    response_format={"type": "json_object"}, # Forza output JSON
                    temperature=GENERATION_CONFIG_BASE["temperature"],
                    top_p=GENERATION_CONFIG_BASE["top_p"],
                    max_tokens=GENERATION_CONFIG_BASE["max_output_tokens"]
                )
            except Exception as e:
                self.logger.log_error(f"DEBUG: LiteLLM Error Details: {e}")
                import traceback
                traceback.print_exc()
                raise e                      
            response_text = response.choices[0].message.content
            
            # Aggiunge la risposta del modello alla cronologia
            chat_history.append({"role": "assistant", "content": response_text})
            
            # Processa la risposta
            success, result = self._process_model_response(response_text, chat_id)
            
            if success:
                # ORIGINALE: }), 200
                return jsonify({
                    "chat_id": chat_id,
                    "response": result,
                    "success": True
                }), 200
            else:
                # ORIGINALE: }), result["status_code"]
                return jsonify({
                    "error": result["error"],
                    "success": False
                }), result["status_code"]
                
        except Exception as e:
            self.logger.log_error(f"Errore nella gestione della chat: {str(e)}")
            # ORIGINALE: }), 500
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
            # La history è già nel formato corretto [{"role":..., "content":...}]
            return jsonify({
                "chat_id": chat_id,
                "history": chat_history,
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
                full_history.append({
                    "chat_id": chat_id,
                    "role": message["role"],
                    "content": message["content"],
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
