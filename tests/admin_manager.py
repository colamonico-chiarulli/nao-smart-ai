"""
File:	/tests/admin_manager.py
-----
Script per testare e gestire le rotte admin del server NAO Smart AI.
Può essere usato da riga di comando o in modalità interattiva.
------
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright (C) 2024-2026 Rino Andriano, Vito Trifone Gargano
Created Date: Wednesday, November 20th 2024, 6:37:29 pm
-----
Last Modified: 	February 26th 2026, 10:24:00 pm
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
import sys
import json
import urllib.request
import urllib.error

# Tenta di caricare le variabili d'ambiente con python-dotenv
try:
    from dotenv import load_dotenv
    # Cerca il file .env nella directory web_api, o nella radice come fallback
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    web_api_env = os.path.join(base_dir, 'web_api', '.env')
    root_env = os.path.join(base_dir, '.env')
    
    if os.path.exists(web_api_env):
        load_dotenv(web_api_env)
    elif os.path.exists(root_env):
        load_dotenv(root_env)
    else:
        load_dotenv()
except ImportError:
    pass

admin_token_env = os.getenv("ADMIN_TOKEN", "")

# Recupera la base URL per le Web API dal file .env (valore predefinito: http://localhost:3030)
base_api_url = os.getenv("WEB_API_URL", "http://localhost:3030")
DEFAULT_URL = f"{base_api_url.rstrip('/')}/admin" if not base_api_url.endswith("/admin") else base_api_url

def send_admin_request(action, chat_id=None, token=None, url=DEFAULT_URL):
    """
    Invia la richiesta POST all'endpoint /admin
    """
    if not token:
        print("\n[!] Errore: Token admin non fornito. Impostalo nel file .env usando la variabile ADMIN_TOKEN.")
        return False
        
    full_url = f"{url}?token={token}"
    
    payload = {"action": action}
    if chat_id:
        payload["chat_id"] = chat_id
        
    data = json.dumps(payload).encode('utf-8')
    headers = {'Content-Type': 'application/json'}
    
    req = urllib.request.Request(full_url, data=data, headers=headers, method='POST')
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode('utf-8'))
            print("\n[+] Successo!")
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return True
            
    except urllib.error.HTTPError as e:
        print(f"\n[-] Errore HTTP: {e.code} ({e.reason})")
        try:
            err_result = json.loads(e.read().decode('utf-8'))
            print(json.dumps(err_result, indent=2, ensure_ascii=False))
        except:
            print(e.read().decode('utf-8'))
        return False
        
    except urllib.error.URLError as e:
        print(f"\n[-] Impossibile connettersi a {url}")
        print(f"[-] Dettagli errore: {e.reason}")
        print("[-] Il server è in esecuzione?")
        return False
        
    except Exception as e:
        print(f"\n[-] Errore imprevisto: {e}")
        return False

def interactive_mode(token, url):
    """
    Avvia la modalità interattiva con menu testuale
    """
    print("====================================")
    print(" NAO Smart AI Server - Admin Client ")
    print("====================================")
    print(f"URL endpoint: {url}")
    print(f"Token admin:  {'[CONFIGURATO]' if token else '[MANCANTE]'}")
    print("====================================\n")
    
    while True:
        print("Azioni disponibili:")
        print("  1. list-chats   - Elenca tutte le chat attive dal server")
        print("  2. history      - Mostra la cronologia completa di una chat")
        print("  3. delete-chats - Cancella tutte le chat in memoria sul server")
        print("  0. Esci")
        
        scelta = input("\nScegli un'opzione: ").strip()
        
        if scelta == "1":
            print("\nEsecuzione 'list-chats'...")
            send_admin_request("list-chats", token=token, url=url)
            
        elif scelta == "2":
            chat_id = input("Inserisci l'ID della chat: ").strip()
            if chat_id:
                print(f"\nEsecuzione 'history' per chat '{chat_id}'...")
                send_admin_request("history", chat_id=chat_id, token=token, url=url)
            else:
                print("[-] ID chat non valido, operazione annullata.")
                
        elif scelta == "3":
            conferma = input("\nATTENZIONE: Questa azione rimuoverà permanentemente tutte le sessioni.\nSei sicuro di voler cancellare tutte le chat? (s/N): ").strip().lower()
            if conferma in ['s', 'si', 'y', 'yes']:
                print("\nEsecuzione 'delete-chats'...")
                send_admin_request("delete-chats", token=token, url=url)
            else:
                print("Operazione annullata.")
                
        elif scelta == "0":
            print("\nUscita dall'Admin Client.")
            break
            
        else:
            print("[-] Scelta non valida. Inserisci un numero da 0 a 3.")
        
        print("\n" + "-"*50 + "\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Script per testare le rotte /admin di NAO Smart AI Server")
    parser.add_argument("action", nargs="?", choices=["list-chats", "delete-chats", "history"], 
                        help="Azione da eseguire. Se omesso, avvia la modalità interattiva")
    parser.add_argument("--chat-id", help="ID della chat (richiesto da riga di comando per l'azione 'history')")
    parser.add_argument("--token", default=admin_token_env, help="Token admin (di default letto da .env)")
    parser.add_argument("--url", default=DEFAULT_URL, help=f"URL endpoint admin (default: {DEFAULT_URL})")
    
    args = parser.parse_args()
    
    if args.action:
        # Modalità a riga di comando singola (CLI)
        if args.action == "history" and not args.chat_id:
            parser.error("L'azione 'history' richiede l'argomento aggiuntivo --chat-id")
        send_admin_request(args.action, chat_id=args.chat_id, token=args.token, url=args.url)
    else:
        # Modalità interattiva (menu GUI testuale)
        try:
            interactive_mode(args.token, args.url)
        except KeyboardInterrupt:
            print("\nUscita forzata dal client.")
            sys.exit(0)
