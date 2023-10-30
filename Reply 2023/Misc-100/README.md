La challenge ci fornisce un'email da uno studio dentistico. Leggendo l'email, viene citato prima un file zip (purtroppo protetto da password)

"In order to provide you with the necessary information for 
addressing this concern, we have attached a detailed report in a 
ZIP file. Please find the attached ZIP file for further instructions 
and recommendations from our team. To access the contents of 
the ZIP file, you will need the password, that is the last one we 
shared."

e successivamente una ricevuta (allegata come immagine), con un indizio di controllarne i metadati.

" Please, be sure to take a look at the attached receipt, taking care 
to save a copy locally and check that all of the (m)data is correct."

Nell'email troviamo l'encoding BASE64 dell'archivio ZIP e anche dell'immagine corrispondente alla ricevuta.

Iniziamo a convertire da BASE64 a file sia l'archivio compresso che l'immagine .png tramite "base64.guru".
Analizzando i metadati della ricevuta, come indicato, tramite exiftool, troviamo dei campi interessanti:
	- artist:  birthDateMail***R3ply!
	- copyright: checkArtistFieldForPwdFormat
Ottimo, abbiamo il formato della password per l'archivio zip.

Dopo un po' di ragionamento e dopo aver letto più e più volte il testo dell'email, ci siamo accorti dell'ultima riga di testo presente " _______________________________R3ply!" da 37 caratteri che potrebbe essere la possibile lunghezza della password.
Inoltre il creatore della challenge ci ha fornito l'hint sul format della data di nascita, che deve essere "yymmdd".
Facendo affidamento su questa nostra intuizione e sfruttando il consiglio dato dal creatore della CTF, abbiamo appuntato un possibile template per la password: " 900802jfeng@veryrealmail.com***R3ply!"

Ora non ci resta che creare uno script python per generare tutte le possibili password, utilizzando tutti i possibili caratteri al posto dei tre asterischi (sì, abbiamo provato la password lasciando gli asterischi e non funziona :( ) --> file pass.py

Una volta che la nostra wordlist è stata generata, lanciato un attacco a dizionare tramite il tool john the ripper contro l'archivio zip e... BOOM! Password trovata e di conseguenza anche la flag contenuta nell'archivio.
