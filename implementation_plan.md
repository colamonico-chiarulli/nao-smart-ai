# Piano di Implementazione: Endpoint Unificato (/chat/voice)

Questo piano dettaglia i passaggi per unificare STT e LLM in una singola chiamata API, riducendo la latenza.

## Backend (`web_api`)

### 1. Refactoring `LLMChatAPI` (`web_api/utils/llm_chat_api.py`)
Attualmente `handle_talk_action` gestisce parsing della request Flask e logica di business. Dobbiamo separare la logica.
*   **Nuovo metodo**: `process_user_message(self, chat_id, message)`
    *   Accetta `chat_id` e `message` stringa.
    *   Contiene tutta la logica di gestione storia, chiamata LiteLLM, parsing risposta.
    *   Restituisce `(success, result_dict, status_code)`.
*   **Aggiornamento**: `handle_talk_action` chiamerà `process_user_message`.

### 2. Nuova Rotta `/chat/voice` (`web_api/main.py`)
*   Accetta `POST` con `multipart/form-data`.
*   Parametri: `audio` (file), `chat_id` (opzionale text).
*   **Logica**:
    1.  Chiama `stt.transcribe_ogg(audio_file)`.
    2.  Se fallisce STT: Ritorna errore.
    3.  Se successo STT: Ottiene `text`.
    4.  Chiama `llm_chat.process_user_message(chat_id, text)`.
    5.  Ritorna JSON unificato:
        ```json
        {
          "success": true,
          "transcription": "Ciao come stai",
          "chat_id": "...",
          "response": { ...chunks... }
        }
        ```

## Client NAO (`nao-client`)

L'architettura attuale usa segnali Choregraphe (Output Box 1 -> Input Box 2). Per supportare il flusso unificato senza modificare il cablaggio grafico complessi (file .pml), useremo **ALMemory** come bus di comunicazione.

### 3. Aggiornamento `nao-stt-client-fast.py`
*   **Modifica URL**: Default a `/chat/voice`.
*   **Gestione Risposta**:
    *   Invece di emettere solo testo, gestisce il JSON completo.
    *   **Azione**: Se riceve `response` nel JSON, serializza il dict `response` in stringa JSON e solleva l'evento ALMemory `Gemini/DirectResponse`.
    *   Mantiene retro-compatibilità: Se riceve solo `text` (vecchio STT), continua a usare `self.onTranscriptionReady`.

### 4. Aggiornamento `nao-smart-ai-client.py`
*   **Nuovo Listener**: In `onLoad`, sottoscrizione all'evento `Gemini/DirectResponse`.
*   **Callback**: `onDirectResponse(value)`.
    *   Disabilita ascolto (come fa `onInput_domanda`).
    *   Deserializza JSON.
    *   Chiama `process_ai_response(json_data)`.
    *   Riabilita ascolto.

---

## Esecuzione
1.  **Backend**: Modifica `llm_chat_api.py`.
2.  **Backend**: Modifica `main.py`.
3.  **Client**: Modifica `nao-stt-client-fast.py`.
4.  **Client**: Modifica `nao-smart-ai-client.py`.
