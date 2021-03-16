# MIT License
# 
# Copyright (c) 2021 Filippo Ziche <filippo.ziche@gmail.com>
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import daily
import datetime
import automaton

from telegram.ext import Updater
from env          import get_env_panic
from dotenv       import load_dotenv 

# Carica configurazione locale
load_dotenv("./conf/.env")

# Collega a telegram
token = get_env_panic("TELEGRAM_TOKEN")
updater = Updater(token, use_context=True)

# Ottiene prodotto valido
feed = get_env_panic("PRESTASHOP_FEED")
product = daily.get_random_product(feed)
if product != None:

    # Prova ad aggiungere il prodotto alla categoria daily
    try:
        # Percorso al file storico
        path = get_env_panic("LAST_PRODUCT_PATH")

        # Carica nome del precedente prodotto da rimuovere dalla DAILY
        with open(path, "r+") as last_product_file:
            print("[I] Trovato file storico!")

            old_product_name = last_product_file.readline().strip()
            remove_old = True

            if old_product_name == '':
                print("[W] Non è stata trovata una vecchia offerta da sostituire")
                remove_old = False
            else:
                print("[I] Ottenuto vecchio prodotto in offerta: " + old_product_name)

            # Ottiene credenziali di accesso
            login_email = get_env_panic("PRESTASHOP_EMAIL")
            login_passw = get_env_panic("PRESTASHOP_PASSW")

            print("[I] Avvio sequenza di settaggio categoria daily per " + product.name + " al posto di " + old_product_name)
            automaton.prestashop_set_daily(old_product_name, product.name, login_email, login_passw, remove_old)

            # Rimpiazza il vecchio nome
            last_product_file.seek(0)
            last_product_file.write(product.name)
            last_product_file.truncate()

            print("[I] Salvato nuovo nome prodotto in memoria: " + product.name)
            
    except IOError as e:
        print("[E] Errore apertura file storico: " + str(e))
        exit(1)

    except Exception as e:
        # TODO: Avverti della gravità della situazione
        print("[E] Errore generico durante la modifica della categoria DAILY su prestashop: " + str(e))
        exit(1)

    today = datetime.date.today()

    # Invia ad entrambi i canali
    daily.send_daily_message_ita(product, 10, today, updater.bot)
    daily.send_daily_message_eng(product, 10, today, updater.bot)
