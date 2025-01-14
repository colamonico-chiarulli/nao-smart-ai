"""
File:	/web_api/utils/fix_movements.py
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright (C) 2024-2026 Rino Andriano, Vito Trifone Gargano
Created Date: Thuesday, January 14th 2025, 7:37:29 pm
-----
Last Modified: 	January 14th 2025, 7:37:29 pm
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

Verifica i movimenti scelti dall'AI per NAO e, se presenti in pù varianti, 
genera stringhe di animazioni casuali tra quelle disponibili

Es. "Emotions/Positive/Interested(2)" => "animations/Stand/Emotions/Positive/Interested_1 o (2)
"""

import random
import re

def fix_animation(movimento):
    """ Funzione helper per processare un singolo movimento
    " se a fine stringa c'è un numero tra parentesi
    " genera una stringa casuale da 1 a N
    """
    pattern = r'_\((\d+)\)$' #verifica se a fine stringa è presente _(nn)
    match = re.search(pattern, movimento)
    
    if match:
        # Estrae il numero tra parentesi
        num_max = int(match.group(1))
        # Genera numero casuale tra 1 e num_max
        num_random = random.randint(1, num_max)
        # Sostituisce (numero) con _numero
        movimento = re.sub(pattern, f'_{num_random}', movimento)
    
    return "animations/Stand/" + movimento

# test di utilizzo
if __name__ == "__main__":
    # Esempio di utilizzo
    test_movement = "Emotions/Positive/Happy_(12)"

    fixed = fix_animation(test_movement)
    print("movimento originale:")
    print(test_movement)
    print("\nmovimento corretto:")
    print(fixed)
