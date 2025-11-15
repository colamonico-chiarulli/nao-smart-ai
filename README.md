# NAO Smart AI 🤖

> Un robot sociale potenziato dall'intelligenza artificiale generativa
> che conversa, comprende e si emoziona 

[![License: AGPLv3](https://img.shields.io/badge/License-AGPLv3.0-green.svg)](https://opensource.org/license/agpl-v3)
[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/)
[![NAO Robot](https://img.shields.io/badge/NAO-Robot%206-red.svg)](https://www.aldebaran.com/en/nao)
[![Google Gemini](https://img.shields.io/badge/Google-Gemini%20AI-brightgreen.svg)](https://ai.google.dev/)

## 📖 Descrizione

**NAO Smart AI** è un progetto innovativo che trasforma il robot NAO 6 in un robot sociale intelligente, connettendolo ai servizi cloud di Google Gemini per creare conversazioni naturali ed empatiche. 

Il sistema supera i limiti delle risposte predefinite, offrendo:
- 🗣️ **Dialoghi naturali dinamici** generati in tempo reale
- 🎭 **Gestione emotiva avanzata** con sincronizzazione del linguaggio del corpo
- 🎯 **Personalità adattive di AI** multiple e attivabili tramite comandi vocali
- 🔄 **Autonomia completa** - serve solo una connessione WiFi ad Internet
- 🎪 **Controllo completamente vocale** - nessun PC da collegare a NAO
- 🔈**Riconoscimento Audio potenziato** - Rispetto agli standard di NAO

## ✨ Caratteristiche principali

### 🧠 Intelligenza Artificiale Avanzata
- Integrazione completa con **Google Gemini** per conversazioni contestuali
- Analisi semantica in tempo reale per riconoscimento emotivo delle risposte
- Generazione dinamica di risposte personalizzate

### 🎭 Espressività Emotiva
- Sincronizzazione automatica tra dialogo e linguaggio del corpo
- Selezione intelligente dei movimenti dalla libreria emotiva di NAO
- Modulazione emotiva basata sul contenuto della conversazione

### 🎯 Personalizzazione Semplice
- **System prompt** configurabili per diverse personalità
- Addestramento specifico per contesti d'uso
- Attivazione di modalità diverse tramite comandi vocali
- Log dei dialoghi per analisi e miglioramento prompt AI

### 🌐 Architettura Scalabile
- **Web API cloud** sviluppata in Python 3.11
- Gestione simultanea di più robot NAO
- Conservazione della cronologia dei dialoghi

## 🏗️ Architettura del Sistema

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│                 │    │                  │    │                 │
│   Robot NAO     │◄──►│   Web API Cloud  │◄──►│  Google Gemini  │
│  (Python 2.7)   │    │  (Python 3.11)   │    │      AI         │
│                 │    │                  │    │                 │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### Componenti
1. **Client NAO** (Python 2.7 + Choregraphe) - NON FORNITO
   - Gestione interfaccia utente sul robot
   - Comunicazione con Web API
   - Controllo movimenti e audio
   - Invio audio

2. **Web API Cloud** (Python 3.11)
   - Riconoscimento audio STT
   - Bridge tra NAO e Google Gemini
   - Gestione personalità multiple
   - Elaborazione emotiva e storia dialoghi


3. **Integrazione Google Gemini**
   - Generazione dialoghi naturali
   - Analisi semantica ed emotiva
   - Risposte contestualizzate

## 🚀 Installazione e Setup

### Prerequisiti
- Robot NAO 6 con NAOqi OS
- Choregraphe Suite per sviluppo
- Server cloud con Python 3.11+
- Account Google AI Platform

### 1. Setup Web API
```bash
# Clone del repository
git clone https://github.com/colamonico-chiarulli/nao-smart-ai
cd nao-smart-ai

# Installazione dipendenze
pip install -r requirements.txt

# Configurazione variabili ambiente
cp .env.example .env
# Editare .env con le proprie chiavi API e gli altri parametri

# Configurazione libreria movimenti
cp movements.example.json movements.json
# Editare movements.json con i movimenti di NAO che si vogliono gestire
```

### 2. Deploy su Cloud
```bash
# Deploy su piattaforma cloud (esempio con Heroku)
heroku create nao-smart-ai
git push heroku main
```

### 3. Configurazione NAO
1. Occorre scrivere un programma client personalizzato

## 🎯 Casi d'Uso

### 🏥 Ospedali Pediatrici
- Supporto psicologico durante procedure mediche
- Riduzione ansia pre-operatoria con narrazioni interattive
- Compagnia durante ricoveri prolungati
- Motivazione in sessioni di fisioterapia

### 🎓 Ambiente Educativo
- Accoglienza e orientamento studenti
- Supporto personalizzato per studenti con BES
- Introduzione metodologie didattiche innovative
- Assistenza nell'apprendimento interattivo

### 🧩 Disturbi dello Spettro Autistico
- Ambiente controllato per sviluppo competenze sociali
- Esercizi di comunicazione personalizzati
- Routine prevedibili e rassicuranti
- Progressione graduale nelle interazioni

### 👵 Assistenza Anziani
- Stimolazione memoria attraverso conversazioni guidate
- Utilizzo di musica e ricordi personali
- Compagnia intelligente adattiva
- Supporto per persone con demenza

## 🛠️ Struttura del Progetto

```
nao-smart-ai/
├── web-api/                  # Web API Cloud (Python 3.11)
│   ├── main.py               # Applicazione principale
│   ├── .env                  # Personalizzazione parametri
│   ├── ai_prompts/           # Prompt AI personalizzabili
│   ├── logs/                 # Log giornaliero delle chat
│   ├── models/               # Modelli STT Vosk
│   ├── utils/                # classi ed utility
│   └── utils/movements.json  # Libreria dei movimenti di NAO (personalizzabile)
└── tests/                    # Test suite
```

## 🎓 Team di Sviluppo

Progetto sviluppato da:
- **Docenti** : Rino Andriano e Gargano Vito Trifone
- **Presso**  : IISS "C. Colamonico - N. Chiarulli" - Acquaviva delle Fonti (BA)

Iniziative Didattiche (progettazione, manutenzione e sviluppo) 
- **Studenti**: Studenti delle Classi 3ª, 4ª e 5ª Informatica e Telecomunicazioni
- **Percorso**: PNRR D.M. 65 "*AI Smart Bots: Assistenti Virtuali Avanzati*" a.s. 2024-25
- **Percorso**: PTOF "*NAO Smart AI - Developers Team*" a.s. 2025-26

---
**NAO Smart AI** - *Rende la robotica sociale intelligente, empatica e accessibile* 🤖❤️

## 📜 Licenza

Questo progetto è rilasciato sotto **licenza GNU Affero General Public License version 3** - vedi il file [LICENSE](LICENSE) per i dettagli.

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
    
## Additional Terms under AGPLv3 Section 7

In accordance with Section 7 of the GNU Affero General Public License v3,
the following additional terms apply to this software:

### 1. REQUIRED ATTRIBUTION (Section 7(b)(c)(d))

Any interactive user interface must preserve and display the original 
author attribution when the AI is asked about its creators, origin, 
or development team.

The robot NAO Smart AI must always identify itself as:
"Developed by Prof. Rino Andriano and Prof. Vito Trifone Gargano 
at IISS Colamonico-Chiarulli, Acquaviva delle Fonti (BA), Italy"

Any deployment in educational or healthcare settings must prominently 
display:

**Powered by NAO Smart AI
Open Source project by Prof. Rino Andriano & Prof. Vito Trifone Gargano
IISS "C. Colamonico - N. Chiarulli" - Acquaviva delle Fonti (BA), Italy**


#### Public deployments and demonstrations:

When demonstrating the robot at public events, conferences, or in 
published materials (videos, articles, case studies), credit must 
be given to the original authors.


### 2. UNMODIFIABLE SYSTEM PROMPTS (Section 7(b))

System prompts containing Author attribution information cannot be modified
or removed without explicit written permission from the copyright holders.

### 3. TRADEMARK PROTECTION (Section 7(e))

"NAO Smart AI" is a trademark associated with the original authors.

Use of this name for commercial purposes requires written authorization.

Modified distributions (forks) must use a different name 
(e.g., "Fork of NAO Smart AI", "Based on NAO Smart AI") and clearly 
indicate modifications.

### 4. INDEMNIFICATION (Section 7(f))

Any person or entity that modifies, deploys, or distributes this 
software agrees to indemnify, defend, and hold harmless the authors 
(Rino Andriano, Vito Trifone Gargano) and IISS "C. Colamonico - N. 
Chiarulli" from all claims, damages, losses, liabilities, and expenses 
(including legal fees) arising from:

a) Modifications to the software affecting robot safety or AI behavior

b) Deployment with vulnerable populations (minors, patients with 
   cognitive impairments, elderly with dementia)

c) Integration with third-party AI services or modifications to 
   AI prompts generating inappropriate content

d) Physical robot operations and safety incidents

e) Violations of applicable healthcare, education, data protection 
   (GDPR), or robotics safety laws

This indemnification supplements, but does not replace, the warranty 
disclaimers in AGPLv3 sections 15-16.

### 5. SAFETY AND ETHICAL USE REQUIREMENTS (Section 7(b)(c))

Users deploying this software with NAO robots MUST comply with:

a) **Supervision**: Adult supervision is MANDATORY when interacting 
   with minors, cognitively impaired individuals, or vulnerable users

