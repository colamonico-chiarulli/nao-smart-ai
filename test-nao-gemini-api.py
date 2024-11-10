import requests
#import json
#import sys

class ChatTester:
    def __init__(self):
        YOUR_URL= "https://YOUR_SERVER_URL:PORT/chat"
        self.API_URL = YOUR_URL
        self.chat_id = None
        
    def send_message(self, message):
        """
        Invia un messaggio al servizio di chat e ritorna la risposta
        """
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
                self.API_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            print (response)
            
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
                    self.API_URL,
                    json={
                        "action": "end",
                        "chat_id": self.chat_id
                    }
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
    
    try:
        while True:
            # Leggi input dell'utente
            user_input = input("\nTu > ").strip()
            
            # Gestisci comando di uscita
            if user_input.lower() == 'exit':
                if chat.end_chat():
                    print("\nChat terminata correttamente")
                else:
                    print("\nErrore durante la chiusura della chat")
                break
                
            # Invia messaggio e mostra risposta
            if user_input:
                response = chat.send_message(user_input)
                print(f"\nBot > {response}")
            
    except KeyboardInterrupt:
        print("\n\nInterruzione da tastiera. Chiusura in corso...")
        chat.end_chat()
    except Exception as e:
        print(f"\nErrore imprevisto: {str(e)}")
        chat.end_chat()

if __name__ == "__main__":
    main()
