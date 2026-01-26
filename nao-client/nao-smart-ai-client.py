"""
File:	/nao-client/nao-smart-ai-client.py
-----
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright	(c)2024 Rino Andriano
Created Date: Wednesday, June 4th 2024, 6:11:00 pm
-----
Last Modified: 	January 24th 2026
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

import requests
import json  # Importa il modulo json per la decodifica
import qi    # per gestire la funzione async
import random
import time

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.api_url = "https://YOUR_WEB_API_URL/chat"
        self.chat_id = None  
        self.unload_requested = False
        self.tts = ALProxy("ALTextToSpeech")
        self.animPlayer = ALProxy("ALAnimationPlayer")
        self.motion = ALProxy("ALMotion")
        self.posture = self.session().service("ALRobotPosture")
        self.dialog = ALProxy("ALDialog")
        self.speech_recognition = ALProxy("ALSpeechRecognition")
        self.memory = ALProxy("ALMemory")
        
        # --- Configurazione Legacy Integrata ---
        self.behavior_mng = ALProxy("ALBehaviorManager")
        self.tts_state_event = "Gemini/TtsSpeaking"
        self.bodytalk_prefix = "animations/Stand/BodyTalk/Speaking/BodyTalk_"
        self.bodytalk_poll_seconds = 0.1
        self.custom_actions = "customanimations/" # Path base per i behavior custom
        # ---------------------------------------

    def onLoad(self):
        self.unload_requested = False
        try:
            self.api_url = self.getParameter("api_url")
        except Exception:
            self.logger.warning("Parametro api_url non trovato o errore, uso default")

        try:
            self.memory.subscribeToEvent("Gemini/DirectResponse", self.getName(), "onDirectResponse")
            self.logger.info("Sottoscritto a Gemini/DirectResponse")
        except Exception as e:
            self.logger.warning("Impossibile sottoscrivere Gemini/DirectResponse: " + str(e))

        self.dialog.subscribe("my_subscribe")
        try:
            self.motion.setMoveArmsEnabled(True, True)
            self.motion.setExternalCollisionProtectionEnabled("All", True)
            self.publish_tts_state(False) # Reset stato iniziale
        except Exception as e:
            self.logger.warning("Errore nella configurazione del motion:"+ str(e))
        pass

    def onUnload(self):
        self.unload_requested = True
        self.stop_all_actions()
        try:
            self.dialog.unsubscribe("my_subscribe")
        except Exception:
            pass
        try:
            if self.memory:
                self.memory.unsubscribeToEvent("Gemini/DirectResponse", self.getName())
        except:
            pass
        pass

    def stop_all_actions(self):
        """Ferma tutte le attività correnti del robot"""
        try:
            if self.tts:
                self.tts.stopAll()
            # self.animPlayer.stopAll() # Metodo non esistente in alcune versioni
            if self.motion:
                self.motion.stopMove()
            if self.behavior_mng:
                self.behavior_mng.stopAllBehaviors()
            self.publish_tts_state(False) # Forza stato 0
        except Exception as e:
            self.logger.error("Errore durante stop_all_actions: " + str(e))

    def publish_tts_state(self, is_speaking):
        """Aggiorna ALMemory con lo stato del TTS (Sync STT)"""
        if not self.memory:
            return
        try:
            self.memory.raiseEvent(self.tts_state_event, 1 if is_speaking else 0)
        except Exception as e:
            self.logger.warning("Impossibile pubblicare stato TTS: " + str(e))

    """
    Processa la risposta dell'AI per NAO, eseguendo movimenti e pronunciando il testo.
    :param response: Dizionario contenente i chunk di risposta dell'AI
    """
    def process_ai_response(self, response):
        chunks = response.get('chunks', []) if isinstance(response, dict) else []
        
        # 1. Check Chunks existence (Legacy Logic)
        if not chunks:
            self.logger.warning("Risposta AI senza chunk, nulla da eseguire")
            return

        # 2. Process Chunks (Testo + Movimenti base)
        for chunk in chunks:
            if self.unload_requested:
                break
                
            # a. Avvio TTS (usando post.say per stabilità)
            tts_task_id = self.start_speaking_chunk(chunk)
            if tts_task_id is None:
                continue

            # b. Esecuzione movimenti associati al chunk
            self.execute_chunk_movements(tts_task_id, chunk.get('movements', []))
            
            # c. BodyTalk di riempimento se il testo è lungo
            self.play_bodytalk_until_speech_done(tts_task_id)
            
            # d. Attesa fine parlato
            while tts_task_id is not None and self.tts.isRunning(tts_task_id):
                if self.unload_requested:
                    self.tts.stopAll()
                    break
                time.sleep(self.bodytalk_poll_seconds)
            
            if not self.unload_requested:
                self.posture.goToPosture("Stand", 1.5)
        
        # 3. Process Action (Behavior complessi)
        action_val = response.get('action')
        # Filtra azioni vuote o generiche se necessario
        if action_val and action_val not in ["", "none", "null"] and not self.unload_requested:
            self.logger.info("Richiesta azione: " + str(action_val))
            
            # Costruzione path completo (logica legacy)
            fullpath_action = str(self.custom_actions + action_val)
            
            try:
                # Verifica esistenza behavior prima di lanciarlo (Safety)
                if self.behavior_mng.isBehaviorPresent(fullpath_action):
                    self.motion.stopMove() # Ferma movimenti precedenti
                    self.logger.info("Esecuzione behavior: " + fullpath_action)
                    self.behavior_mng.runBehavior(fullpath_action)
                else:
                    # Tenta di eseguirlo come animazione semplice se non è un behavior complesso
                    self.logger.warning("Behavior non trovato, tento come animazione semplice: " + str(action_val))
                    self.animPlayer.run(str(action_val))
                    
            except Exception as e:
                self.logger.error("Errore nell'esecuzione dell'azione/behavior: " + str(e))


    def start_speaking_chunk(self, chunk):
        """Avvia il TTS per il chunk e restituisce il taskId (non Future)"""
        text = str(chunk.get('text', '')) if isinstance(chunk, dict) else ''
        if not text:
            return None
        try:
            self.publish_tts_state(True)
            # USIAMO post.say INVECE DI qi.async PER STABILITÀ
            return self.tts.post.say(text)
        except Exception as e:
            self.logger.error("Errore nella pronuncia " + str(e))
            return None

    def execute_chunk_movements(self, tts_task_id, movements):
        """Esegue le animazioni principali finché il TTS è attivo"""
        if not movements:
            return
            
        for movimento in movements:
            # Controllo se il tts sta ancora parlando e se non è stato richiesto unload
            if (tts_task_id is not None and not self.tts.isRunning(tts_task_id)) or self.unload_requested:
                break
                
            # Salta movimenti "Laugh" se il tts ha finito (logica legacy preservata opzionalmente, qui semplificata)
            
            try:
                # Per le animazioni usiamo ancora qi.async per non bloccare il thread principale
                # che deve controllare lo stato del TTS
                movement_future = qi.async(self.animPlayer.run, str(movimento))
                
                # Loop di attesa fine movimento o fine parlato
                while movement_future.isRunning():
                    if (tts_task_id is not None and not self.tts.isRunning(tts_task_id)) or self.unload_requested:
                        # Se il parlato finisce, lasciamo finire l'animazione corrente o la interrompiamo?
                        # La logica legacy interrompeva.
                        # self.animPlayer.stopAll() # Rimosso per bug noto, lasciamo finire o usiamo motion.stopMove() se critico
                        break
                    time.sleep(self.bodytalk_poll_seconds)
                    
            except Exception as e:
                self.logger.error("Errore nell'esecuzione del movimento " + str(e))
                continue

    def play_bodytalk_until_speech_done(self, tts_task_id):
        """Lancia micro-animazioni random finché il TTS è attivo"""
        filler_future = None
        
        while tts_task_id is not None and self.tts.isRunning(tts_task_id):
            if self.unload_requested:
                break
                
            if not filler_future or not filler_future.isRunning():
                mov_speaking = self.bodytalk_prefix + str(random.randint(1, 22))
                try:
                    filler_future = qi.async(self.animPlayer.run, mov_speaking)
                except Exception as e:
                    # self.logger.error("Errore BodyTalk: " + str(e)) # Log ridondante
                    filler_future = None
                    time.sleep(self.bodytalk_poll_seconds)
                    continue
            
            time.sleep(self.bodytalk_poll_seconds)
        
        # Alla fine del parlato aggiorno lo stato
        self.publish_tts_state(False)

    '''
    '' Invia un messaggio al servizio di chat e ritorna la risposta
    '''
    def send_message(self, message):
        try:
            # Prepara il payload
            payload = {
                "action": "talk",
                "message": message
            }

            # Aggiunge chat_id se esiste una conversazione in corso
            if self.chat_id:
                payload["chat_id"] = self.chat_id

            # Invia la richiesta
            response = requests.post(
                self.api_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            # Controlla lo status della risposta
            if response.status_code == 200:
                response_data = response.json()
                # Salva il chat_id se presente nella risposta
                if "chat_id" in response_data:
                    self.chat_id = response_data["chat_id"]
                    try:
                         self.memory.insertData("Gemini/ChatId", str(self.chat_id))
                    except:
                         pass
                    self.logger.info("Chat ID salvato: " + str(self.chat_id))
                # Ritorna la risposta
                return response_data.get("response")

            else:
                return {"response": "Errore: response status:" + str(response.status_code)}

        except requests.exceptions.RequestException as e:
            self.logger.error("Errore di connessione: " + str(e))
            return {"response": "Errore di connessione: " + str(e)}

    """
    "" Termina la sessione di chat corrente
    """
    def end_chat(self):
        if self.chat_id:
            try:
                response = requests.post(
                    self.api_url,
                    json={
                        "action": "end",
                        "chat_id": self.chat_id
                    }
                )
                self.chat_id=None
                try:
                     self.memory.insertData("Gemini/ChatId", "")
                except:
                     pass
                return True
            except requests.exceptions.RequestException:
                return False
        return True

    def disable_hearing(self):
        # Disattiva il TAG Gemini nel Dialog Colamonico
        self.dialog.deactivateTag("localAudio", "smart_ai_online")
        # Disabilita l'ascolto durante la risposta
        self.speech_recognition.pause(True)
        # Disattiva i segnali visivi dell'ascolto
        self.speech_recognition.setAudioExpression(False)
        self.speech_recognition.setVisualExpression(False)
        self.publish_tts_state(True)

    def enable_hearing(self):
        # Riabilita l'ascolto
        self.speech_recognition.pause(False)
        # Attiva i segnali visivi dell'ascolto
        self.speech_recognition.setAudioExpression(True)
        self.speech_recognition.setVisualExpression(True)
        # Riattiva il topic geminiAI
        self.dialog.activateTag("localAudio", "smart_ai_online")
        self.memory.insertData("gemini", 1)
        self.publish_tts_state(False)

    def onInput_domanda(self, domanda):
        #Viene scartato audio non compreso
        if domanda in ["<...>", "audio locale", "audio online", "audio fast"]:
            return
        try:
            # Chiama API Gemini e recupera la risposta
            response_data = self.send_message(domanda)

            self.disable_hearing()
            #Pronuncia il testo della risposta AI e i relativi movimanti
            self.process_ai_response(response_data)
            
            # Pausa di sicurezza per evitare auto-ascolto dell'eco
            time.sleep(1.0)
            
            self.enable_hearing()


        except Exception as e:
            self.logger.error("Errore in onInput_domanda: " + str(e))
            self.tts.say('Adesso non posso risponderti. Sono confuso!')
            self.onStopped()

    def onDirectResponse(self, key, value, message):
        """Callback per risposta diretta ricevuta via ALMemory (Fast Track)"""
        try:
            self.logger.info("Ricevuta DirectResponse da ALMemory")
            if not value:
                return

            import json
            # Value è una stringa JSON
            data = json.loads(value)
            
            # Se è presente chat_id, aggiorniamolo
            if 'chat_id' in data:
                self.chat_id = data['chat_id']
                try:
                     self.memory.insertData("Gemini/ChatId", str(self.chat_id))
                except:
                     pass

            response_payload = data.get('response')
            if response_payload:
                self.disable_hearing()
                self.process_ai_response(response_payload)
                self.enable_hearing()
            else:
                self.logger.warning("DirectResponse senza payload response")

        except Exception as e:
            self.logger.error("Errore in onDirectResponse: " + str(e))
            self.tts.say('Errore nella risposta diretta.')

    def onInput_cambio(self):
        """Gestisce il cambio di argomento: resetta solo la sessione"""
        if self.end_chat():
            self.logger.info("Chat reset on user request (topic change)")
            # Nessuna azione fisica o verbale di stop qui, come richiesto

    def onInput_onStop(self):
        """Gestisce lo stop dell'esecuzione"""
        self.onUnload()
        self.onStopped()