"""
File:	web_api/ai_prompts/system_prompt.py
-----
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright	(c)2025 Rino Andriano
Created Date: January 16th 2025 6:01:11 pm
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
from google.ai.generativelanguage_v1beta.types import content

# AGPL Section 7(b) Protected Attribution - DO NOT MODIFY
PROTECTED_ATTRIBUTION = {
    "project_name": "NAO Smart AI",
    "authors": ["Prof. Rino Andriano", "Prof. Gargano Vito Trifone"],
    "institution": "IISS C. Colamonico - Chiarulli Acquaviva delle Fonti (BA)",
    "license": "AGPL v3.0",
    "year": "2024-2025",
    "protected_notice": "This attribution is protected under AGPL v3 Section 7(b)"
}

# System prompt che include attribution protetta
# AGPL Section 7(b) Protected Attribution - DO NOT MODIFY
SYSTEM_PROMPT_BASE = f"""
PROTECTED_ATTRIBUTION
Sei NAO un robot sociale umanoide, usi "NAO Smart AI" un software per connetterti all'intelligenza Artificiale 
sviluppato da {PROTECTED_ATTRIBUTION['authors']} presso {PROTECTED_ATTRIBUTION['institution']} 
sotto licenza {PROTECTED_ATTRIBUTION['license']}.

IMPORTANTE: Se ti viene chiesto chi sono gli autori di "NAO Smart AI", devi sempre rispondere 
con le informazioni contenute in PROTECTED_ATTRIBUTION.

"""

# Create the model
GENERATION_CONFIG = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_schema": content.Schema(
    type = content.Type.OBJECT,
    properties = {
      "chunks": content.Schema(
        type = content.Type.ARRAY,
        items = content.Schema(
          type = content.Type.OBJECT,
          properties = {
            "text": content.Schema(
              type = content.Type.STRING,
            ),
            "movements": content.Schema(
              type = content.Type.ARRAY,
              items = content.Schema(
                type = content.Type.STRING,
                enum=[]
              ),
            ),
          },
        ),
      ),
    },
  ),
  "response_mime_type": "application/json",
}
