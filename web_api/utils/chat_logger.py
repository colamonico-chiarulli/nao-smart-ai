"""
File:	/web_api/utils/chat_logger.py
-----
Class ChatLogger - Log per le Chat AI
-----
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright (C) 2024-2026 Rino Andriano, Vito Trifone Gargano
Created Date: Wednesday, November 19th 2024, 6:37:29 pm
-----
Last Modified: 	November 19th 2024 7:01:11 pm
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
import logging
from datetime import datetime


class ChatLogger:
    def __init__(self, log_directory=None, log_level=logging.INFO):
        """
        " Inizializza il logger per la chat
        " Args:
        "    log_directory (str, optional): Directory per i file di log.
        "        Se None, usa una sottocartella 'logs' nella directory corrente.
        "    log_level (int, optional): Livello di logging. Default è logging.INFO.
        """
        # Imposta la directory dei log
        if log_directory is None:
            log_directory = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "logs"
            )

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

        # Aggiungi un file handler
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        self.logger.addHandler(file_handler)

    def log_chat_message(self, chat_id, role, content):
        """
        " Registra un messaggio di chat nel file di log
        "  Args:
        "    chat_id (str): Identificativo della chat
        "    role (str): Ruolo del mittente (es. 'user', 'assistant')
        "    content (str): Contenuto del messaggio
        """
        # Limita la lunghezza del contenuto a 2000 caratteri
        content_str = str(content)[:2000]
        log_entry = f"CHAT_ID: {chat_id} | ROLE: {role} | MSG: {content_str}"
        self.logger.info(log_entry)

    def log_info(self, info_message):
        """Registra un messaggio di informazione"""
        self.logger.info(info_message)

    def log_error(self, error_message):
        """Registra un messaggio di errore"""
        self.logger.error(error_message)

    def log_warning(self, warning_message):
        """Registra un messaggio di warning"""
        self.logger.warning(warning_message)


# Esempio di utilizzo
if __name__ == "__main__":
    # Crea un'istanza del logger personalizzabile
    chat_logger = ChatLogger()

    # Registra un messaggio di chat
    chat_logger.log_chat_message("chat_001", "user", "Ciao, come posso aiutarti?")

    # Registra un errore
    chat_logger.log_error("Errore di connessione")
