# NAO Smart AI 🤖

> Un robot sociale potenziato dall'intelligenza artificiale generativa
> che conversa, comprende e si emoziona 

[![License: AGPLv3](https://img.shields.io/badge/License-AGPLv3.0-green.svg)](https://opensource.org/license/agpl-v3)
[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/)
[![NAO Robot](https://img.shields.io/badge/NAO-Robot%206-red.svg)](https://www.aldebaran.com/en/nao)
[![Any AI Models](https://img.shields.io/badge/LiteLLM%20AI%20Models-brightgreen.svg)](https://docs.litellm.ai/docs/providers)

## 📖 Descrizione

**NAO Smart AI** è un progetto innovativo che trasforma il robot NAO 6 in un robot sociale intelligente, connettendolo all'Intelligenza Artificiale per creare conversazioni naturali ed empatiche. 

## 🎓 Team di Sviluppo

Progetto sviluppato da:
- **Docenti** : Rino Andriano e Gargano Vito Trifone
- **In servizio presso** : IISS "C. Colamonico - N. Chiarulli" - Acquaviva delle Fonti (BA)



## 📜 Licenze 

### Architettura Dual-License

NAO Smart AI adotta un modello di licensing duale:

#### 🌐 Web REST API Server (AGPL-3.0)
Il componente server è rilasciato sotto **GNU AGPL-3.0**.
Questo garantisce che miglioramenti al **core** rimangano 
aperti e disponibili alla comunità.

#### 🤖 Client NAO (Licenza Proprietaria)
Il componente client per robot NAO è rilasciato sotto 
**licenza proprietaria con uso gratuito** per:
- Ospedali e strutture sanitarie pubbliche
- Centri Alzheimer
- Fondazioni ed enti no-profit con finalità sociali
- Università per fini di ricerca
- Scuole dotate di NAO con accordi documentati con gli enti sopra elencati per finalità sociali no-profit

### 📜 Licenza per il Server Web REST API (AGPL-3.0) vedi il file [LICENSE](LICENSE) per i dettagli.

---

# Changelog NAO Smart AI - Server Web API 
Tutte le modifiche a questo componente saranno documentate in questo file.

## [1.2] - 2025-02-25

### Aggiunta nuova rotta `/chat/voice`
** Endpoint combinato: STT + Chat LLM** in una singola chiamata.
 - Input: audio (file OGG/WAV), chat_id (opzionale)
 - Output: Risposta LLM con trascrizione inclusa
 - Include timing statistics se TIMING_ENABLED

### Miglioramenti
- **STT Server Optimization (RAM & Smart Trim)**: Eliminato l'I/O su disco per la rotte Fast STT elaborando l'audio interamente in RAM (`io.BytesIO`). Introdotta una logica di "Smart Trim" basata sui metadati (`recording_start` e `speech_detected`) per rimuovere il silenzio iniziale, migliorando la velocità e reattività (`web_api/utils/stt.py`).

### Sicurezza
- **Admin Token Auth**: Protetta la rotta `/admin` con token segreto configurato tramite variabile `ADMIN_TOKEN` nel file `.env`, passato come query parameter `?token=`. Risponde `401` se assente, `403` se errato, `503` se non configurato (`web_api/main.py`).
- **History protetta**: L'azione `history` (cronologia di una chat) è stata spostata dalla rotta pubblica `/chat` alla rotta protetta `/admin`, richiedendo il token per l'accesso (`web_api/main.py`).

### Fix
- **LLM Error Logging**: Rimosso il troncamento a 200 caratteri in caso di eccezioni sulla decodifica JSON dal modello LLM: ora viene stampato l'intero payload testuale restituito per facilitare il debug (`web_api/utils/llm_chat_api.py`).

### Documentazione
- **API_ROUTES.md**: Aggiornata la documentazione delle rotte API per riflettere le nuove implementazioni e miglioramenti.

## [1.1] - 2025-12-13

### Aggiunto
- **LiteLLM API**: Implementata una nuova interfaccia API per LLM agnostici nel modulo `web_api`. Aggiunta la dipendenza `litellm` per supportare molteplici provider (OpenAI, Anthropic, Gemini, etc.) e una gestione unificata delle chiavi API (commit del 2025-12-11).
- **API_KEY Multiple** Adesso è possibile utilizzare più API_KEY per il provider del modello LLM - Verranno attivate in round-robin ad ogni scambio
- **Ottimizzazione Storia Chat**: Limitata la cronologia inviata al modello agli ultimi 10 scambi (20 messaggi) più la richiesta corrente, per ridurre i costi e la latenza (commit del 2025-12-13).

## [1.0] - 2025-12-02

### Aggiunto
- **Fast Client-Server STT**: Introdotta una nuova modalità "fast" per il riconoscimento vocale.
  L'audio OGG viene inviato direttamente all'endpoint `/stt/vosk/fast` senza pre-elaborazione locale (trimming), delegando tutto al server per massimizzare la velocità di risposta.

### Migliorato
- **Animazioni Personalizzate**: L'IA ora può scegliere ed eseguire animazioni personalizzate in base al contesto della risposta (commit del 2025-11-12).

## [0.9] - 2025-11-11

### Aggiunto
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
