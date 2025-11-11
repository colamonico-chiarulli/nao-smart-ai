"""
File:	/nao-client/nao-smart-ai-client.py
-----
@author  Nuccio Gargano <v.gargano@colamonicochiarulli.edu.it>
@copyright	(c)2025 Nuccio Gargano
Created Date: Friday, October 10th 2025, 18:30:00 pm
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

1. Any interactive user interface must preserve the original author 
   attribution when the AI is asked about its creators
2. System prompts containing author information cannot be modified
3. The robot must always identify its original creators as specified 
   in the source code
------------------------------------------------------------------------------
"""

class MyClass(GeneratedClass):
    def __init__(self):
        GeneratedClass.__init__(self)
        self.memory = None
        self.audio_recorder = None
        self.is_recording = False
        self.audio_file_path = "/tmp/temp_audio.wav"

        self.api_url = self.getParameter("api_url")
        if not self.api_url or self.api_url.strip() == "":
            self.api_url = "http://127.0.0.1:5000/stt/vosk"

        self.recording_start_time = None
        self.speech_detected_time = None
        self.prebuffer_seconds = 0.8  

    def onLoad(self):
        """Inizializzazione del box"""
        try:
            self.memory = self.session().service("ALMemory")
            self.audio_recorder = self.session().service("ALAudioRecorder")
            self.speech_recognition = self.session().service("ALSpeechRecognition")

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
            self.stop_recording()

        elif value == "EndOfProcess":
            self.trim_by_timing_and_send()

    def start_recording(self):
        """Inizia registrazione e segna il tempo di inizio"""
        try:
            if self.is_recording:
                self.logger.warning("Registrazione già attiva, forzo stop")
                try:
                    self.audio_recorder.stopMicrophonesRecording()
                except:
                    pass
                self.is_recording = False

            # Resetta i tempi
            self.recording_start_time = time.time()
            self.speech_detected_time = None

            # Avvia registrazione
            self.audio_recorder.startMicrophonesRecording(
                self.audio_file_path,
                "wav",
                16000,
                [0, 0, 1, 0]
            )
            self.is_recording = True
        except Exception as e:
            self.logger.error("Errore avvio registrazione: " + str(e))
            self.is_recording = False

    def mark_speech_detected(self):
        """Segna il momento in cui viene rilevato il parlato"""
        if self.is_recording and self.speech_detected_time is None:
            self.speech_detected_time = time.time()
            elapsed = self.speech_detected_time - self.recording_start_time

    def stop_recording(self):
        """Ferma la registrazione audio"""
        if self.is_recording:
            try:
                recording_end_time = time.time()
                total_duration = recording_end_time - self.recording_start_time

                self.audio_recorder.stopMicrophonesRecording()
                self.is_recording = False

            except Exception as e:
                self.logger.error("Errore stop registrazione: " + str(e))

    def trim_by_timing_and_send(self):
        """Taglia il silenzio iniziale basandosi sui timestamp"""
        try:
            import os

            if not os.path.exists(self.audio_file_path):
                self.logger.error("File audio non trovato")
                self.onTranscriptionFailed()
                return

            if self.recording_start_time is None:
                self.logger.warning("Tempo di inizio registrazione non disponibile")
                # Invia senza tagliare
                self.send_audio_to_stt()
                return

            if self.speech_detected_time is None:
                self.logger.warning("SpeechDetected non ricevuto, invio tutto l'audio")
                self.send_audio_to_stt()
                return

            silence_duration = self.speech_detected_time - self.recording_start_time
            cut_start_seconds = max(0, silence_duration - self.prebuffer_seconds)

            if self.trim_audio_by_time(self.audio_file_path, cut_start_seconds):
                self.send_audio_to_stt()
            else:
                self.logger.warning("Trim fallito, invio audio originale")
                self.send_audio_to_stt()

        except Exception as e:
            self.logger.error("Errore trim_by_timing: " + str(e))
            self.onTranscriptionFailed()

    def trim_audio_by_time(self, audio_path, start_seconds):
        """Taglia l'audio dal secondo start_seconds in poi"""
        try:
            import wave
            import array
            import os

            wf = wave.open(audio_path, 'rb')
            params = wf.getparams()
            sample_rate = wf.getframerate()
            frames = wf.readframes(wf.getnframes())
            wf.close()

            audio_data = array.array('h', frames)
            original_samples = len(audio_data)
            original_duration = float(original_samples) / sample_rate

            start_sample = int(start_seconds * sample_rate)

            if start_sample >= original_samples:
                self.logger.warning("Punto di taglio oltre la fine del file")
                return False

            if start_sample < 100:
                self.logger.info("Taglio troppo piccolo, mantengo tutto")
                return True


            trimmed_data = audio_data[start_sample:]
            trimmed_samples = len(trimmed_data)
            trimmed_duration = float(trimmed_samples) / sample_rate

            wf_out = wave.open(audio_path, 'wb')
            wf_out.setparams(params)
            wf_out.writeframes(trimmed_data.tostring())
            wf_out.close()

            reduction_percent = int((1.0 - float(trimmed_samples) / original_samples) * 100)

            return True

        except Exception as e:
            self.logger.error("Errore trim_audio_by_time: " + str(e))
            return False

    def send_audio_to_stt(self):
        """Invia l'audio al server STT esterno e recupera la trascrizione"""
        try:
            import os

            if not os.path.exists(self.audio_file_path):
                self.logger.error("File audio non trovato")
                self.onTranscriptionFailed()
                return

            file_size = os.path.getsize(self.audio_file_path)
            if file_size < 1000:
                self.logger.warning("File audio troppo piccolo: " + str(file_size) + " bytes")
                self.onTranscriptionFailed()
                return

            self.logger.info("Invio audio al server STT: " + str(file_size) + " bytes")

            try:
                import requests as req_module 

                # Leggi file audio
                with open(self.audio_file_path, 'rb') as audio_file:
                    files_data = {'audio': ('audio.wav', audio_file, 'audio/wav')}

                    # Invia al server STT
                    response = req_module.post(
                        self.api_url,
                        files=files_data,
                        timeout=10
                    )

                if response.status_code == 200:
                    result = response.json()

                    if result.get('success'):
                        transcription = result.get('text', '').strip()

                        if transcription:
                            self.onTranscriptionReady(str(transcription))
                        else:
                            self.logger.warning("Trascrizione vuota")
                            self.onTranscriptionFailed()
                    else:
                        error_msg = result.get('error', 'Errore sconosciuto')
                        self.logger.warning("STT fallito: " + str(error_msg))
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