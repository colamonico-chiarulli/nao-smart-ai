"""
File:	/web_api/utils/stt_vosk.py
-----
Classe VoskSTT - Speech-to-Text con Vosk per NAO Robot
-----
@author  Nuccio Gargano <v.gargano@colamonicochiarulli.edu.it>
@copyright	(c)2025 Nuccio Gargano
Created Date: Friday, October 10th 2025, 18:30:00 pm
-----
Last Modified: 	October 10th 2025, 19:00:00 pm
Modified By: 	Nuccio Gargano <v.gargano@colamonicochiarulli.edu.it>
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

import os
import json
import wave
import tempfile
from datetime import datetime
from flask import request, jsonify

# Import Vosk con gestione errori
try:
    from vosk import Model, KaldiRecognizer, SetLogLevel
    VOSK_AVAILABLE = True
    # Disabilita log verbosi di Vosk
    SetLogLevel(-1)
except ImportError:
    VOSK_AVAILABLE = False
    Model = None
    KaldiRecognizer = None


class STT:
    """
    Classe per gestire il riconoscimento vocale con Vosk o altri modelli
    """
    
    def __init__(self, logger=None, model_path=None):
        """
        Inizializza il sistema STT con Vosk
        
        Args:
            logger: Istanza di ChatLogger per logging
            model_path: Percorso personalizzato del modello (opzionale)
        """
        self.logger = logger
        self.vosk_model = None
        self.error_message = None
        self.is_available = False
        
        # Inizializza il modello
        self._initialize_model(model_path)
    
    def _find_vosk_model(self, models_dir):
        """
        Cerca automaticamente il modello Vosk nella cartella models
        Accetta sia 'vosk-model-it' che 'vosk-model-it-0.22'
        
        Args:
            models_dir: Directory dove cercare i modelli
            
        Returns:
            str: Percorso del modello trovato, None se non trovato
        """
        if not os.path.exists(models_dir):
            return None
        
        # Prima cerca il nome standard
        standard_path = os.path.join(models_dir, "vosk-model-it")
        if os.path.exists(standard_path) and os.path.isdir(standard_path):
            # Verifica che contenga i file necessari
            required_dirs = ['am', 'conf', 'graph', 'ivector']
            if all(os.path.exists(os.path.join(standard_path, d)) for d in required_dirs):
                return standard_path
        
        # Altrimenti cerca cartelle che iniziano con "vosk-model-it"
        try:
            for item in os.listdir(models_dir):
                item_path = os.path.join(models_dir, item)
                if os.path.isdir(item_path) and item.startswith("vosk-model-it"):
                    # Verifica che contenga i file necessari
                    required_dirs = ['am', 'conf', 'graph', 'ivector']
                    if all(os.path.exists(os.path.join(item_path, d)) for d in required_dirs):
                        return item_path
        except Exception:
            pass
        
        return None
    
    def _initialize_model(self, model_path=None):
        """
        Inizializza il modello Vosk
        
        Args:
            model_path: Percorso personalizzato del modello
        """
        if not VOSK_AVAILABLE:
            self.error_message = "Libreria Vosk non installata. Installa con: pip install vosk"
            # Non logga su file, solo messaggio in caso di debug
            return
        
        # Determina il percorso del modello
        if model_path is None:
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            models_dir = os.path.join(current_dir, "models")
            
            # Cerca automaticamente il modello
            model_path = self._find_vosk_model(models_dir)
            
            if model_path is None:
                # Se non trovato, usa il percorso standard per il messaggio di errore
                model_path = os.path.join(models_dir, "vosk-model-it")
        
        # Verifica esistenza modello
        if not os.path.exists(model_path):
            self.error_message = self._generate_installation_instructions(model_path)
            # Non logga su file
            return
        
        try:
            # Carica il modello Vosk
            self.vosk_model = Model(model_path)
            self.is_available = True
            # Non logga su file
        except Exception as e:
            self.error_message = f"Errore nel caricamento del modello Vosk: {str(e)}"
            # Non logga su file
    
    def _generate_installation_instructions(self, expected_path):
        """
        Genera le istruzioni per installare il modello Vosk
        
        Args:
            expected_path: Percorso dove il modello è atteso
            
        Returns:
            str: Messaggio formattato con istruzioni
        """
        current_dir = os.path.dirname(expected_path)
        
        return f"""
