# CDDB - Caneva Daily Discount Bot

Questo semplice bot una volta avviato ottiene un prodotto casuale dal database di prestashop e genera un messaggio di offerta giornaliera sui canali telegram indicati con un link alla pagina del negozio.

## Installazione e Distribuzione - Docker

Per scaricare il programma e creare un immagine docker chiamata **CDDB_IMAGE** basta questo:

```
git clone <this> 
cd CDDB

docker build -t CDDB_IMAGE
```

Per eseguire l'immagine in un container chiamato **CDDB**:

```
docker run -name CDDB CDDB_IMAGE
```

## Configurazione

La configurazione avviene tramite un file **.env**, al suo interno
sono presenti tutte le variabili necessarie al corretto funzionamento del bot e altre configurazioni varie. Al momento dell'installazione sono vuote per sicurezza.

| Variabile | Descrizione |
| - | - |
| TELEGRAM_TOKEN | Token che il bot usa su telegram, ottenuto da *@BotFather*. |
| PRESTASHOP_FEED | Link al feed di prestashop per scaricare il catalogo usando il modulo di Facebook. |
| TELEGRAM_CHANNEL_XXX | Nome del canali dove inviare il messaggio di offerta, nella forma *@NomeCanale*, divisi per italiano e inglese. |


## Cronjob

Solitamente il bot deve essere eseguito uno volta al giorno, per questo basta creare una regola per cronjob, ad esempio per eseguire il bot **ogni giorno alle 2 di notte** tramite docker container:

```
0 2 * * * docker run --name CDDB CDDB_IMAGE
```