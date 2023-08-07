# Writeup di Year of the Rabbit di TryHackMe (p on THM)

## [Link alla macchina](https://tryhackme.com/room/yearoftherabbit)

### Enumeration
Iniziamo scannerizzando la macchina con nmap e vediamo che tre servizi sono up: FTP, SSH e HTTP.
Proviamo a fare l'anonymous login su ftp ma non funziona...
Controlliamo innanzitutto il sito web sulla porta 80 e troviamo una pagina di default di apache, nulla di interessante.
Tramite gobuster troviamo la pagina /assets e /server-status. Recandoci su /assets troviamo un video .mp4 e un foglio di stile .css.

### Exploitation
Se andiamo a leggere il file ci parla di una pagina segreta che se proviamo ad accedere ci dice di disattivare javascript.
Da firefox about:config disattiviamo l'esecuzione automatica di javascript e finiamo su una pagina e un video.
Se facciamo partire il video (con audio alto come detto nel testo della challenge), a una certa sentiamo *BURP*, quindi utilizziamo burp suite per vedere cosa succede quando effettuiamo una GET di quella pagina segreta.
Troviamo una directory intermedia nascosta. Ci accediamo e troviamo Hot_Babe.png.
La scarichiamo tramite wget (per mantenere la maggior parte dei metadati) e la analizziamo con exiftool e purtroppo nulla di interessante.
Con il comando strings tiriamo fuori tutte le stringhe e troviamo l'username per fare l'accesso ftp e una lista delle possibili password.

Facciamo un dictionary attack tramite hydra e riusciamo ad accedere al servizio FTP.
Cercando tra i file troviamo un .txt con delle credenziali (lo scarichiamo con GET).
Una volta aperto vediamo che è crittografato con "Brainfuck". Lo decodifichiamo con un qualsiasi tool online e troviamo la password per l'utente eli.

Testiamo queste credenziali sul servizio SSH e funzionano!. Al login c'è una notifica di un messaggio s3cr3t. Allora proviamo a fare locate s3cr3t e troviamo la directory di questo messaggio nascosto che, fortunatamente, contiene le credenziali dell'utente gwendoline. Tramite il comando su ci spostiamo nel suo utente e riusciamo a leggere il file user.txt e trovare la prima flag.

### Privilege Escalation
Ora dobbiamo riuscire a fare privilege escalation e leggere il file root.txt per ottenere la flag. Facendo sudo -l vediamo che l'utente gwendoline può editare il file /home/gwendoline/user.txt con usr/bin/vi con permessi sudo. Provo a cercare su GTFOBins se c'è qualche comando per exploitare /bin/vi e trovo sudo vi -c ':!/bin/sh' /dev/null ma purtroppo ci dice che non possiamo eseguire questo comando perchè non siamo root.

Dopo qualche minuto di ricerca mi imbatto nella CVE-2019-14287 che ci può venire in aiuto. Quindi adattando il comando per exploitare questa vulnerabilità al nostro caso, digito sul terminale "sudo -u#-1 /usr/bin/vi /home/gwendoline/user.txt" (con questo comando possiamo runnare vi come sudo passando come uid -1 che viene tradotto in 0 e quindi root).
A questo punto ci si apre l'editor Vim, entriamo in modalità insert digitando ":" e scriviamo !/bin/sh, facciamo invio e otteniamo una shell come root.
A questo punto ci spostiamo in /root e leggiamo il contenuto di root.txt per trovare la seconda e ultima flag

MACCHINA COMPLETATA.
