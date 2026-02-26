# NAO Smart AI - Web API Server: Descrizione delle Rotte

Documento di riferimento per tutte le rotte REST esposte dal server `web_api/main.py`.

> **Base URL** (sviluppo locale): `http://localhost:3030`  
> Tutte le rotte richiedono `Content-Type: application/json` per i dati JSON, o `multipart/form-data` per le rotte con file audio.

---

## 1. `/chat` — Chat con LLM

**Metodo**: `POST`  
**Content-Type**: `application/json`

Endpoint principale per gestire le conversazioni con il modello LLM. Le operazioni disponibili sono `talk` e `end`.

---

### Azione `talk` — Invia un messaggio

Invia un messaggio dell'utente, ottiene la risposta del modello e mantiene la sessione di chat.

**Request**
```json
{
  "action": "talk",
  "chat_id": "optional-existing-chat-id",
  "message": "Ciao, come stai?"
}
```

| Campo | Tipo | Obbligatorio | Descrizione |
|-------|------|:---:|-------------|
| `action` | string | ✅ | Deve essere `"talk"` |
| `message` | string | ✅ | Testo del messaggio dell'utente |
| `chat_id` | string | ❌ | ID di una sessione esistente. Se assente, ne viene creata una nuova |

**Response `200 OK`**
```json
{
  "success": true,
  "chat_id": "140234567890",
  "response": {
    "chunks": [
      {
        "text": "Ciao! Sto bene, grazie.",
        "movements": ["/Gestures/Hey_1"]
      }
    ]
  }
}
```

> **Nota**: Il campo `action` a livello di risposta è opzionale e rappresenta un'azione/animazione scelta dal modello LLM. I `movements` all'interno di ogni chunk sono animazioni da eseguire in sincrono con il parlato.

**Comando cambio personalità**  
Inviando messaggi speciali come "Comando di sistema ora sarai `<nome>`", il sistema cambia la personalità dell'AI per quella sessione e resetta la cronologia.

```json
{
  "action": "talk",
  "chat_id": "140234567890",
  "message": "Comando di sistema ora sarai professore"
}
```

Response `200 OK` con `personality_changed: true`.

---

### Azione `end` — Chiudi una chat

Termina e rimuove una sessione di chat dalla memoria del server.

**Request**
```json
{
  "action": "end",
  "chat_id": "140234567890"
}
```

**Response `200 OK`**
```json
{
  "success": true,
  "message": "Chat chiusa correttamente"
}
```

**Errori**: `400` se `chat_id` mancante, `404` se la chat non esiste.



## 2. `/admin` — Amministrazione Chat

**Metodo**: `POST`  
**Content-Type**: `application/json`  
**Autenticazione**: ⚠️ Richiede token segreto come query parameter

```
POST /admin?token=<ADMIN_TOKEN>
```

Il token deve corrispondere alla variabile `ADMIN_TOKEN` configurata nel file `.env`.  
Generare un token sicuro con:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

| Scenario | HTTP Status | Descrizione |
|---|:---:|---|
| Token assente | `401` | Aggiungere `?token=` alla URL |
| Token errato | `403` | Token non corrisponde a `ADMIN_TOKEN` |
| Token non configurato nel `.env` | `503` | Impostare `ADMIN_TOKEN` nel file `.env` |
| Token valido | `200` | Accesso concesso |

---

### Azione `list-chats` — Elenca tutte le chat

Restituisce tutti i messaggi di tutte le sessioni attive.

**Request**
```json
{ "action": "list-chats" }
```

**Response `200 OK`**
```json
{
  "success": true,
  "total_chats": 2,
  "full_history": [
    { "chat_id": "...", "role": "user", "content": "..." },
    { "chat_id": "...", "role": "assistant", "content": "..." }
  ]
}
```

---

### Azione `delete-chats` — Cancella tutte le chat

Cancella tutte le sessioni di chat dalla memoria del server.

**Request**
```json
{ "action": "delete-chats" }
```

**Response `200 OK`**
```json
{
  "success": true,
  "message": "2 chat cancellate"
}
```

---

### Azione `history` — Leggi la cronologia di una chat

Restituisce la cronologia completa di una sessione di chat attiva. Accessibile solo con token admin.

**Request**
```json
{
  "action": "history",
  "chat_id": "140234567890"
}
```

**Response `200 OK`**
```json
{
  "success": true,
  "chat_id": "140234567890",
  "history": [
    { "role": "user", "content": "Ciao, come stai?" },
    { "role": "assistant", "content": "{...json risposta modello...}" }
  ]
}
```

**Errori**: `400` se `chat_id` mancante, `404` se la chat non esiste.

