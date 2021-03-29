import daily
import datetime
import service

from telegram.ext        import Updater
from env                 import get_env_panic
from dotenv              import load_dotenv 

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

# Carica configurazione locale
load_dotenv("./conf/.env")

# Collega prestashop
prestashop_token = get_env_panic("PRESTASHOP_TOKEN")
ps = service.connect(prestashop_token)

# Collega a telegram
telegram_token = get_env_panic("TELEGRAM_TOKEN")
updater = Updater(telegram_token, use_context=True)

# Aggiorna prestashop
product_data = service.get_random_product(ps)
service.update_category_product(ps, product_data)

# Invia ad entrambi i canali
image_token = get_env_panic("PRESTASHOP_IMAGE_TOKEN")
today = datetime.date.today()

channel_id = get_env_panic("TELEGRAM_CHANNEL_ITA")
print("[I] Sending message to " + channel_id)
daily.send_message(image_token, 0, MSG_HTML_DAILY_ITA, channel_id, product_data, 10, today, updater.bot)

channel_id = get_env_panic("TELEGRAM_CHANNEL_ENG")
print("[I] Sending message to " + channel_id)
daily.send_message(image_token, 1, MSG_HTML_DAILY_ENG, channel_id, product_data, 10, today, updater.bot)

