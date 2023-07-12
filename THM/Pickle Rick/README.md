##Writeup di Pickle Rick di TryHackMe

(Link alla macchina)[https://tryhackme.com/room/picklerick]

Partiamo con la fase di enumeration usando nmap (nmap -sV IP), nikto (nikto -h IP) e dirbuster (dirb http://IP). Con nikto scopriamo che c'è una pagina di login a /login.php e con dirbuster troviamo il file robots.txt di interessanti.

Recandoci sulla pagina web non si trova nulla di interessante. Proviamo ad ispezionare la pagina e leggere il codice e troviamo uno Username. Proviamo a visitare la pagina /robots.txt e troviamo una stringa strana che potrebbe funziona da password.

Andiamo sulla pagina /login.php, proviamo ad inserire i dati e... SBAM! siamo dentro.

Troviamo una box che ci permette di inserire un input. Testiamo se è vulnerabile a code injection con un semplice "ls". Notiamo un file sospetto "Sup3rS3cretPickl3Ingred.txt" che potrebbe contenere il primo ingrediente. Se proviamo a fare un semplice cat, il sito ci ritorna una risposta negativa e il comando viene bloccato. Allora, per aggirare questa cosa, accediamo direttamente al file /Sup3rS3cretPickl3Ingred.txt e troviamo il primo ingrediente.

Passiamo al secondo... Oltre al file contenente il primo ingrediente, c'è un altro file interessante "clue.txt" che ci dice "Look around the file system for the other ingredient". Quindi probabilmente ci sarà una vulnerabilità di tipo Directory Traversal per vedere altre parti del sistema.
Per testare se ciò è vero, diamo come comando ls .. e vediamo che funziona. Allora ci conviene spostarsi nel file system alla ricerca di qualcosa di interessante.

Spostiamoci alla root directory con cd ../../../../; ls -lah; pwd, stampiamo la lista dei file in modalità estesa e anche la directory corrente per essere sicuri di dove ci troviamo. Ci sono molte cartelle, ma quelle più interessanti sono home e root (accessibile da root).

Inziamo dalla cartella home: spostandoci all'interno di /home troviamo altre due subdirectory, "rick" e "ubuntu". Rick sembra quella più interessante. Se listiamo i file all'interno di questa folder troviamo un file chiamato "second ingredient". Visto che cat è bloccato, proviamo con less "second ingredient" (usiamo le virgolette siccome c'è uno spazio nel nome). Siamo riusciti a recuperare il secondo ingrediente.

Ora concentriamoci sulla cartella di root. Con il comando sudo -l per vedere quali privilegi abbiamo (ci serve fare Privilege Escalation per accedere alla cartella root). Buona notizia, tutti i comandi sudo possono essere eseguiti senza password (ALL NOPASSWD: ALL)!.
Listiamo i file all'interno della cartella root con sudo ls /root e troviamo il file "3rd.txt". Sempre tramite il comando less leggiamo il file e troviamo il terzo e ultimo ingrediente.

MACCHINA COMPLETATA.
