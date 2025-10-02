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
1. **Client NAO** (Python 2.7 + Choregraphe)
   - Gestione interfaccia utente sul robot
   - Comunicazione con Web API
   - Controllo movimenti e audio

2. **Web API Cloud** (Python 3.11)
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
1. Aprire Choregraphe
2. Importare il progetto dalla cartella `nao-client/`
3. Configurare l'indirizzo della Web API nel behavior
4. Caricare il progetto su NAO

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
│   ├── utils/                # classi ed utility
│   └── utils/movements.json  # Libreria dei movimenti di NAO (personalizzabile)
├── nao-client/               # Client NAO (Python 2.7)
└── tests/                    # Test suite
```

## 🎓 Team di Sviluppo

Progetto sviluppato da:
- **Docenti** : Rino Andriano e Gargano Vito Trifone
- **Presso**  : IISS "C. Colamonico - N. Chiarulli" - Acquaviva delle Fonti (BA)

Corso di approfondimento per:
- **Studenti**: Studenti delle Classi 3ª, 4ª, 5ª Informatica e Telecomunicazioni
- **Percorso**: PNRR D.M. 65 "*AI Smart Bots: Assistenti Virtuali Avanzati*" a.s. 2024-25
- **Percorso**: PTOF  "*NAO Smart AI - Developers Team" a.s. 2025-26

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
    
Additional Terms under Section 7(b):

>   The following attribution requirements apply to this work:
>
>   1. Any interactive user interface must preserve the original author 
>      attribution when the AI is asked about its creators
>   2. System prompts containing author information cannot be modified
>   3. The robot must always identify its original creators as specified 
>      in the source code

---
**NAO Smart AI** - *Rende la robotica sociale intelligente, empatica e accessibile* 🤖❤️