# Writeup di Daily Bugle di TryHackMe

## [Link alla macchina](https://tryhackme.com/room/dailybugle)

### Enumeration
Iniziamo scannerizzando la macchina con NMAP e come servizi attivi troviamo SSH, HTTP e MYSQL. Entrando nel sito web riusciamo subito a rispondere alla prima domanda.
Sulla pagina principale non troviamo niente di interessante, quindi proviamo ad usare gobuster e nikto per trovare qualcosa di un po' più juicy.
Ecco, abbiamo trovato una pagina molto interessante di nome /administrator. E' un portale di login del CMS Joomla. Cerchiamo di capire che versione monta per trovare eventuali CVE.
Tramite il tool joomscan troviamo la versione del CMS.

### Exploitation
Cercando un po' sul web e su exploit-DB/searchsploit notiamo che questa versione è vulnerabile ad SQL Injection. L'exploit su Exploit-DB ci spiega come farla tramite SQLmap, ma cercando un po' troviamo un PoC in python su github. Lo scarichiamo e lo lanciamo per ottenere lo username Jonah (superuser) e la relativa password hash. Ora ci tocca usare john the ripper per craccare questa password... dopo un tempo sconsiderevole e grazie a rockyou.txt siamo riusciti a trovare la password.
Effettuiamo il login su Joomla e cerchiamo come caricare una reverse shell.
### Rev Shell
Con un po' di ricerche scopriamo che andando su Extensions -> Templates -> Templates, selezioniamo un template e sulla destra troviamo la lista dei file. Modifichiamo il file index.php e ci mettiamo la nostra reverse shell (nel mio caso ho usato quella di PentestMonkey). Ricordiamoci di modificare i parametri relativi alla nostra macchina.
Sull'attack box lanciamo il comando nc -lvp <port> per metterci in ascolto e facciamo una richiesta a http://private_ip/index.php e vediamo che riusciamo a stabilire una connessione con la nostra macchina.
Esiste un altro utente ma non abbiamo il permesso per accedere alla sua home.
Ora che siamo dentro, girovaghiamo un po' tra i vari file finchè sotto /var/www/configuration.php troviamo una password in chiaro.
Proviamo ad utilizzare in ssh con l'utente appena trovato e vediamo che funziona. Così riusciamo a recuperare la user flag.

### Privilege Escalation
Ora dobbiamo cercare un modo per raggiungere il livello root e recuperare la flag. Subito utilizziamo il comando sudo -l e ci viene restituito che possiamo runnare come sudo il binario /usr/bin/yum. Andando a vedere su GTFObins vediamo che c'è un modo di fare privilege escalation tramite questo binario. Copiamo e incolliamo in codice proposto sulla shell di jjameson e abbiamo ottenuto una root shell con cui possiamo recuperare la root flag.

MACCHINA COMPLETATA
