"""
File:	/nao-client/nao-smart-ai-client.py
-----
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright	(c)2024 Rino Andriano
Created Date: Wednesday, June 4th 2024, 6:11:00 pm
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
        self.tts = ALProxy("ALTextToSpeech")
        self.animPlayer = ALProxy("ALAnimationPlayer")
        self.motion = ALProxy("ALMotion")
        self.posture = self.session().service("ALRobotPosture")
        self.dialog = ALProxy("ALDialog")
        self.speech_recognition = ALProxy("ALSpeechRecognition")

    def onLoad(self):
        self.dialog.subscribe("my_subscribe")
        try:
            self.motion.setMoveArmsEnabled(True, True)
            self.motion.setExternalCollisionProtectionEnabled("All", True)

        except Exception as e:
            self.logger.warning("Errore nella configurazione del motion:"+ str(e))
        pass

    def onUnload(self):
        self.dialog.unsubscribe("my_subscribe")
        pass

    """
    Processa la risposta dell'AI per NAO, eseguendo movimenti e pronunciando il testo.
    :param response: Dizionario contenente i chunk di risposta dell'AI
    """
    def process_ai_response(self, response):
        # Scorrimento dei chunk
        for chunk in response['chunks']:
            # Pronuncia del testo associato
            try:
                speaking=qi.async(self.tts.say, str(chunk['text']))

            except Exception as e:
                self.logger.error("Errore nella pronuncia " + str(e))

            # Esecuzione dei movimenti associati al chunk
            for movimento in chunk['movements']:
                time.sleep(1)
                try:
                    # Riproduzione dell'animazione
                    self.animPlayer.run(str(movimento))

                except Exception as e:
                    self.logger.error("Errore nell'esecuzione del movimento" + str(e))

            while speaking.isRunning():
                mov_speaking='animations/Stand/BodyTalk/Speaking/BodyTalk_' + str(random.randint(1, 22))
                self.animPlayer.run(mov_speaking)
                time.sleep(0.5) #pausa 0.5 secondi

            self.posture.goToPosture("Stand", 1.0)

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

            if response.status_code == 200:
                response_data = response.json()
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
                return True
            except requests.exceptions.RequestException:
                return False
        return True

    def disable_hearing(self):
        # Disattiva il TAG Gemini nel Dialog Colamonico
        self.dialog.deactivateTag("gemini", "YOUR_TOPIC")
        # Disabilita l'ascolto durante la risposta
        self.speech_recognition.pause(True)
        # Disattiva i segnali visivi dell'ascolto
        self.speech_recognition.setAudioExpression(False)
        self.speech_recognition.setVisualExpression(False)

    def enable_hearing(self):
        # Riabilita l'ascolto
        self.speech_recognition.pause(False)
        # Attiva i segnali visivi dell'ascolto
        self.speech_recognition.setAudioExpression(True)
        self.speech_recognition.setVisualExpression(True)
        # Riattiva il topic geminiAI
        self.dialog.activateTag("gemini", "YOUR_TOPIC")

    def onInput_domanda(self, domanda):
        #Viene scartato audio non compreso
        if domanda =="<...>":
            return
        try:
            # Chiama API Gemini e recupera la risposta
            response_data = self.send_message(domanda)

            self.disable_hearing()
            #Pronuncia il testo della risposta AI e i relativi movimanti
            self.process_ai_response(response_data)
            self.enable_hearing()


        except Exception as e:
            self.logger.error("Errore in onInput_domanda: " + str(e))
            self.tts.say('Adesso non posso risponderti. Sono confuso!')
            self.onStopped()

    def onInput_cambio(self):
        """Gestisce il cambio di argomento"""
        if self.end_chat():
            if self.tts:
                self.tts.say('Ok. Cambiamo argomento!')
            self.logger.info("Chat chiusa correttamente")

    def onInput_onStop(self):
        """Gestisce lo stop dell'esecuzione"""
        self.onUnload()
        self.onStopped()