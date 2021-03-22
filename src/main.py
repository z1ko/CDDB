import daily
import datetime
import service

from telegram.ext        import Updater
from env                 import get_env_panic
from dotenv              import load_dotenv 

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
today = datetime.date.today()

image_token = get_env_panic("PRESTASHOP_IMAGE_TOKEN")
daily.send_message(image_token, product_data, 10, today, updater.bot)

