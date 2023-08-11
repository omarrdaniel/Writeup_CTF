# Writeup di Brooklyn Nine Nine di TryHackMe

## [Link alla macchina](https://tryhackme.com/room/brooklynninenine)

## Metodo 1
### Enumeration
Iniziamo facendo un rapido scan con nmap e notiamo che ci sono 3 servizi aperti: ssh, tcp e http. Leggiamo inoltre che il login anonimo con ftp è abilitato.

### Exploitation
### FTP
Ci dirigiamo immediatamente verso il servizio ftp e facciamo il login anonimo 'anonymous:guest'. Una volta loggati, con il comando "ls" vediamo i file disponibili e notiamo che c'è una nota per jake. La scarichiamo con il comando "get" e ne leggiamo il contenuto. Possiamo dedurre che la password sia semplice e serva per il servizio SSH per l'utente jake.
Proviamo a farne il bruteforce con hydra.

### SSH
Hydra ci da buone notizie e scopriamo la password che ci servirà per accedere al servizio SSH. Una volta loggati come jake, ci muoviamo un po' nel file system e troviamo la flag user in un file user.txt. Ora ci tocca riuscire ad ottenere la flag root per completare la sfida.

### Privilege Escalation
Con il comando sudo -l vediamo che l'utente jake ha i permessi di sudo sul comando usr/bin/less. Molto semplicemente allora potremmo dare il comando "sudo usr/bin/less /root/root.txt" per leggere il contenuto e ottenere la flag root e completare la macchina. Se volessimo invece guadagnarci una shell come root, facendo un giro su GTFOBins vediamo che è possibile ottenere una root shell a partire da /usr/bin/less se eseguito come sudo. I comandi sono i seguenti: "sudo less /etc/profile --> !/bin/sh". Ottenuta la root shell, ci basterà leggere il file root.txt

_________________________________________________________________________________________________________________________________________
## Metodo 2
Così avremmo completato la macchina, ma il creatore ci dice che ci sono due modi per ottenere le flag e completarla, quindi proviamo anche il secondo.

### HTTP
Invece che partire da FTP, sfruttiamo il servizio HTTP. Visitiamo la pagina web e non notiamo niente di interessante se non un'immagine di Brooklyn 99 molto grande. Andando a controllare il source code notiamo un commento lasciato dallo sviluppato che ci parla di steganografia. Scarichiamo la foto (/brooklyn99.jpg) tramite wget e cerchiamo di estrarre qualcosa tramite il tool steghide. Notiamo che è protetta da una password.
Allora utilizzando il tool stegcracker (che utilizzerà la rockyou.txt di default) facciamo un bruteforce della password. BINGO!. Password trovata (molto semplice come password :)).
Con steghide andiamo ad estrarre il contenuto e lo leggiamo. C'è scritta la password per l'utente "Holt".

### SSH
Effettuiamo il login tramite SSH con l'utente holt e la password appena trovata. Anche in questo caso troviamo subito la flag user all'interno della cartella dell'utente holt.

### Privilege Escalation
Con il comando sudo -l vediamo che l'utente holt può eseguire il comando /bin/nano come sudo. Anche in questo caso potremmo semplicemente scrivere sudo /bin/nano /root/root.txt per leggere solamente il file e ottenere la flag. Altrimenti, sempre cercando su GTFOBins, possiamo spawnare una root shell con il seguente comando: "sudo nano --> ^R^X (CTRL+R,CTRL+X per dire che vogliamo eseguire un comando) --> reset; sh 1>&0 2>&0". La shell viene spawnata all'interno di nano. Ora possiamo leggere il file root.txt e completare la macchina

MACCHINA COMPLETATA.