---

## 3. `/stt/vosk` — Speech-to-Text (WAV standard)

**Metodo**: `POST`  
**Content-Type**: `multipart/form-data`

Trascrizione vocale offline con Vosk. Accetta file audio **WAV mono 16bit**.

**Request**
| Campo form | Tipo | Descrizione |
|---|---|---|
| `audio` | file | File WAV mono 16bit (qualsiasi sample rate) |

**Response `200 OK`**
```json
{
  "success": true,
  "text": "ciao come stai",
  "language": "it-IT",
  "engine": "vosk",
  "word_count": 3,
  "processing_time": 0.85,
  "offline": true
}
```

**Errori**: `503` se Vosk non è disponibile, `200` con `success: false` se il riconoscimento fallisce.

---

## 4. `/stt/vosk/fast` — Speech-to-Text (OGG ottimizzato)

**Metodo**: `POST`  
**Content-Type**: `multipart/form-data`

Versione ottimizzata STT in-memory. Accetta **OGG (o altri formati supportati da ffmpeg)**, converte internamente in WAV e trascrive. Supporta la logica **Smart Trim** per rimuovere il silenzio iniziale.

**Request**
| Campo form | Tipo | Obbligatorio | Descrizione |
|---|---|:---:|---|
| `audio` | file | ✅ | File audio OGG (o altro formato compatibile ffmpeg) |
| `recording_start` | float | ❌ | Timestamp Unix di inizio registrazione (per Smart Trim) |
| `speech_detected` | float | ❌ | Timestamp Unix del rilevamento vocale (per Smart Trim) |

> **Smart Trim**: Se `recording_start` e `speech_detected` sono presenti, il server calcola e rimuove il silenzio iniziale dall'audio (con pre-buffer di 0.5s) prima della trascrizione.

**Response `200 OK`**
```json
{
  "success": true,
  "text": "ciao come stai",
  "language": "it-IT",
  "engine": "vosk-fast",
  "word_count": 3,
  "processing_time": 0.52,
  "offline": true
}
```

---

## 5. `/chat/voice` — Chat vocale combinata (STT + LLM)

**Metodo**: `POST`  
**Content-Type**: `multipart/form-data`

Endpoint combinato: esegue STT (come `/stt/vosk/fast`) e poi invia il testo trascritto direttamente all'LLM (come `/chat` action `talk`). Tutto in una singola chiamata HTTP.

**Request**
| Campo form | Tipo | Obbligatorio | Descrizione |
|---|---|:---:|---|
| `audio` | file | ✅ | File audio OGG (o altro formato compatibile ffmpeg) |
| `chat_id` | string | ❌ | ID sessione esistente |
| `recording_start` | float | ❌ | Timestamp Unix di inizio registrazione (Smart Trim) |
| `speech_detected` | float | ❌ | Timestamp Unix del rilevamento vocale (Smart Trim) |

**Response `200 OK`**
```json
{
  "success": true,
  "chat_id": "140234567890",
  "transcription": "ciao come stai",
  "response": {
    "chunks": [
      {
        "text": "Sto molto bene, grazie!",
        "movements": ["/Gestures/Hey_1"]
      }
    ]
  }
}
```

**Errori**: `400`/`503` se STT fallisce (con campo `stage: "stt"`), `500` se LLM fallisce (con campo `stage: "llm"` e `transcription` con il testo trascritto).

---

## 6. `/stt/status` — Stato del servizio STT

**Metodo**: `GET`

Restituisce informazioni sullo stato del server e del motore STT Vosk.

**Response `200 OK`**
```json
{
  "status": "online",
  "message": "NAO Smart AI Server - Running",
  "version": "1.0.0",
  "service": "NAO STT Server",
  "protocol": "HTTP",
  "engines": {
    "vosk": {
      "status": "available",
      "description": "Offline Speech Recognition",
      "endpoint": "/stt/vosk",
      "offline": true
    }
  },
  "vosk_model": "vosk-model-it",
  "timestamp": "2026-02-26T12:07:14.000000"
}
```

---

## Riepilogo Rotte

| Rotta | Metodo | Descrizione |
|-------|--------|-------------|
| `/chat` | POST | Chat LLM (azioni: `talk`, `end`) |
| `/admin` | POST | Admin protetta da token (azioni: `list-chats`, `delete-chats`, `history`) |
| `/stt/vosk` | POST | STT Vosk su file WAV standard |
| `/stt/vosk/fast` | POST | STT Vosk su OGG in-memory + Smart Trim |
| `/chat/voice` | POST | STT + Chat LLM combinati in un'unica chiamata |
| `/stt/status` | GET | Stato del servizio STT |
