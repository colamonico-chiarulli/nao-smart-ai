"""
File:	/tests/utils/extract_errors.py
-----
Extract errors from logs
-----
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright (C) 2024-2026 Rino Andriano, Vito Trifone Gargano
Created Date: 	March 17th 2026 10:43:49 am
-----
Last Modified: 	March 17th 2026 10:44:13 am
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

import os
import re
import json

def extract_errors_from_logs(logs_dir, output_file):
    error_blocks = []
    
    for filename in os.listdir(logs_dir):
        if not filename.endswith('.txt'):
            continue
            
        filepath = os.path.join(logs_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        i = 0
        while i < len(lines):
            line = lines[i]
            # Look for "ERROR - Testo ricevuto: "
            if "ERROR - Testo ricevuto: " in line:
                # Extract the first line of the block
                block = line.split("Testo ricevuto: ")[1]
                i += 1
                
                # Consume lines until we hit another log line (starts with a date/time like 2026-03-xx)
                while i < len(lines) and not re.match(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}', lines[i]):
                    block += lines[i]
                    i += 1
                    
                error_blocks.append(block.strip())
            else:
                i += 1
                
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(error_blocks, f, indent=4, ensure_ascii=False)
        
    print(f"Estratti {len(error_blocks)} blocchi di errore e salvati in {output_file}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    logs_dir = os.path.join(current_dir, "..", "..", "web_api", "logs")
    output_file = os.path.join(current_dir, "bad_responses.json")
    
    extract_errors_from_logs(logs_dir, output_file)
