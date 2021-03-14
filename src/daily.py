
from os import extsep
import xml.etree.ElementTree as ET
import urllib.request
import random

from telegram.error import TelegramError
from telegram       import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from env            import get_env_panic
from datetime       import date

# Stringa dinamica usata come prefisso dei tag
G = "http://base.google.com/ns/1.0"

# Informazioni che ci servono per ogni prodotto, non controlliamo
# che il database sia corretto... mi fido
class Product:
    def __init__(self, element: ET.Element) -> None:

        self.name         = ""
        self.link         = ""
        self.price        = 0
        self.availability = 0
        self.image_link   = ""

        e = element.find("title")
        if e != None:
            self.name = e.text
        else:
            print("[W] Il prodotto non ha il nome")

        e = element.find("link")
        if e != None:
            self.link = e.text
        else:
            print("[W] Il prodotto non ha il link al negozio")

        e = element.find("{" + G + "}price")
        if e != None:
            self.price = float(e.text.split(" ")[0])
        else:
            print("[W] Il prodotto non ha il prezzo")

        e = element.find("{" + G + "}inventory")
        if e != None:
            self.availability = int(e.text)
        else:
            print("[W] Il prodotto non ha una quantità segnata in magazzino")

        e = element.find("{" + G + "}image_link")
        if e != None:
            self.image_link = e.text
        else:
            print("[W] Il prodotto non ha il link all'immagine")

        pass
        
# Ottiene un prodotto valido dal catalogo, un prodotto per essere valido
# deve avere i link all'immagine e la pagina del negozio funzionanti ed
# essere in magazzino
def get_random_product(feed_link) -> Product:
    try:
        # Ottiene XML da prestashop e lo decodifica
        result = urllib.request.urlopen(feed_link)
        result = ET.parse(result)

        # Scorre tutti i prodotti
        products = []
        for element in result.getroot()[0].findall("item"):
            products.append(Product(element))

        # Se non ci sono prodotti allora termina
        if len(products) == 0:
            print("[E] Non ci sono prodotti nel catalogo")
            return None

        retry = 1
        while retry <= 20:
            result = random.choice(products)

            # Controlla se il link dell'immagine e del prodotto sono raggiungibili e 
            # se il prodotto sia in magazzino
            try:
                ret_code1 = urllib.request.urlopen(result.image_link).getcode()
                ret_code2 = urllib.request.urlopen(result.link).getcode()
 
                if result.availability == 0:
                    print("[W] Il prodotto scelto non è presente in inventario, ritento (x{t})...".format(t=retry))
                    result = random.choice(products)
                    retry += 1
                else:
                    print("[I] Il prodotto scelto è valido: " + result.name)
                    return result

            except:
                print("[W] Il prodotto scelto non è valido, ritento (x{t})...".format(t=retry))
                result = random.choice(products)
                retry += 1
    except:
        print("[E] Impossibile ottenere prodotto giornaliero: errore generico")
        return None

    print("[E] Impossibile ottenere prodotto giornaliero, troppi tentativi")
    return None

# =======================================================================

# Scheletro messaggio italiano
MSG_HTML_DAILY_ITA = """

⭐ <b>OFFERTA GIORNALIERA {date}</b> ⭐
<u>{name}</u>

🟠 Sconto extra:  {discount}%

<b>CODICE SCONTO:</b> {code}

"""

# Scheletro messaggio inglese
MSG_HTML_DAILY_ENG = """

⭐ <b>DAILY OFFER {date}</b> ⭐
<u>{name}</u>

🟠 Extra discount:  {discount}%

<b>DISCOUNT CODE:</b> {code}

"""


# Invia messaggio italiano per l'offerta del giorno
def send_daily_message_ita(product: Product, discount: int, today: date, bot: Bot):

    text = MSG_HTML_DAILY_ITA.format(
        discount = discount,
        name     = product.name, 
        date     = today.strftime("%d-%m-%Y"),
        code     = get_env_panic("DISCOUNT_CODE")
    )

    buttons = [[ InlineKeyboardButton("Link", url = product.link) ]]
    reply_markup = InlineKeyboardMarkup(buttons)

    channel_name  = get_env_panic("TELEGRAM_CHANNEL_ITA")
    try:
        bot.send_photo(
            chat_id = channel_name,
            photo = product.image_link,
            reply_markup = reply_markup,
            parse_mode = 'html',
            caption = text,
        )
    except TelegramError as e:
        print("[E] Errore invio messaggio daily: " + str(e))


# Invia messaggio inglese per l'offerta del giorno
def send_daily_message_eng(product: Product, discount: int, today: date, bot: Bot):

    text = MSG_HTML_DAILY_ENG.format(
        discount = discount,
        name     = product.name, 
        date     = today.strftime("%d-%m-%Y"), 
        code     = get_env_panic("DISCOUNT_CODE")
    )

    # Il link inglese è diverso
    shop_link = product.link.replace("caneva937.com/it", "caneva937.com/en")
    buttons = [[ InlineKeyboardButton("Link", url = shop_link) ]]
    reply_markup = InlineKeyboardMarkup(buttons)

    channel_name = get_env_panic("TELEGRAM_CHANNEL_ENG")
    try:
        bot.send_photo(
            chat_id = channel_name,
            photo = product.image_link,
            reply_markup = reply_markup,
            parse_mode = 'html',
            caption = text,
        )
    except TelegramError as e:
        print("[E] Errore invio messaggio daily: " + str(e))

    pass
