"""
File:	/web_api/utils/cleantex.py
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright (C) 2024-2026 Rino Andriano, Vito Trifone Gargano
Created Date: Saturday, November 9th 2024, 6:37:29 pm
-----
Last Modified: 	October 02nd 2025 06:59:11 pm
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

Pulisce il testo rimuovendo emoji, caratteri speciali e normalizzando la punteggiatura.
"""

import re
from unidecode import unidecode

"""
"    Pulisce il testo rimuovendo emoji, caratteri speciali e normalizzando la punteggiatura.    
"    Args:  text (str): Testo da pulire
"    Returns:      str: Testo pulito e ottimizzato
"""


def clean_text(text):
    # Rimuove emoji e caratteri speciali
    # Questo pattern copre la maggior parte degli emoji Unicode e altri simboli speciali
    text = re.sub(
        r"[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+",
        "",
        text,
    )

    # Rimuove emoticon testuali comuni
    text = re.sub(r"[:;=]-?[)(/\\|dpDP]", "", text)  # e.g., :) :( ;) :D :P

    # Rimuove spazi multipli e va a capo
    text = re.sub(r"\s+", " ", text)

    # Normalizza la punteggiatura
    text = re.sub(r"(!+)", "!", text)  # Normalizza esclamazioni multiple
    text = re.sub(r"(\?+)", "?", text)  # Normalizza punti interrogativi multipli
    text = re.sub(r"(\.+)", ".", text)  # Normalizza punti multipli
    text = re.sub(r"(-+)", "-", text)  # Normalizza trattini multipli
    text = re.sub(r"(\*+)", "", text)  # Rimuove gli asterischi
    text = re.sub(r"[\[\]\(\)\{\}]", "", text)  # Rimuove le parentesi
    text = re.sub(r"[/\\]", "", text)  # Rimuove slash e backslash
    text = re.sub(r'"', '', text)      # Rimuove le doppie virgolette

    # Rimuove spazi prima della punteggiatura
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)

    # Rimuove spazi extra
    text = text.strip()

    # Converte in ascii e restuisce
    return unidecode(text)

def clean_markdown(text):
    # Rimuove gli eventuali blocchi di codice Markdown e spazi bianchi extra
    # dal JSON generato come risposta da LLM (Es. Gemini 2.5)
    cleaned = text.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]  # Rimuove ```json
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]  # Rimuove ```
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3] # Rimuove ``` alla fine
    cleaned = cleaned.strip()  # Rimuove eventuali spazi rimasti
    return cleaned

# test di utilizzo
if __name__ == "__main__":
    test_text = """
    Ciao!! 😊 Come stai??? :) 
    \n\n Oggi (nota importante) è una bellissima giornata... 🌞 
    Andiamo a fare una "passeggiata" [ore 15:00] nel parco! 🚶‍♂️ :D 
    {nota: portare l'ombrello} *** ....
    """

    test_markdown = """
    ```json
    {'chunks': [{'text': 'Ciao! Sono NAO, un robot umanoide. ', 'movements': ['Gestures/Hey_(7)', 'Emotions/Positive/Happy_(4)']}, {'text': 'È un piacere conoscerti! Come posso esserti utile oggi?', 'movements': ['BodyTalk/Speaking/BodyTalk_(20)', 'Emotions/Positive/Happy_(4)']}]}
    ```
    """

    cleaned = clean_text(test_text)
    print("Testo originale:")
    print(test_text)
    print("\nTesto pulito:")
    print(cleaned)
    print("\n-----")
    
    json = clean_markdown(test_markdown)
    print("JSON originale:")
    print(test_markdown)
    print("\nJSON pulito:")
    print(json)
    