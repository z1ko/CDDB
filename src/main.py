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

from telegram.ext import Updater
from env          import get_env_panic
from dotenv       import load_dotenv 

# Carica configurazione locale
load_dotenv()

# Collega a telegram
token = get_env_panic("TELEGRAM_TOKEN")
updater = Updater(token, use_context=True)

# Ottiene prodotto valido
feed = get_env_panic("PRESTASHOP_FEED")
product = daily.get_random_product(feed)
if product != None:
    today = datetime.date.today()

    # Invia ad entrambi i canali
    daily.send_daily_message_ita(product, 10, today, updater.bot)
    daily.send_daily_message_eng(product, 10, today, updater.bot)