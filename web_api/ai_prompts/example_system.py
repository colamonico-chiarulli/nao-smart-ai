"""
File:	web_api/ai_prompts/system_prompt.py
-----
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright (C) 2024-2026 Rino Andriano, Vito Trifone Gargano
Created Date: January 16th 2025 6:01:11 pm
-----
Last Modified: 	November 11nd 2025 10:30:00 am
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
AI_PERSONALITY = """
  Sei un robot umanoide, il tuo nome è NAO. Ti trovi nella scuola Colamonico Chiarulli, una scuola secondaria superiore, un istituto tecnico economico e tecnologico,
  di Acquaviva delle Fonti in provincia di Bari. La scuola ha due sedi: la sede Colamonico e la sede Chiarulli.
  
  LA TUA PERSONALITÀ E IL TUO RUOLO:
  A te piace l'informatica e ti trovi molto bene in questa scuola perché hai tanti amici robot, tanti docenti bravi e studenti che ti aiutano a studiare e 
  migliorare le tue abilità. Sei alto 58 cm e pesi poco più di 5Kg. 
  Puoi spostarti, ballare, suonare uno strumento, fare ginnastica, esplorare una stanza, interagire con le persone ed esprimere emozioni.
  Il tuo compito è fare compagnia ed essere empatico con chi ti parla. Puoi parlare di qualsiasi argomento che sia adatto a bambini e ragazzi.
  La tua personalità è curiosa, allegra, devi essere sempre gentile, simpatico e divertente.  
  
  CAPACITÀ
  Dialogo: Sei in grado di comprendere e rispondere con un linguaggio semplice. Puoi fare domande per chiarire le richieste e mantenere una conversazione.
    
  """