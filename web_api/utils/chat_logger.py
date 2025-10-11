"""
File:	/web_api/utils/chat_logger.py
-----
Class ChatLogger - Log per le Chat AI
-----
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright	(c)2024 Rino Andriano
Created Date: Wednesday, November 19th 2024, 6:37:29 pm
-----
Last Modified: 	October 10th 2025 8:01:11 pm
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
import sys
import logging
from datetime import datetime


class ChatLogger:
    def __init__(self, log_directory=None, log_level=logging.INFO):
        """
        Inizializza il logger per la chat
        Args:
            log_directory (str, optional): Directory per i file di log.
                Se None, usa la cartella 'logs' nella root del progetto (web_api/logs).
            log_level (int, optional): Livello di logging. Default è logging.INFO.
        """
        # Imposta la directory dei log nella root del progetto (web_api/logs)
        if log_directory is None:
            # Dalla cartella utils, risali di un livello per arrivare a web_api
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            log_directory = os.path.join(parent_dir, "logs")

        # Crea la directory se non esiste
        os.makedirs(log_directory, exist_ok=True)

        # Genera il nome del file di log con timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        log_file = os.path.join(log_directory, f"chat_log_{timestamp}.txt")

        # Configura il logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # Rimuove eventuali handler esistenti per evitare duplicazioni
        self.logger.handlers.clear()

        # Aggiungi un file handler con encoding UTF-8
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.logger.addHandler(file_handler)
        
        # Aggiungi un console handler per Windows
        # Se su Windows, usa encoding compatibile per la console
        if sys.platform == 'win32':
            try:
                # Prova a impostare UTF-8 per la console
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(
                    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
                )
                # Su Windows, gestisci gli errori di encoding
                console_handler.stream.reconfigure(encoding='utf-8', errors='replace')
                self.logger.addHandler(console_handler)
            except Exception:
                # Se fallisce, usa handler standard senza emoji
                console_handler = logging.StreamHandler(sys.stdout)
                console_handler.setFormatter(
                    logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
                )
                self.logger.addHandler(console_handler)

    def log_chat_message(self, chat_id, role, content):
        """
        Registra un messaggio di chat nel file di log
        Args:
            chat_id (str): Identificativo della chat
            role (str): Ruolo del mittente (es. 'user', 'assistant')
            content (str): Contenuto del messaggio
        """
        # Limita la lunghezza del contenuto a 2000 caratteri
        content_str = str(content)[:2000]
        log_entry = f"CHAT_ID: {chat_id} | ROLE: {role} | MSG: {content_str}"
        self.logger.info(log_entry)

    def log_info(self, info_message):
        """Registra un messaggio di informazione"""
        # Rimuovi emoji su Windows per evitare errori di encoding
        if sys.platform == 'win32':
            info_message = self._sanitize_windows_message(info_message)
        self.logger.info(info_message)

    def log_error(self, error_message):
        """Registra un messaggio di errore"""
        if sys.platform == 'win32':
            error_message = self._sanitize_windows_message(error_message)
        self.logger.error(error_message)

    def log_warning(self, warning_message):
        """Registra un messaggio di warning"""
        if sys.platform == 'win32':
            warning_message = self._sanitize_windows_message(warning_message)
        self.logger.warning(warning_message)
    
    def _sanitize_windows_message(self, message):
        """
        Rimuove caratteri non supportati dalla console Windows
        Args:
            message (str): Messaggio originale
        Returns:
            str: Messaggio sanitizzato
        """
        # Mappa emoji comuni a caratteri ASCII
        replacements = {
            '✓': '[OK]',
            '✗': '[ERROR]',
            '⚠': '[WARNING]',
            '⚡': '[!]',
            '🤖': '[ROBOT]',
            '📝': '[LOG]',
            '💾': '[SAVE]',
            '🔍': '[SEARCH]',
        }
        
        for emoji, replacement in replacements.items():
            message = message.replace(emoji, replacement)
        
        # Rimuovi altri caratteri non ASCII se necessario
        # message = message.encode('ascii', 'replace').decode('ascii')
        
        return message


# Esempio di utilizzo
if __name__ == "__main__":
    # Crea un'istanza del logger personalizzabile
    chat_logger = ChatLogger()

    # Registra un messaggio di chat
    chat_logger.log_chat_message("chat_001", "user", "Ciao, come posso aiutarti?")

    # Registra messaggi vari
    chat_logger.log_info("✓ Sistema avviato correttamente")
    chat_logger.log_warning("⚠ Attenzione: risorsa limitata")
    chat_logger.log_error("✗ Errore di connessione")