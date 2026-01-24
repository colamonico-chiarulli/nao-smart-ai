"""
File:    /nao-client/nao-stt-client-fast.py
-----
@author  Nuccio Gargano <v.gargano@colamonicochiarulli.edu.it>
@copyright    (c)2025 Nuccio Gargano
Created Date: Friday, October 10th 2025, 18:30:00 pm
-----
Last Modified: 	 January 22nd 2026 7:00:00 pm
Modified By:     Rino Andriano <andriano@colamonicochiarulli.edu.it>
-----
@license    https://www.gnu.org/licenses/agpl-3.0.html AGPL 3.0

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

import time
import threading
import struct

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.memory = None
        self.audio_recorder = None
        self.is_recording = False
        self.audio_file_path = "/tmp/temp_audio.ogg" # Changed to OGG
        # Per registrare tutti i microfoni NAO occorre usare 48 kHz
        # (cfr. doc 2.8: http://doc.aldebaran.com/2-8/naoqi/audio/alaudiorecorder-api.html)
        self.record_sample_rate = 16000 # OGG encoder on NAO handles resampling usually, or we can try 16k directly if supported for OGG
        # Note: NAO 6 supports OGG recording. 
        #Canali di registrazione (microfoni)
        self.channel_mask = [1, 1, 1, 1] 

        self.post_silence_seconds = 0.8
        self.listen_off_time = None
        self.last_speech_time = None
        self.stop_lock = threading.Lock()
        self.tts = None
        self.max_tts_wait_seconds = 4.0
        self.tts_state_event = "Gemini/TtsSpeaking"
        self.tts_event_available = False
        self.tts_is_speaking = False
        self.last_tts_finished_time = None
        self.tts_post_buffer_seconds = 0.35

        self.api_url = self.getParameter("api_url")
        if not self.api_url or self.api_url.strip() == "":
            self.api_url = "http://127.0.0.1:5000/chat/voice" # Default to NEW UNIFIED route

        self.recording_start_time = None
        self.speech_detected_time = None
        self.prebuffer_seconds = 0.8
        self.chat_id = None # Maintain chat_id session


    def onLoad(self):
        """Inizializzazione del box"""
        try:
            self.memory = self.session().service("ALMemory")
            self.audio_recorder = self.session().service("ALAudioRecorder")
            self.speech_recognition = self.session().service("ALSpeechRecognition")
            try:
                self.memory.subscribeToEvent(
                    self.tts_state_event,
                    self.getName(),
                    "onTtsStateChanged"
                )
                self.tts_event_available = True
            except Exception as e:
                self.tts_event_available = False
                self.logger.warning("Impossibile sottoscrivere evento stato TTS: " + str(e))
            try:
                self.tts = self.session().service("ALTextToSpeech")
            except Exception as e:
                self.tts = None
                self.logger.warning("Impossibile ottenere ALTextToSpeech: " + str(e))

        except Exception as e:
            self.logger.error("Errore in onLoad: " + str(e))

    def onUnload(self):
        """Pulizia prima della chiusura"""
        try:
            if self.memory:
                self.memory.unsubscribeToEvent(
                    "ALSpeechRecognition/Status",
                    self.getName()
                )
                if self.tts_event_available:
                    try:
                        self.memory.unsubscribeToEvent(
                            self.tts_state_event,
                            self.getName()
                        )
                    except Exception as e:
                        self.logger.debug("Errore unsubscribe stato TTS: " + str(e))
                    finally:
                        self.tts_event_available = False
            if self.audio_recorder:
                try:
                    self.audio_recorder.stopMicrophonesRecording()
                except:
                    pass
            self.is_recording = False
        except Exception as e:
            self.logger.error("Errore in onUnload: " + str(e))

    def onInput_onStart(self):
        """Attiva l'intercettazione degli eventi di riconoscimento vocale"""
        try:
            self.memory.subscribeToEvent(
                "ALSpeechRecognition/Status",
                self.getName(),
                "onSpeechRecognitionStatus"
            )

        except Exception as e:
            self.logger.error("Errore sottoscrizione evento: " + str(e))

    def onSpeechRecognitionStatus(self, key, value, message):
        """Callback per gli eventi di riconoscimento vocale"""
        self.logger.info("STATO RICONOSCIMENTO: " + str(value))

        # Registra solo se AI è attiva
        if value == "ListenOn":
            self.start_recording()

        elif value == "SpeechDetected":
            self.mark_speech_detected()

        elif value == "ListenOff":
            self.listen_off_time = time.time()

        elif value == "EndOfProcess":
            self.handle_end_of_process()

    def start_recording(self):
        """Inizia registrazione e segna il tempo di inizio"""
        try:
            self.wait_for_robot_to_finish_speaking()

            if self.is_recording:
                self.logger.warning("Registrazione già attiva, forzo stop")
                try:
                    self.audio_recorder.stopMicrophonesRecording()
                except:
                    pass
                self.is_recording = False

            # Resetta i tempi di riferimento
            self.recording_start_time = time.time()
            self.speech_detected_time = None
            self.last_speech_time = None
            self.listen_off_time = None

            # Avvia registrazione in OGG
            # NAO 6 supports "ogg" format natively
            self.audio_recorder.startMicrophonesRecording(
                self.audio_file_path,
                "ogg",
                self.record_sample_rate,
                self.channel_mask
            )
            self.is_recording = True
        except Exception as e:
            self.logger.error("Errore avvio registrazione: " + str(e))
            self.is_recording = False

    def mark_speech_detected(self):
        """Segna il momento in cui viene rilevato il parlato"""
        if self.is_recording and self.speech_detected_time is None:
            self.speech_detected_time = time.time()
        if self.is_recording:
            self.last_speech_time = time.time()

    def stop_recording(self):
        """Ferma la registrazione audio"""
        with self.stop_lock:
            if not self.is_recording:
                return
            try:
                self.audio_recorder.stopMicrophonesRecording()
            except Exception as e:
                self.logger.error("Errore stop registrazione: " + str(e))
            finally:
                self.is_recording = False
                self.listen_off_time = None

    def handle_end_of_process(self):
        """Gestisce la chiusura applicando un buffer di silenzio"""
        try:
            was_recording = self.is_recording
            if self.is_recording:
                wait_seconds = 0.0
                now = time.time()

                if self.last_speech_time:
                    elapsed = now - self.last_speech_time
                    if elapsed < self.post_silence_seconds:
                        wait_seconds = self.post_silence_seconds - elapsed
                elif self.listen_off_time:
                    elapsed = now - self.listen_off_time
                    if elapsed < self.post_silence_seconds:
                        wait_seconds = self.post_silence_seconds - elapsed

                if wait_seconds > 0:
                    time.sleep(wait_seconds)

                self.stop_recording()

            if was_recording:
                self.trim_by_timing_and_send()

        except Exception as e:
            self.logger.error("Errore handle_end_of_process: " + str(e))
            self.onTranscriptionFailed()

    def trim_by_timing_and_send(self):
        """
        In questa versione FAST, saltiamo il trim locale (complesso con OGG su Python 2.7)
        e inviamo tutto al server.
        """
        try:
            import os

            if not os.path.exists(self.audio_file_path):
                # self.logger.error("File audio non trovato")
                # self.onTranscriptionFailed()
                return

            # Skip trim logic entirely for OGG/Fast mode
            self.logger.info("Modalità FAST: invio audio senza trim locale")
            self.send_audio_to_stt()

        except Exception as e:
            self.logger.error("Errore trim_by_timing: " + str(e))
            self.onTranscriptionFailed()

    def is_robot_speaking(self):
        """Verifica se il TTS del robot è ancora in corso"""
        if not self.tts:
            return False
        try:
            return bool(self.tts.isSpeaking())
        except Exception as e:
            self.logger.warning("Errore verifica stato TTS: " + str(e))
            return False

    def wait_for_robot_to_finish_speaking(self):
        """Attende che il robot termini di parlare prima di registrare"""
        if self.wait_for_tts_event_clearance():
            return

        if not self.is_robot_speaking():
            return

        self.logger.info("Robot sta parlando, attendo prima di registrare (fallback)")
        start_wait = time.time()
        while self.is_robot_speaking():
            if time.time() - start_wait > self.max_tts_wait_seconds:
                self.logger.warning("Timeout attesa TTS, avvio comunque registrazione")
                break
            time.sleep(0.05)

    def onTtsStateChanged(self, key, value, message):
        """Callback ALMemory per lo stato TTS pubblicato dal blocco AI"""
        try:
            is_speaking = bool(value)
            self.tts_is_speaking = is_speaking
            if not is_speaking:
                self.last_tts_finished_time = time.time()
        except Exception as e:
            self.logger.warning("Errore gestione evento stato TTS: " + str(e))

    def wait_for_tts_event_clearance(self):
        """Utilizza l'evento ALMemory per garantire il buffer post-parlato"""
        if not self.tts_event_available:
            return False

        start_wait = time.time()
        while self.tts_is_speaking:
            if time.time() - start_wait > self.max_tts_wait_seconds:
                self.logger.warning("Timeout evento TTS, procedo con la registrazione")
                break
            time.sleep(0.05)

        if self.last_tts_finished_time:
            elapsed = time.time() - self.last_tts_finished_time
            if elapsed < self.tts_post_buffer_seconds:
                time.sleep(self.tts_post_buffer_seconds - elapsed)

        return True

    def send_audio_to_stt(self):
        """Invia l'audio al server STT esterno e recupera la trascrizione"""
        try:
            import os

            if not os.path.exists(self.audio_file_path):
                self.logger.error("File audio non trovato")
                self.onTranscriptionFailed()
                return

            file_size = os.path.getsize(self.audio_file_path)
            if file_size < 100:
                self.logger.warning("File audio troppo piccolo: " + str(file_size) + " bytes")
                self.onTranscriptionFailed()
                return

            self.logger.info("Invio audio OGG al server STT FAST: " + str(file_size) + " bytes")

            try:
                import requests as req_module

                # Leggi file audio
                with open(self.audio_file_path, 'rb') as audio_file:
                    files_data = {'audio': ('audio.ogg', audio_file, 'audio/ogg')}
                    data_payload = {}
                    if self.chat_id:
                        data_payload['chat_id'] = self.chat_id

                    # Invia al server
                    response = req_module.post(
                        self.api_url,
                        files=files_data,
                        data=data_payload,
                        timeout=15
                    )

                if response.status_code == 200:
                    result = response.json()

                    if result.get('success'):
                        # 1. Update Session Info
                        if 'chat_id' in result:
                            self.chat_id = result['chat_id']
                        
                        # 2. Check for Unified Response (New Flow)
                        if 'response' in result:
                            self.logger.info("Ricevuta risposta diretta AI")
                            if self.memory:
                                # Serialize full response for ALMemory
                                import json
                                self.memory.raiseEvent("Gemini/DirectResponse", json.dumps(result))
                            else:
                                self.logger.error("ALMemory non disponibile per DirectResponse")

                        # 3. Check for Transcription (Old Flow or logging)
                        # Even in new flow, we might want to log user text
                        transcription = result.get('transcription', result.get('text', '')).strip()
                        
                        if transcription:
                             # If NO response key was present, we MUST trigger the old signal
                             # to keep backward compatibility with old server boxes
                             if 'response' not in result:
                                 self.onTranscriptionReady(str(transcription))
                             else:
                                 self.logger.info("Utente ha detto: " + str(transcription))
                        else:
                             if 'response' not in result:
                                 self.logger.warning("Trascrizione vuota")
                                 self.onTranscriptionFailed()

                    else:
                        error_msg = result.get('error', 'Errore sconosciuto')
                        self.logger.warning("Errore API: " + str(error_msg))
                        self.onTranscriptionFailed()

                else:
                    self.logger.error("Errore HTTP: " + str(response.status_code))
                    self.onTranscriptionFailed()

            except Exception as e:
                import sys
                exc_type, exc_value, exc_traceback = sys.exc_info()
                self.logger.error("Tipo errore: " + str(exc_type))
                self.logger.error("Dettaglio: " + str(exc_value))
                self.onTranscriptionFailed()

        except Exception as e:
            self.logger.error("Errore generico esterno: " + str(e))
            self.onTranscriptionFailed()

    def onInput_onStop(self):
        """Ferma il box"""
        self.onUnload()
        self.onStopped()
