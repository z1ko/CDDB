
from os import extsep
import xml.etree.ElementTree as ET
import urllib.request
import random

from telegram.error import TelegramError
from telegram       import InlineKeyboardButton, InlineKeyboardMarkup, Bot
from env            import get_env_panic
from datetime       import date


# Template per ottenere il link alla pagina del negozio di un prodotto
PRESTASHOP_PRODUCT_LINK = "www.caneva937.com/index.php?id_product={id}&controller=product"

# Template per ottenere il link all'immagine di base di un prodotto, richiede chiave API per le immagini
PRESTASHOP_PRODUCT_IMAGE_LINK = "https://caneva937.com/api/images/products/{id}/{image_id}?ws_key={api_key}"

def send_message(image_token, template: str, channel_id: str, product_data, discount: int, today: date, bot: Bot):
    product = product_data['product']

    text = template.format(
        discount = discount,
        name     = product['meta_title']['language'][0]['value'], 
        date     = today.strftime("%d-%m-%Y"),
        code     = get_env_panic("DISCOUNT_CODE")
    )

    shop_link = PRESTASHOP_PRODUCT_LINK.format(id = product['id'])
    buttons = [[ InlineKeyboardButton("Link", url = shop_link) ]]
    reply_markup = InlineKeyboardMarkup(buttons)
    
    # Ottiene link immagine
    image_id = product['id_default_image']['value']
    image_link = PRESTASHOP_PRODUCT_IMAGE_LINK.format(
            api_key = image_token,
            image_id = image_id, 
            id = product['id'], 
    )

    print("[I] link_immagine = " + image_link)
    try:
        bot.send_photo(
            chat_id = channel_id,
            photo = image_link,
            reply_markup = reply_markup,
            parse_mode = 'html',
            caption = text,
        )
    except TelegramError as e:
        print("[E] Errore invio messaggio daily: " + str(e))
