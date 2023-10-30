# Writeup di Bulletproof Penguin di TryHackMe

## [Link alla macchina](https://tryhackme.com/room/bppenguin)

Questa stanza ci permette di approfondire il processo di hardening di un server Linux, lavorando su servizi come Redis, MySQL, FTP, SSH...
Dobbiamo riuscire a fare i cambiamenti adeguati per mettere in sicurezza un servizio, al fine di guadagnare la flag relativa.

Iniziamo connettendoci alla macchina tramite ssh con i dati thm:p3ngu1n. Con il comando "get-flags" otteniamo le flag delle parti svolte.
Per ogni vulnerabilità, il testo ci fornisce una breve spiegazione e la contromisura scelta da applicare.

### Redis Server No Password
Per quanto riguarda il server Redis, dobbiamo inserire una password. Per fare ciò, andiamo a modificare il file di configurazione /etc/redis/redis.conf e andiamo a togliere il commento sulla riga "requirepass".
Una volta fatto ciò, riavviamo il servizio Redis con il comando "sudo systemctl restart redis" e digitando "get-flags", otteniamo la prima flag

### Report Default Community Names of the SNMP Agent
Ora dobbiamo modificare il community name per SNMP, in quanto "public" è troppo prevedibile.
Quindi modifichiamo il file di configurazione /etc/snmp/snmpd.conf, andando a modificare le due righe che iniziamo con rocommunity e rocommunity6.
Riavviamo il servizio "sudo systemctl restart snmpd.service" e otteniamo la flag

### Nginx Running as Root
Per runnare il server Nginx non è consigliato utilizzare l'utente root, in quanto potrebbe essere usato in modo malevolo da un attaccante.
Andiamo quindi a modificare il file di configurazione /etc/nginx/nginx.conf per eseguirlo come l'utente www-data (cambiamo "user root" con "user www-data").
Riavviamo il servizio con "sudo systemctl restart nginx.service" per ottenere la flag.

### Cleartext Protocols
Ci viene detto che bisogna disattivare il servizio telnet e il servizio che runna sulla porta 69 UDP in quanto lasciano viaggiare il traffico in chiaro.
Per scoprire cosa runna sulla porta 69 UDP utilizziamo NMAP e scopriamo che si tratta di tftp.
Tramite il comando "sudo lsof -i" che ci permette di vedere i file aperti dai vari processi, scopriamo che sia telnet che tftp hanno la propria configurazione nel file inetd.
Allora andiamo ad editare il file /etc/inetd.conf, commentando la riga relativa a telnet e a tftp.

### Weak SSH Crypto
Per questa task ci viene detto che il protocollo ssh utilizza degli algoritmi di crittografia deboli.
Per completare questo punto, dobbiamo modificare il file /etc/ssh/sshd_config e rimuovere dalla lista presente i protocolli considerati non sicuri.
Anche in questo caso restartiamo il servizio tramite "sudo systemctl restard sshd.service" per ottenere la flag tramite il comando "get-flags"

### Anonymous FTP Logging
Dobbiamo disattivare l'accesso anonimo su FTP in quanto espone un file segreto al pubblico.
Anche in questo caso possiamo risolvere semplicemente questa issue modificando il file di configurazione di ftp, modificando da YES a NO nella riga "anonymous_enable"

### Weak Passwords
In questa task dobbiamo modificare le password degli utenti "mary" e "munra" perchè sono state trovate all'interno di un leak di password. Per fare ciò sfruttiamo il comando "sudo passwd [username]"
Inoltre ci viene chiesto di rimuovere gli utenti "john" e "test1". Possiamo farlo con il comando "sudo deluser [username]" così da recuperare le due flags.

### Review Sudo Permissions
Anche in questo caso dobbiamo fare due cose: togliere tutti i privilegi SUDO all'utente munra e dare il permesso di runnare /usr/bin/ss come root all'utente mary senza bisogno di chiedere la password.
Per completare il primo punto, modifichiamo il file /etc/sudoers con l'editor visudo (come suggerito nel testo della challenge per evitare incompatibilità), commentando la riga relativa all'utente munra.
Per il secondo punto creiamo, sempre nel file /etc/sudoers tramite visudo, una riga per l'utente mary con il seguente contenuto "mary ALL=(root) NOPASSWD:/usr/bin/ss"

### Exposed Database Ports
In questa task dobbiamo modificare i file di configurazione MySQL e Redis per bindare la porta solo sul localhost (e non più pubbliche in quanto sono servizi che vengono usati solo internamente).
Per quanto riguarda MySQL, tramite il file di configurazione /etc/mysql/mysql.conf.d/mysql.conf, aggiungiamo la riga "bind 127.0.0.1" e riavviamo il servizio.
Per Redis, invece, sempre tramite il file di configurazione /etc/redis/redis.conf, aggiungiamo la riga "bind 127.0.0.1" per ottenere le ultime due flags.

MACCHINA COMPLETATA.
