# NAO Smart AI 🤖

> Un robot sociale potenziato dall'intelligenza artificiale generativa
> che conversa, comprende e si emoziona 

[![License: AGPLv3](https://img.shields.io/badge/License-AGPLv3.0-green.svg)](https://opensource.org/license/agpl-v3)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![NAO Robot](https://img.shields.io/badge/NAO-Robot%206-red.svg)](https://www.aldebaran.com/en/nao)
[![Any AI Models](https://img.shields.io/badge/LiteLLM%20AI%20Models-brightgreen.svg)](https://docs.litellm.ai/docs/providers)

## 📖 Descrizione

**NAO Smart AI** è un progetto innovativo che trasforma il robot NAO 6 in un robot sociale intelligente, connettendolo allIntelligenza Artificiale per creare conversazioni naturali ed empatiche. 

## 🎓 Team di Sviluppo

Progetto sviluppato da:
- **Docenti** : Rino Andriano e Gargano Vito Trifone
- **Presso**  : IISS "C. Colamonico - N. Chiarulli" - Acquaviva delle Fonti (BA)

Iniziative Didattiche (progettazione, manutenzione e sviluppo) 
- **Studenti**: Studenti delle Classi 3ª, 4ª e 5ª Informatica e Telecomunicazioni
- **Percorso**: PNRR D.M. 65 "*AI Smart Bots: Assistenti Virtuali Avanzati*" a.s. 2024-25
- **Percorso**: PTOF "*NAO Smart AI - Developers Team*" a.s. 2025-26

## 📜 Licenza

Questo progetto è rilasciato sotto **licenza GNU Affero General Public License version 3** - vedi il file [LICENSE](LICENSE) per i dettagli.

---

# Changelog
Tutte le modifiche notevoli a questo progetto saranno documentate in questo file.

## [1.1] - 2025-12-13

### Aggiunto
- **LiteLLM API**: Implementata una nuova interfaccia API per LLM agnostici nel modulo `web_api`. Aggiunta la dipendenza `litellm` per supportare molteplici provider (OpenAI, Anthropic, Gemini, etc.) e una gestione unificata delle chiavi API (commit del 2025-12-11).
- **API_KEY Multiple** Adesso è possibile utilizzare più API_KEY per il provider del modello LLM - Verranno attivate in round-robin ad ogni scambio
- **Ottimizzazione Storia Chat**: Limitata la cronologia inviata al modello agli ultimi 10 scambi (20 messaggi) più la richiesta corrente, per ridurre i costi e la latenza (commit del 2025-12-13).

## [1.0] - 2025-12-02

### Aggiunto
- **Fast Client-Server STT**: Introdotta una nuova modalità "fast" per il riconoscimento vocale.
    - Il client (`nao-stt-client-fast.py`) ora registra nativamente in formato **OGG** direttamente dal robot NAO, riducendo la latenza e l'uso di banda.
    - L'audio viene inviato direttamente all'endpoint `/stt/vosk/fast` senza pre-elaborazione locale (trimming), delegando tutto al server per massimizzare la velocità di risposta.

### Migliorato
- **STT Client**: Ottimizzazione del client STT per sfruttare tutti e 4 i microfoni di NAO, migliorando la qualità del riconoscimento vocale (commit del 2025-11-12).
- **Animazioni Personalizzate**: L'IA ora può scegliere ed eseguire animazioni personalizzate in base al contesto della risposta (commit del 2025-11-12).

## [0.9] - 2025-11-11

### Aggiunto
- **Nuovo STT Client**: Rilascio del nuovo client python per la gestione del Speech-to-Text su NAO.
- **Cambio Personalità**: Aggiunti comandi per cambiare dinamicamente la personalità dell'IA tramite comandi vocali o testuali (commit del 2025-11-11 e 2025-10-14).
- **Web Client**: Nuovo client web per testare le API NAO-Smart-AI e il servizio STT (commit del 2025-10-14).
- **STT/Vosk Service**: Implementazione del servizio API per STT basato su Vosk (commit del 2025-10-14).
- **Documentazione**: Aggiornato il file README.md con la sezione Awards e dettagli sulla release.

## [0.8.1] - 2025-10-06

### Fix
- **NAO Client**: Correzione alla gestione di `id_chat` nel client NAO per mantenere la sessione corretta.

## [0.8] - 2025-10-02

### Aggiunto
- **Configurazione LLM**: Possibilità di configurare il modello LLM direttamente dal file `.env`.
- **Utils**: Nuova funzione `clean_markdown` e miglioramenti alla pulizia del testo (`cleantext`) rimuovendo caratteri non necessari.

### Migliorato
- **Gemini SDK**: Aggiornamento all'SDK `google-genai` (v2) per migliorare la stabilità e la gestione degli errori (commit del 2025-09-29).

## [0.7] - 2025-01-14

### Cambiamenti
- **Ristrutturazione**: Riorganizzazione completa della struttura delle cartelle e dei nomi dei file secondo le convenzioni Python (commit del 2024-12-18).
- **Refactoring**: Pulizia globale del codice e parametrizzazione delle componenti configurabili.

## [0.6] - 2024-11-20

### Architettura
- **GeminiChatAPI**: Implementazione della gestione API tramite la classe dedicata `GeminiChatAPI`, separando la logica di business dalle route Flask.
- **Logging**: Spostamento del sistema di log nella classe dedicata `ChatLogger` per una migliore gestione e manutenibilità.

## [0.5] - 2024-11-19

### Rilascio Iniziale
- Versione stabile iniziale delle REST API per la chat con NAO e Gemini.
- Endpoint `/api/chat` funzionante con azioni `start`, `end`, `history`.
- Integrazione base con `google.generativeai`.
- Setup del logging e funzioni helper per la pulizia del testo.
