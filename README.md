# CDDB - Caneva Daily Discount Bot

Questo semplice bot una volta avviato ottiene un prodotto casuale dal database di prestashop e genera un messaggio di offerta giornaliera sui canali telegram indicati con un link alla pagina del negozio.

## Installazione e Distribuzione - Docker

Per scaricare il programma e creare un immagine docker chiamata **cddb** basta questo:

```
git clone https://github.com/z1ko/CDDB.git
cd CDDB

docker build . -t cddb
```

Per eseguire l'immagine in un container e poi eliminarlo:

```
docker run --rm cddb
```

## Configurazione

La configurazione avviene tramite un file **.env**, al suo interno
sono presenti tutte le variabili necessarie al corretto funzionamento del bot e altre configurazioni varie. Al momento dell'installazione sono vuote per sicurezza.

| Variabile | Descrizione |
| - | - |
| TELEGRAM_TOKEN | Token che il bot usa su telegram, ottenuto da *@BotFather*. |
| PRESTASHOP_FEED | Link al feed di prestashop per scaricare il catalogo usando il modulo di Facebook. |
| TELEGRAM_CHANNEL_XXX | Nome del canali dove inviare il messaggio di offerta, nella forma *@NomeCanale*, divisi per italiano e inglese. |
| DISCOUNT_CODE  | Codice da inserire ad ogni messaggio, utilizzabile poi nel negozio. |

## Cronjob

Solitamente il bot deve essere eseguito uno volta al giorno, per questo basta creare una regola per cron, ad esempio per eseguire il bot **ogni giorno alle 2 di notte** tramite docker container:

```
0 2 * * * docker run --rm cddb
```

## TODO

Le seguenti features sono pianificate:

- [ ] Webscapper per eliminare il bisogno di cambiare manualmente le tag su prestashop (Moduli di prestashop sono ***cursati*** e non voglio toccarli) 
- [ ] File di configurazione per il layout del messaggio promozionale
- [x] Easter egg 

