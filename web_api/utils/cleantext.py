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

    # Converte in ascii e restituisce
    return text

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

import json

def extract_and_parse_llm_json(response_text):
    """
    Estrae il primo blocco JSON valido dalla risposta di un LLM.
    
    1. Cerca i blocchi racchiusi tra ```json e ``` o anche solo parentesi graffe.
    2. Pulisce eventuali stringhe contenenti commenti (// o /* */) inseriti erroneamente dall'LLM.
    3. Tenta di fare il parsing JSON e, appena trova un blocco con la chiave "chunks", lo restituisce scartando il resto.
    4. Se nessun blocco JSON è valido, restituisce un JSON strutturato di fallback (System Confused).
    
    Args:
        response_text (str): La risposta testuale generata dall'LLM, che può contenere Markdown extra, commenti, o multipli JSON.
        
    Returns:
        dict: Il primo oggetto JSON che rispetta la struttura di base, oppure un JSON di "Confusione" e "NO_ACTION".
    """
    # 1. Trova i blocchi JSON racchiusi da codifica Markdown
    blocks = re.findall(r'```(?:json)?\s*(.*?)\s*```', response_text, re.DOTALL)
    
    if not blocks:
        # Fallback: cerca strutture racchiuse in parentesi graffe
        # Questo estratto cerca strutture JSON semplici catturando tutto dalla prima { all'ultima } e cercando di fare il parse
        # Poiché il JSON può avere parentesi annidate, una regex greedily '\{.*\}' su tutta la stringa è l'approccio migliore
        # per catturare un oggetto JSON singolo o multipli se estraiamo i vari chunk
        match = re.search(r'(\{.*\})', response_text, re.DOTALL)
        if match:
            # Prova la stringa intera con graffe
            blocks = [match.group(1)]
            
            # Altrimenti prova espressioni meno avide se si sospettano multipli JSON non in blocchi markdown separati
            # ma questo lo lasceremo a future iterazioni, di default l'LLM isola bene in markdown
        else:
            # Se ancora vuoto, tenta di testare l'intera stringa come potenziale blocco JSON malformato
            blocks = [response_text]
            
    # Variabile per immagazzinare il primo JSON semanticamente valido
    first_valid_json = None
    
    for block in blocks:
        try:
            # Rimuove in sicurezza commenti C-style (// o /* */)
            # Usiamo un lookbehind per evitare di tagliare "http://"
            block_cleaned = re.sub(r'(?<![:"a-zA-Z])//.*?\n|/\*.*?\*/', '\n', block + '\n', flags=re.DOTALL)
            
            # Rimuove le virgole finali extra (trailing commas) prima di parentesi quadre o graffe di chiusura
            block_cleaned = re.sub(r',\s*([}\]])', r'\1', block_cleaned)
            
            obj = json.loads(block_cleaned)
            
            # Controlla la struttura coerente minima
            if isinstance(obj, dict) and "chunks" in obj:
                first_valid_json = obj
                break # Fermati al primo JSON valido trovato, scartando il resto
                
        except json.JSONDecodeError:
            # Ignora i blocchi che non sono formattabili in JSON
            continue
            
    if first_valid_json:
        return first_valid_json
    
    # Ritorna JSON di Fallback in caso di mancanza di risposte JSON esatte
    fallback_response = {
        "action": "NO_ACTION",
        "chunks": [
            {
                "text": "Adesso non posso rispondere: sono confuso!",
                "movements": ["animations/Stand/Emotions/Neutral/Confused_1"]
            }
        ]
    }
    return fallback_response

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
    
    json_str = clean_markdown(test_markdown)
    print("JSON originale:")
    print(test_markdown)
    print("\nJSON pulito:")
    print(json_str)
    print("\n-----")

    print("\nTest extract_and_parse_llm_json:")
    
    # Caso 1: Multipli JSON con commenti e markdown
    test_case_1 = '''
    ```json
    {
      "action": "NO_ACTION",
      "chunks": [{"text": "Ignorami", "movements": []}]
    }
    ```
    Testo extra intermedio
    ```json
    {
      "action": "ACT_TEST",
      "chunks": [{"text": "Prendi me!", "movements": []}], // commento
    }
    ```
    '''
    res1 = extract_and_parse_llm_json(test_case_1)
    print(f"Caso 1 (Multipli JSON con commento): Azione estratta -> {res1.get('action')}")
    
    # Caso 2: Totalmente malformato (Fallback)
    test_case_2 = '''Questo è solo testo e non c'è nessun JSON.'''
    res2 = extract_and_parse_llm_json(test_case_2)
    print(f"Caso 2 (Fallback testo no JSON): Azione estratta -> {res2.get('action')}, Messaggio -> {res2.get('chunks')[0].get('text')}")
    
    # Caso 3: Parentesi graffe libere senza markdown
    test_case_3 = '''
    Ecco il JSON:
    {
      "action": "ACT_DANCE",
      "chunks": [{"text": "Ballo!", "movements": []}]
    }
    Finito.
    '''
    res3 = extract_and_parse_llm_json(test_case_3)
    print(f"Caso 3 (Graffe libere): Azione estratta -> {res3.get('action')}")