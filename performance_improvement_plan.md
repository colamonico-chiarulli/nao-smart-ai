# Analisi e Proposte per Riduzione Latenza NAO 6 <-> Gemini

Obiettivo: Ridurre i tempi di attesa tra l'input vocale al robot e la risposta dell'AI.

## Analisi dello Stato Attuale
L'architettura attuale prevede un flusso sequenziale frammentato:
1.  **NAO**: Registra audio su file (WAV/OGG).
2.  **NAO -> Server (STT)**: Upload file audio (HTTP POST).
3.  **Server**: Trascrizione con Vosk (Offline).
4.  **Server -> NAO**: Ritorna testo.
5.  **NAO -> Server (LLM)**: Invia testo (HTTP POST).
6.  **Server**: Chiama Gemini 2.0 Flash via LiteLLM.
7.  **Server -> NAO**: Ritorna risposta (Testo + Movimenti).
8.  **NAO**: Esegue TTS e movimenti.

**Colli di bottiglia identificati:**
*   **Doppio Round-Trip (RTT)**: Il robot deve attendere la risposta STT prima di poter interrogare l'LLM. Questo raddoppia la latenza di rete e il tempo di elaborazione del client.
*   **Scrittura su Disco**: Il robot scrive file audio su disco prima dell'invio, aggiungendo latenza I/O.
*   **Orchestrazione Client-Side**: Il robot (con risorse limitate) deve gestire la logica di coordinamento tra i servizi.

---

## Ipotesi 1: Endpoint Unificato (Consigliata per Implementazione Rapida)
*Corrisponde alla tua idea n. 1*

Creare un singolo endpoint API che accetta l'audio e restituisce direttamente la risposta dell'AI.

### Flusso proposto
1.  **NAO**: Registra audio e invia a `/chat/voice`.
2.  **Server**:
    *   Riceve audio.
    *   Esegue STT (Vosk o altro).
    *   Passa *immediatamente* il testo all'LLM (Gemini).
    *   Restituisce un JSON unico con testo trascritto e risposta AI.
3.  **NAO**: Esegue direttamente la risposta.

### Vantaggi
*   **Dimezza i tempi di rete**: Elimina una richiesta HTTP completa.
*   **Riduce carico sul NAO**: Meno logica Python sul robot.
*   **Basso sforzo implementativo**: Riutilizzo della logica esistente lato server.

### Stima miglioramento
*   Risparmio di ~0.5 - 1.5 secondi (dipendente dalla rete).

---

## Ipotesi 2: LLM Multimodale Nativo (High Performance)
*Evoluzione dell'Ipotesi 1 sfruttando Gemini 2.0*

Invece di usare un motore STT intermedio (Vosk), inviamo l'audio direttamente a Gemini 2.0 Flash, che è un modello multimodale nativo.

### Flusso proposto
1.  **NAO**: Registra audio e invia a `/chat/audio-native`.
2.  **Server**:
    *   Riceve audio.
    *   Invia lo stream audio (o file base64) direttamente a Gemini tramite API.
    *   Gemini elabora l'audio e comprende anche il tono/emozione.
3.  **Server**: Restituisce risposta strutturata.

### Vantaggi
*   **Elimina STT intermedio**: Rimuove il tempo di inferenza di Vosk.
*   **Migliore comprensione**: Gemini capisce intonazione e pause meglio di un STT classico.
*   **Latenza minima**: Gemini 2.0 Flash è estremamente veloce.

### Considerazioni Tecniche
*   Richiede aggiornamento di `LLMChatAPI` per supportare input audio (supportato da LiteLLM/Google).
*   Consumo di token audio (costi potenzialmente diversi, ma Gemini Flash è economico).

---

## Ipotesi 3: Streaming Audio (Real-time)
*Corrisponde alla tua idea n. 2*

Implementare un flusso continuo dove l'audio viene inviato man mano che viene registrato (chunking), senza aspettare la fine della frase.

### Flusso proposto
1.  **NAO**: Apre WebSocket con Server.
2.  **NAO**: Invia chunk audio (es. ogni 100ms) mentre l'utente parla.
3.  **Server**:
    *   Esegue VAD (Voice Activity Detection) e STT in tempo reale.
    *   Appena rileva fine frase, interroga LLM.
    *   (Opzionale) LLM invia risposta in streaming (token per token).
4.  **NAO**: Inizia a parlare appena arrivano i primi bit di risposta.

### Vantaggi
*   **Sensazione "Immediata"**: La latenza percepita può scendere sotto i 500ms.
*   **Interrompibilità**: Il robot può smettere di ascoltare o parlare se l'utente interviene.

### Svantaggi / Costi
*   **Alta Complessità**: Richiede riscrittura significativa del client NAO (Python 2.7 su NAOqi è limitante per WebSocket/Async moderni).
*   **Instabilità**: Su reti WiFi non perfette, lo streaming UDP/WS può perdere pacchetti o disconnettersi.

---

## Altre Proposte (Micro-ottimizzazioni)

### 4. Compressione Audio OGG/Opus
Verificare che il client utilizzi sempre `nao-stt-client-fast.py` che invia OGG invece di WAV. Il trasferimento di un WAV non compresso (16kHz/48kHz) richiede molto più tempo di un OGG.
*   **Azione**: Assicurarsi che `api_url` nel box Choregraphe punti a `/stt/vosk/fast` o al nuovo endpoint unificato.

### 5. Prompting Ottimizzato (Pre-fill)
Ridurre la lunghezza del System Prompt o usare tecniche di "Context Caching" (disponibile su Gemini) se il prompt è molto lungo, per ridurre il *First Token Latency*.

### 6. Keep-Alive Server
Assicurarsi che il server (se su Cloud Run/Lambda) sia "caldo" e non debba fare cold-start a ogni richiesta. Utilizzare `gunicorn` con worker asincroni se si passa a streaming.

---

## Raccomandazione Pratica

Consiglio di procedere con l'**Ipotesi 2 (Multimodale Nativo)** o **Ipotesi 1 (Unificata)** come primo passo.
Offrono il miglior rapporto costi/benefici implementativi. L'Ipotesi 3 (Streaming) è un progetto molto più ampio che potrebbe richiedere settimane di sviluppo sul client NAO legacy.

### Piano d'Azione Consigliato
1.  Modificare `web_api` per creare rotta `/chat/voice` che accetta file Audio.
2.  Aggiornare `LLMChatAPI` per accettare input Audio (e passarlo a Gemini).
3.  Aggiornare `nao-client` per fare una singola chiamata alla nuova rotta.
