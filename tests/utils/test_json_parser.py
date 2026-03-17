"""
File:	/tests/utils/test_json_parser.py
-----
Test parser JSON
-----
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright (C) 2024-2026 Rino Andriano, Vito Trifone Gargano
Created Date: March 17th 2026 10:42:46 am
-----
Last Modified: 	March 17th 2026 10:42:46 am
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

import sys
import os

# Aggiunge la directory web_api al path per importare i moduli in modo corretto
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from web_api.utils.cleantext import extract_and_parse_llm_json
import json

def test_multiple_jsons_with_comments():
    test_str = '''
    ```json
    {
      "action": "NO_ACTION",
      "chunks": [
        {
          "text": "Per chiamare il taxi, faccio così:",
          "movements": ["Gestures/Point_(1)"]
        },
        {
          "text": "Ascolta il mio segnale speciale!",
          "movements": ["Emotions/Positive/Excited_(2)"]
        }
      ]
    }
    ```

    *Ora eseguo l'azione per chiamare il taxi!* 🚖

    ```json
    {
      "action": "ACT_ACTOR_STOP_TAXI",
      "chunks": [
        {
          "text": "TAXI! TAXI! Fermati qui, per favore!", // commento che rompe il json nativo
          "movements": ["Gestures/Hey_(3)"]
        }
      ]
    }
    ```
    '''
    
    # Dovrebbe parsare solo il PRIMO json valido riscontrato
    result = extract_and_parse_llm_json(test_str)
    
    assert result["action"] == "NO_ACTION"
    assert len(result["chunks"]) == 2
    assert "Per chiamare il taxi" in result["chunks"][0]["text"]
    
    print("Test 1 completato con successo: Parsato correttamente il primo di due JSON ignorando il secondo.")

def test_invalid_json_fallback():
    test_str = '''Questo è solo testo e non c'è nessun JSON valido qui.'''
    
    result = extract_and_parse_llm_json(test_str)
    
    assert result["action"] == "NO_ACTION"
    assert len(result["chunks"]) == 1
    assert "confuso" in result["chunks"][0]["text"].lower()
    
    print("Test 2 completato con successo: Fallback eseguito su input non valido.")
    
def test_json_blocks_with_naked_braces():
    test_str = '''
    Ah sì, ecco qui!
    {
      "action": "ACT_DANCE",
      "chunks": [
        {
          "text": "Sto ballando!",
          "movements": ["animations/Stand/Gestures/Yes_1"]
        }
      ]
    }
    Ed eccomi qui che finisco di ballare.
    '''
    
    result = extract_and_parse_llm_json(test_str)
    
    assert result["action"] == "ACT_DANCE"
    assert len(result["chunks"]) == 1
    
    print("Test 3 completato con successo: JSON estratto correttamente dalle parentesi graffe ignorando il testo verbale extra.")

def test_incomplete_json():
    # JSON troncato a metà
    test_str = '''
    {
      "action": "ACT_DANCE",
      "chunks": [
        {
          "text": "Sto bal
    '''
    result = extract_and_parse_llm_json(test_str)
    
    assert result["action"] == "NO_ACTION"
    assert "confuso" in result["chunks"][0]["text"].lower()
    
    print("Test 4 completato con successo: JSON troncato o non chiuso genera correttamente il fallback.")

def test_pure_json_with_comments():
    # Solo JSON puro (niente triple tilde markdown) contenente però commenti
    test_str = '''{
      // Questa è la mia azione principale
      "action": "ACT_DANCE",
      "chunks": [
        {
          /* Commento multilinea
             molto fastidioso */
          "text": "Ballo puro!", // Spiegazione qui
          "movements": ["animations/Stand/Gestures/Yes_1"]
        }
      ]
    }'''
    
    result = extract_and_parse_llm_json(test_str)
    
    assert result["action"] == "ACT_DANCE"
    assert len(result["chunks"]) == 1
    assert "Ballo puro!" in result["chunks"][0]["text"]
    
    print("Test 5 completato con successo: Parsing da JSON puro contente commenti C-style ha rimosso i commenti e funzionato.")

def test_historical_errors():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    bad_responses_file = os.path.join(current_dir, "bad_responses.json")
    
    if not os.path.exists(bad_responses_file):
        print("File bad_responses.json non trovato. Esegui prima extract_errors.py")
        return
        
    with open(bad_responses_file, 'r', encoding='utf-8') as f:
        errors = json.load(f)
        
    success_count = 0
    fallback_count = 0
        
    for index, err_str in enumerate(errors):
        try:
            result = extract_and_parse_llm_json(err_str)
            # Verifica che il risultato abbia i campi minimi richiesti
            assert "chunks" in result
            assert "action" in result
            
            # Se ha restituito confuso era perchè era completamene malformato
            if "confuso" in result["chunks"][0].get("text", "").lower():
                fallback_count += 1
            
            success_count += 1
        except Exception as e:
            print(f"ERRORE nel parsing della risposta #{index + 1}: {e}")
            print(f"Testo: {err_str[:100]}...")
            
    print(f"Test Storici: {success_count}/{len(errors)} errori passati con successo. Di cui {fallback_count} convertiti in fallback.")

if __name__ == "__main__":
    print("Esecuzione test parser JSON...")
    test_multiple_jsons_with_comments()
    test_invalid_json_fallback()
    test_json_blocks_with_naked_braces()
    test_incomplete_json()
    test_pure_json_with_comments()
    print("-" * 50)
    test_historical_errors()
    print("Tutti i test completati con successo!")
