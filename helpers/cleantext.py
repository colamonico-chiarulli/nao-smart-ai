'''
Rino Andriano
cleantext 

Pulisce il testo rimuovendo emoji, caratteri speciali e normalizzando la punteggiatura.
'''
import re

def clean_text(text):
    """
    Pulisce il testo rimuovendo emoji, caratteri speciali e normalizzando la punteggiatura.
    
    Args:
        text (str): Testo da pulire
        
    Returns:
        str: Testo pulito e ottimizzato
    """
    # Rimuove emoji e caratteri speciali
    # Questo pattern copre la maggior parte degli emoji Unicode e altri simboli speciali
    text = re.sub(r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF\U00002702-\U000027B0\U000024C2-\U0001F251]+', '', text)
    
    # Rimuove emoticon testuali comuni
    text = re.sub(r'[:;=]-?[)(/\\|dpDP]', '', text)  # e.g., :) :( ;) :D :P
    
    # Rimuove spazi multipli e va a capo
    text = re.sub(r'\s+', ' ', text)
    
    # Normalizza la punteggiatura
    text = re.sub(r'(!+)', '!', text)   # Normalizza esclamazioni multiple
    text = re.sub(r'(\?+)', '?', text)  # Normalizza punti interrogativi multipli
    text = re.sub(r'(\.+)', '.', text)  # Normalizza punti multipli
    text = re.sub(r'(-+)', '-', text)   # Normalizza trattini multipli
    text = re.sub(r'(\*+)', '', text)   # Rimuove gli asterischi
    text = re.sub(r'[\[\]\(\)\{\}]', '', text)   # Rimuove le parentesi
    
    # Rimuove spazi prima della punteggiatura
    text = re.sub(r'\s+([.,!?;:])', r'\1', text)
    
    # Rimuove spazi extra
    text = text.strip()
    
    return text


# test di utilizzo
if __name__ == "__main__":
    test_text = """
    Ciao!! 😊 Come stai??? :) 
    \n\n Oggi (nota importante) è una bellissima giornata... 🌞 
    Andiamo a fare una passeggiata [ore 15:00] nel parco! 🚶‍♂️ :D 
    {nota: portare l'ombrello} *** ....
    """
    
    cleaned = clean_text(test_text)
    print("Testo originale:")
    print(test_text)
    print("\nTesto pulito:")
    print(cleaned)