╔════════════════════════════════════════════════════════════════╗
║  ERRORE: Modello Vosk non trovato                              ║
╠════════════════════════════════════════════════════════════════╣
║  Percorso atteso: {expected_path:44s} ║
║                                                                ║
║  ISTRUZIONI PER L'INSTALLAZIONE:                               ║
║                                                                ║
║  1. Scarica il modello italiano da:                            ║
║     https://alphacephei.com/vosk/models                        ║
║                                                                ║
║  2. Modello consigliato: vosk-model-it-0.22                    ║
║     (dimensione: ~1.1 GB, accuratezza alta)                    ║
║                                                                ║
║  3. Estrai lo zip                                              ║
║                                                                ║
║  4. IMPORTANTE: Rinomina la cartella estratta in               ║
║     'vosk-model-it' (senza il numero di versione)              ║
║                                                                ║
║  5. Posiziona la cartella in: {current_dir:31s} ║
║                                                                ║
║  LINK DIRETTO:                                                 ║
║  https://alphacephei.com/vosk/models/vosk-model-it-0.22.zip    ║
║                                                                ║
║  ESEMPIO COMANDI LINUX/MAC:                                    ║
║  cd {current_dir:54s} ║
║  wget https://alphacephei.com/vosk/models/vosk-model-it-0.2... ║
║  unzip vosk-model-it-0.22.zip                                  ║
║  mv vosk-model-it-0.22 vosk-model-it                           ║
║  rm vosk-model-it-0.22.zip                                     ║
║                                                                ║
║  ESEMPIO COMANDI WINDOWS (PowerShell):                         ║
║  cd {current_dir:54s} ║
║  Invoke-WebRequest -Uri "https://alphacephei.com/vosk/model... ║
║    -OutFile "vosk-model-it-0.22.zip"                           ║
║  Expand-Archive -Path "vosk-model-it-0.22.zip" -Destination... ║
║  Rename-Item -Path "vosk-model-it-0.22" -NewName "vosk-model-it" ║
║  Remove-Item "vosk-model-it-0.22.zip"                          ║
║                                                                ║
║  STRUTTURA FINALE CORRETTA:                                    ║
║  models/                                                       ║
║  └── vosk-model-it/          <- Nome senza versione!           ║
║      ├── am/                                                   ║
║      ├── conf/                                                 ║
║      ├── graph/                                                ║
║      └── ivector/                                              ║
╚════════════════════════════════════════════════════════════════╝
"""
    
    def _validate_audio_format(self, wf):
        """
        Valida il formato del file audio WAV
        
        Args:
            wf: Oggetto wave aperto
            
        Returns:
            tuple: (is_valid, error_message)
        """
        channels = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        framerate = wf.getframerate()
        
        # Non logga formato audio su file
        
        # Validazione: deve essere MONO
        if channels != 1:
            return False, f"Audio deve essere MONO (ricevuto {channels} canali)"
        
        # Validazione: deve essere 16bit
        if sampwidth != 2:
            return False, f"Audio deve essere 16bit (ricevuto {sampwidth*8}bit)"
        
        return True, None
    
    def _process_audio(self, wf, framerate):
        """
        Processa il file audio con Vosk
        
        Args:
            wf: Oggetto wave aperto
            framerate: Sample rate dell'audio
            
        Returns:
            str: Testo trascritto
        """
        # Crea recognizer Vosk
        rec = KaldiRecognizer(self.vosk_model, framerate)
        rec.SetWords(True)
        
        # Non logga inizio trascrizione su file
        
        # Processa audio
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                if 'text' in result and result['text'].strip():
                    results.append(result['text'].strip())
        
        # Risultato finale
        final_result = json.loads(rec.FinalResult())
        if 'text' in final_result and final_result['text'].strip():
            results.append(final_result['text'].strip())
        
        return ' '.join(results).strip()
    
    def transcribe(self, audio_file):
        """
        Trascrivi un file audio usando Vosk
        
        Args:
            audio_file: File audio da Flask request.files
            
        Returns:
            tuple: (success, result_dict)
        """
        start_time = datetime.now()
        audio_path = None
        
        # Verifica disponibilità Vosk
        if not VOSK_AVAILABLE:
            return False, {
                'error': 'Libreria Vosk non installata',
                'instructions': 'Installa con: pip install vosk'
            }
        
        if not self.is_available or self.vosk_model is None:
            return False, {
                'error': 'Modello Vosk non caricato',
                'instructions': self.error_message if self.error_message else 'Verifica la configurazione'
            }
        
        try:
            # Salva file temporaneo
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
                audio_path = temp_audio.name
                audio_file.save(audio_path)
                file_size = os.path.getsize(audio_path)
                
                # Non logga dimensione file su file
            
            # Verifica dimensione minima
            if file_size < 1000:
                if audio_path and os.path.exists(audio_path):
                    os.unlink(audio_path)
                return False, {
                    'error': 'File audio troppo piccolo o vuoto',
                    'text': ''
                }
            
            # Apri file WAV
            try:
                wf = wave.open(audio_path, "rb")
            except wave.Error as e:
                if audio_path and os.path.exists(audio_path):
                    os.unlink(audio_path)
                return False, {
                    'error': f'File WAV non valido: {str(e)}'
                }
            
            # Valida formato audio
            is_valid, error_msg = self._validate_audio_format(wf)
            if not is_valid:
                wf.close()
                if audio_path and os.path.exists(audio_path):
                    os.unlink(audio_path)
                return False, {'error': error_msg}
            
            # Processa audio
            framerate = wf.getframerate()
            full_text = self._process_audio(wf, framerate)
            
            wf.close()
            
            # Cleanup file temporaneo
            if audio_path and os.path.exists(audio_path):
                os.unlink(audio_path)
            
            # Calcola tempo di elaborazione
            elapsed = (datetime.now() - start_time).total_seconds()
            
            if full_text:
                # Non logga trascrizione su file
                
                return True, {
                    'text': full_text,
                    'language': 'it-IT',
                    'processing_time': elapsed,
                    'engine': 'vosk',
                    'word_count': len(full_text.split()),
                    'offline': True
                }
            else:
                # Non logga warning su file
                
                return False, {
                    'error': 'Nessun testo riconosciuto',
                    'text': '',
                    'processing_time': elapsed
                }
            
        except Exception as e:
            # Non logga errori su file
            
            if audio_path and os.path.exists(audio_path):
                try:
                    os.unlink(audio_path)
                except:
                    pass
            
            return False, {
                'error': f'Errore server: {str(e)}'
            }
    
    def handle_stt_request(self):
        """
        Handler per la richiesta Flask di STT
        Usa direttamente request.files di Flask
        
        Returns:
            tuple: (response, status_code) per Flask
        """
        # Verifica presenza file audio
        if 'audio' not in request.files:
            return jsonify({
                'success': False,
                'error': 'Nessun file audio fornito'
            }), 400
        
        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({
                'success': False,
                'error': 'Nome file non valido'
            }), 400
        
        # Trascrivi audio
        success, result = self.transcribe(audio_file)
        
        if success:
            return jsonify({
                'success': True,
                **result
            }), 200
        else:
            status_code = 503 if 'instructions' in result else 200
            return jsonify({
                'success': False,
                **result
            }), status_code

    def get_status(self):
        """
        Restituisce lo stato del sistema STT Vosk
        
        Returns:
            dict: Informazioni sullo stato del servizio
        """
        from datetime import datetime
        
        status_info = {
            "status": "online",
            "message": "NAO Smart AI Server - Running",
            "version": "1.0.0",
            "service": "NAO STT Server",
            "protocol": "HTTP",
            "engines": {
                "vosk": {
                    "status": "available" if self.is_available else "unavailable",
                    "description": "Offline Speech Recognition",
                    "endpoint": "/stt/vosk",
                    "offline": True
                }
            },
            "vosk_model": "vosk-model-it" if self.is_available else None,
            "timestamp": datetime.now().isoformat()
        }
        
        return status_info
    

# Esempio di utilizzo standalone
if __name__ == "__main__":
    from chat_logger import ChatLogger
    
    # Crea logger
    logger = ChatLogger()
    
    # Inizializza STT
    stt = STT(logger=logger)
    
    if stt.is_available:
        print("[OK] VoskSTT inizializzato correttamente")
    else:
        print("[ERROR] VoskSTT non disponibile")
        if stt.error_message:
            print(stt.error_message)