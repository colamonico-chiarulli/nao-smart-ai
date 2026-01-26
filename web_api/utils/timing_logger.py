"""
File:   /web_api/utils/timing_logger.py
-----
Utility per registrare statistiche di timing delle operazioni STT/LLM
Salva le statistiche in un file CSV per analisi successive.
-----
@author  Rino Andriano <andriano@colamonicochiarulli.edu.it>
@copyright    (c)2026 Rino Andriano
Created Date: Sunday, January 26th 2026
-----
@license    https://www.gnu.org/licenses/agpl-3.0.html AGPL 3.0
------------------------------------------------------------------------------
"""

import os
import csv
import time
import threading
from datetime import datetime

# ============================================================================
# FLAG DI CONTROLLO - Commentare per disabilitare il timing
# ============================================================================
TIMING_ENABLED = True
# TIMING_ENABLED = False  # Decommentare questa riga per disabilitare
# ============================================================================


class TimingLogger:
    """
    Classe per registrare e analizzare statistiche di timing.
    Thread-safe per uso in ambiente Flask multi-thread.
    """
    
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls, *args, **kwargs):
        """Singleton pattern per avere una sola istanza in tutta l'app"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, logs_dir="logs"):
        """
        Inizializza il TimingLogger
        
        Args:
            logs_dir: Directory per i file CSV (relativa a web_api)
        """
        if hasattr(self, '_initialized'):
            return
            
        self._initialized = True
        self._write_lock = threading.Lock()
        
        # Determina percorso assoluto logs
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.logs_dir = os.path.join(current_dir, logs_dir)
        
        # Crea directory se non esiste
        if not os.path.exists(self.logs_dir):
            os.makedirs(self.logs_dir)
        
        self.csv_path = os.path.join(self.logs_dir, "timing_stats.csv")
        
        # Inizializza CSV con header se non esiste
        if not os.path.exists(self.csv_path):
            self._write_csv_header()
        
        # Statistiche in memoria per endpoint /timing/stats
        self._stats_cache = []
        self._max_cache_size = 1000  # Mantieni ultime 1000 richieste in memoria
    
    def _write_csv_header(self):
        """Scrive l'header del file CSV"""
        with open(self.csv_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp',
                'chat_id',
                'audio_prep_ms',
                'stt_ms',
                'llm_ms',
                'total_server_ms',
                'transcription_length',
                'response_length'
            ])
    
    def record_timing(self, timing_data: dict):
        """
        Registra una entry di timing nel CSV e nella cache.
        
        Args:
            timing_data: Dizionario con i dati di timing:
                - chat_id: ID della chat
                - audio_prep_ms: Tempo preparazione audio (ms)
                - stt_ms: Tempo trascrizione STT (ms)
                - llm_ms: Tempo risposta LLM (ms)
                - transcription_length: Lunghezza testo trascritto
                - response_length: Lunghezza risposta LLM
        """
        if not TIMING_ENABLED:
            return
            
        timestamp = datetime.now().isoformat()
        
        # Calcola totale
        total_ms = (
            timing_data.get('audio_prep_ms', 0) +
            timing_data.get('stt_ms', 0) +
            timing_data.get('llm_ms', 0)
        )
        
        row = {
            'timestamp': timestamp,
            'chat_id': timing_data.get('chat_id', ''),
            'audio_prep_ms': round(timing_data.get('audio_prep_ms', 0), 1),
            'stt_ms': round(timing_data.get('stt_ms', 0), 1),
            'llm_ms': round(timing_data.get('llm_ms', 0), 1),
            'total_server_ms': round(total_ms, 1),
            'transcription_length': timing_data.get('transcription_length', 0),
            'response_length': timing_data.get('response_length', 0)
        }
        
        # Scrivi su CSV (thread-safe)
        with self._write_lock:
            with open(self.csv_path, 'a', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=row.keys())
                writer.writerow(row)
            
            # Aggiorna cache in memoria
            self._stats_cache.append(row)
            if len(self._stats_cache) > self._max_cache_size:
                self._stats_cache = self._stats_cache[-self._max_cache_size:]
    
    def get_stats_summary(self, last_n: int = 100) -> dict:
        """
        Calcola statistiche aggregate sulle ultime N richieste.
        
        Args:
            last_n: Numero di richieste da analizzare
            
        Returns:
            dict: Statistiche aggregate (min, max, avg, count)
        """
        if not TIMING_ENABLED:
            return {'enabled': False, 'message': 'Timing disabled'}
            
        # Prendi ultime N entries dalla cache
        entries = self._stats_cache[-last_n:] if self._stats_cache else []
        
        if not entries:
            return {
                'enabled': True,
                'count': 0,
                'message': 'Nessun dato disponibile'
            }
        
        # Calcola statistiche per ogni metrica
        metrics = ['audio_prep_ms', 'stt_ms', 'llm_ms', 'total_server_ms']
        stats = {}
        
        for metric in metrics:
            values = [e[metric] for e in entries if e.get(metric, 0) > 0]
            if values:
                stats[metric] = {
                    'min': round(min(values), 1),
                    'max': round(max(values), 1),
                    'avg': round(sum(values) / len(values), 1),
                    'count': len(values)
                }
            else:
                stats[metric] = {'min': 0, 'max': 0, 'avg': 0, 'count': 0}
        
        return {
            'enabled': True,
            'analyzed_requests': len(entries),
            'total_recorded': len(self._stats_cache),
            'csv_path': self.csv_path,
            'metrics': stats,
            'last_entry': entries[-1] if entries else None
        }
    
    def clear_stats(self):
        """Resetta le statistiche in memoria (non cancella il CSV)"""
        with self._write_lock:
            self._stats_cache = []
        return True


class TimingContext:
    """
    Context manager per misurare tempi di esecuzione.
    
    Uso:
        with TimingContext() as timer:
            # codice da misurare
        elapsed_ms = timer.elapsed_ms
    """
    
    def __init__(self):
        self.start_time = None
        self.end_time = None
        self.elapsed_ms = 0
    
    def __enter__(self):
        if TIMING_ENABLED:
            self.start_time = time.perf_counter()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if TIMING_ENABLED and self.start_time:
            self.end_time = time.perf_counter()
            self.elapsed_ms = (self.end_time - self.start_time) * 1000
        return False


# Istanza globale (singleton)
timing_logger = TimingLogger()
