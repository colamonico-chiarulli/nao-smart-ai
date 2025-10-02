"""
File:	/tests/test_main.py
-----
Test API NAO gemini
-----
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright	(c)2024 Rino Andriano
Created Date: Saturday, November 9th 2024, 6:37:29 pm
-----
Last Modified: 	October 6th 2025 4:50:00 pm
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
------------------------------------------------------------------------------
"""

import requests
import json
import re
import os
from dotenv import load_dotenv


class ChatTester:
    def __init__(self):
        # Imposta l'URL del servizio web API dal file .env
        # Assicurati che il file .env sia nella cartella web_api     
        current_dir = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(current_dir, "..", "web_api", ".env")
        load_dotenv(dotenv_path)
        self.API_URL = os.getenv("WEB_API_URL")
        self.chat_id = None

    def send_message(self, message):
        """
        Invia un messaggio al servizio di chat e ritorna la risposta
        """
        try:
            # Prepara il payload
            payload = {"action": "talk", "message": message}

            # Aggiunge chat_id se esiste una conversazione in corso
            if self.chat_id:
                payload["chat_id"] = self.chat_id

            # Invia la richiesta
            response = requests.post(
                self.API_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10,
            )

            if response.status_code == 200:
                response_data = response.json()

                # Salva il chat_id se è una nuova conversazione
                if not self.chat_id:
                    self.chat_id = response_data.get("chat_id")

                return response_data.get("response")
            else:
                return f"Errore: Status code {response.status_code}"

        except requests.exceptions.RequestException as e:
            return f"Errore di connessione: {str(e)}"

    def end_chat(self):
        """
        Termina la sessione di chat corrente
        """
        if self.chat_id:
            try:
                response = requests.post(
                    self.API_URL, json={"action": "end", "chat_id": self.chat_id}
                )
                return response.status_code == 200
            except requests.exceptions.RequestException:
                return False
        return True


def main():
    print("=== Test Client per Web Service Chat ===")
    print("Scrivi 'exit' per terminare la chat")
    print("=====================================")

    chat = ChatTester()
    
    # Decodifica eventuali sequenze Unicode escape letterali (es. \u00e0 -> à)
    # Usa re.sub per trovare e sostituire le sequenze \uXXXX
    def decode_unicode_escape(match):
        return chr(int(match.group(1), 16))

    try:
        while True:
            # Leggi input dell'utente
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
                # Formatta il JSON e lo stampa in modo leggibile 
                # rimuovendo le sequenze Unicode escape
                pretty_json = json.dumps(response, indent=2)
                pretty_json = re.sub(r'\\u([0-9a-fA-F]{4})', decode_unicode_escape, pretty_json)
                print("\nBot > " + pretty_json)

    except KeyboardInterrupt:
        print("\n\nInterruzione da tastiera. Chiusura in corso...")
        chat.end_chat()
    except Exception as e:
        print(f"\nErrore imprevisto: {str(e)}")
        chat.end_chat()


if __name__ == "__main__":
    main()
