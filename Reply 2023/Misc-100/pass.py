import itertools
import string
# Caratteri da utilizzare per le combinazioni
caratteri = string.ascii_letters + string.digits + string.punctuation
# Lunghezza delle combinazioni
lunghezza = 3
# Formato con gli asterischi
formato = '900802jfeng@veryrealmail.com***R3ply!'
# Nome del file in cui scrivere le combinazioni
nome_file = 'wordlist.txt'
with open(nome_file, 'w') as file:
  # Genera tutte le possibili combinazioni di 3 caratteri
  combinazioni = [''.join(p) for p in itertools.product(caratteri, repeat=lunghezza)]
  # Sostituisci gli asterischi con le combinazioni e scrivi nel file
  for combinazione in combinazioni:
    riga_modificata = formato.replace('***', combinazione, 1)
    file.write(riga_modificata + '\n')