b) **Risk Assessment**: Conduct risk assessment before deployment in 
   healthcare or educational settings, considering:
   - Physical safety (robot movements in proximity to users)
   - Psychological safety (content appropriateness)
   - Data protection (GDPR compliance for conversation logs)

c) **Content Filtering**: Implement content filtering and moderation 
   appropriate for the target population (children, patients, elderly)

d) **Regulatory Compliance**: Comply with applicable regulations for:
   - Medical devices (if used in clinical settings)
   - Educational technology (privacy, child protection)
   - Assistive technologies (accessibility standards)
   - Robotics safety (ISO standards if applicable)

e) **Data Protection**: Maintain conversation logs in compliance with 
   GDPR and local privacy laws, including:
   - Informed consent from users (or legal guardians for minors)
   - Right to access, rectification, erasure
   - Data minimization and purpose limitation
   - Secure storage and encryption

f) **Incident Reporting**: Report any serious incidents (injuries, 
   inappropriate content, privacy breaches) to local authorities 
   and the software authors

Failure to comply with these requirements does not void the license, 
but increases indemnification obligations under term 4 above.

### 6. CONTRIBUTION LICENSE AGREEMENT

Contributors submitting code (pull requests, patches, extensions) 
automatically agree to:

a) Release their contributions under AGPLv3

b) Accept these Additional Terms (Section 7)

c) Grant a perpetual, worldwide, royalty-free license to the project
maintainers to use, modify, and distribute their contributions

d) Warrant that their contributions are original or properly licensed

Contributors retain copyright on their specific contributions and 
will be acknowledged in the AUTHORS or CONTRIBUTORS file.

