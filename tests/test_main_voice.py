"""
File:    tests/test_main_voice.py
-----
Test interattivo della rotta POST /chat/voice
Consente input testuale, lo converte in audio WAV (16000 Hz) tramite gTTS + ffmpeg
e lo invia all'API simulando una conversazione vocale.
-----
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@license https://www.gnu.org/licenses/agpl-3.0.html AGPL 3.0
"""

import requests
import json
import os
import sys
import tempfile
import subprocess
from dotenv import load_dotenv

class VoiceChatTester:
    def __init__(self):
        # Imposta l'URL del servizio web API dal file .env
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(current_dir, "..", "web_api", ".env")
        load_dotenv(dotenv_path)
        base_url = os.getenv("WEB_API_URL", "http://127.0.0.1:5000").rstrip("/")
        self.API_URL_VOICE = f"{base_url}/chat/voice"
        self.API_URL_CHAT = f"{base_url}/chat"
        self.chat_id = None

    def generate_tts_wav(self, text: str, lang: str = "it") -> str:
        """
        Genera un file WAV a 16000Hz monocanale da testo usando gTTS + ffmpeg.
        """
        try:
            from gtts import gTTS
        except ImportError:
            print("\n[ERRORE] gTTS non è installato. Installa con:")
            print("         pip install gtts")
            sys.exit(1)

        print(f"\n[TTS] Generazione audio in corso... ({lang})")

        tmp_mp3 = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
        tmp_wav = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        tmp_mp3.close()
        tmp_wav.close()

        try:
            # 1. gTTS -> MP3
            tts = gTTS(text=text, lang=lang, slow=False)
            tts.save(tmp_mp3.name)

            # 2. ffmpeg -> WAV 16000 Hz 1 ch
            result = subprocess.run(
                [
                    "ffmpeg", "-y",
                    "-v", "error", # Riduce l'output non necessario di ffmpeg
                    "-i", tmp_mp3.name,
                    "-ac", "1",
                    "-ar", "16000",
                    tmp_wav.name,
                ],
                capture_output=True,
                text=True,
            )

            if result.returncode != 0:
                print(f"\n[ERRORE] ffmpeg ha restituito un errore:\n{result.stderr}")
                sys.exit(1)

            print(f"[TTS] File WAV temporaneo generato: {tmp_wav.name}")
            return tmp_wav.name

        finally:
            if os.path.exists(tmp_mp3.name):
                os.unlink(tmp_mp3.name)

    def send_message(self, message):
        """
        Trasforma il testo in WAV, lo invia alla rotta /chat/voice e ritorna la risposta.
        """
        wav_path = self.generate_tts_wav(message)

        try:
            form_data = {}
            if self.chat_id:
                form_data["chat_id"] = self.chat_id

            file_name = os.path.basename(wav_path)
            
            print("[INFO] Invio file audio al server...")
            with open(wav_path, "rb") as audio_file:
                files = {
                    "audio": (file_name, audio_file, "audio/wav")
                }

                response = requests.post(
                    self.API_URL_VOICE,
                    files=files,
                    data=form_data,
                    timeout=60,
                )

            if response.status_code == 200:
                response_data = response.json()

                # Salva il chat_id se è una nuova conversazione
                if not self.chat_id and "chat_id" in response_data:
                    self.chat_id = response_data["chat_id"]

                return response_data
            else:
                return {
                    "error": f"Status code {response.status_code}", 
                    "details": response.text
                }

        except requests.exceptions.RequestException as e:
            return {"error": f"Errore di connessione: {str(e)}"}
        finally:
            # Pulisce il file WAV temporaneo
            if os.path.exists(wav_path):
                os.unlink(wav_path)

    def end_chat(self):
        """
        Termina la sessione di chat corrente tramite la rotta /chat.
        """
        if self.chat_id:
            try:
                response = requests.post(
                    self.API_URL_CHAT, json={"action": "end", "chat_id": self.chat_id}
                )
                return response.status_code == 200
            except requests.exceptions.RequestException:
                return False
        return True


def main():
    print("=== Test Client per Web Service Chat Voice (TTS -> WAV 16kHz) ===")
    print("Scrivi 'exit' per terminare la chat")
    print("==================================================================")

    chat = VoiceChatTester()

    try:
        while True:
            # Leggi input testuale dell'utente
            user_input = input("\nTu > ").strip()

            # Gestisci comando di uscita
            if user_input.lower() == "exit":
                if chat.end_chat():
                    print("\nChat terminata correttamente")
                else:
                    print("\nErrore durante la chiusura della chat")
                break

            # Invia messaggio e mostra risposta
            if user_input:
                response = chat.send_message(user_input)
                
                # Formatta e stampa la risposta dal server vocale
                # Mostriamo la trascrizione (se presente) e la risposta LLM
                print("\n=== Risposta Server ===")
                
                if "transcription" in response:
                    print(f"Trascrizione riconosciuta:")
                    print(f"  > \"{response['transcription']}\"")
                
                print("\nJSON Response completo:")
                print(json.dumps(response, indent=2, ensure_ascii=False))

    except KeyboardInterrupt:
        print("\n\nInterruzione da tastiera. Chiusura in corso...")
        chat.end_chat()
    except Exception as e:
        print(f"\nErrore imprevisto: {str(e)}")
        chat.end_chat()


if __name__ == "__main__":
    main()
