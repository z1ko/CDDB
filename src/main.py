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
import service

from telegram.ext        import Updater
from env                 import get_env_panic
from dotenv              import load_dotenv 
from prestapyt           import PrestaShopWebServiceDict
from prestapyt.prestapyt import PrestaShopAuthenticationError

# Carica configurazione locale
load_dotenv("./conf/.env")

# Collega prestashop
try:
    prestashop_token = get_env_panic("PRESTASHOP_TOKEN")
    ps = PrestaShopWebServiceDict('https://caneva937.com/api', prestashop_token)

except PrestaShopAuthenticationError as e:
    print("[E] Errore collegamento a prestashop: " + str(e))

# Collega a telegram
telegram_token = get_env_panic("TELEGRAM_TOKEN")
updater = Updater(telegram_token, use_context=True)

# Aggiorna prestashop
product_data = service.get_random_product(ps)
service.update_category_product(ps, product_data)

# Invia ad entrambi i canali
today = datetime.date.today()
daily.send_message(product_data, 10, today, updater.bot)