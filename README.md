# CDDB - Caneva Daily Discount Bot

Questo semplice bot una volta avviato ottiene un prodotto casuale dal database di Prestashop e genera un messaggio di offerta giornaliera sui canali telegram indicati con un link alla pagina del negozio. Inoltre tramite un webdriver accede al sito di Prestashop per amministrare la categoria di riferimento del codice sconto aggiungendo e rimuovendo prodotti. 

## Installazione e Distribuzione - Docker

Per scaricare il programma e creare un immagine docker chiamata **cddb** basta questo:

```
git clone https://github.com/z1ko/CDDB.git
cd CDDB

docker build . -t cddb
```

Per eseguire l'immagine in un container e poi eliminarlo:

```
docker run --rm -v <config-path>:/code cddb
```

## Configurazione

La configurazione avviene tramite un file **.env**, al suo interno
sono presenti tutte le variabili necessarie al corretto funzionamento del bot e altre configurazioni varie. Al momento dell'installazione sono vuote per sicurezza.

| Variabile | Descrizione |
| - | - |
| TELEGRAM_TOKEN | Token che il bot usa su telegram, ottenuto da *@BotFather*. |
| PRESTASHOP_FEED | Link al feed di Prestashop per scaricare il catalogo usando il modulo di Facebook. |
| PRESTASHOP_EMAIL | Email per accedere alla console admin di Prestashop |
| PRESTASHOP_PASSW | Password per accedere alla console admin di Prestashop |
| DISCOUNT_CODE  | Codice da inserire ad ogni messaggio, utilizzabile poi nel negozio. |
| TELEGRAM_CHANNEL_XXX | Nome del canali dove inviare il messaggio di offerta, nella forma *@NomeCanale*, divisi per italiano e inglese. |
| LAST_PRODUCT_PATH | Percorso per il file storico contenente il nome dell'ultimo prodotto in offerta attivo, necessario per rimuoverlo dalla categoria daily quando viene scelta una nuova offerta. |


## Cronjob

Solitamente il bot deve essere eseguito una volta al giorno, per questo basta creare una regola per cron, ad esempio per eseguire il bot **ogni giorno alle 2 di notte** tramite docker container:

```
0 2 * * * docker run --rm cddb
```

## TODO

Le seguenti features sono pianificate:

- [x] Webscapper per eliminare il bisogno di cambiare manualmente le tag su prestashop (Moduli di prestashop sono ***cursati*** e non voglio toccarli) 
- [ ] File di configurazione per il layout del messaggio promozionale
- [x] Easter egg 

