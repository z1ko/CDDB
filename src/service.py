#
# Questo è l'assalto finale al castello, l'ultima speranza 
# dell'umanità
#

import random

from prestapyt           import PrestaShopWebServiceDict
from prestapyt.prestapyt import PrestaShopAuthenticationError

# ID della categoria DAILY
PRESTASHOP_DAILY_ID = 146

# Template per ottenere il link alla pagina del negozio di un prodotto
PRESTASHOP_PRODUCT_LINK = "www.caneva937.com/index.php?id_product={id}&controller=product"

# Ottiene connessione a prestashop
def connect(token: str):
    try:
        ps = PrestaShopWebServiceDict('https://caneva937.com/api', token)
        return ps
    except:
        print("[E] Errore collegamento a prestashop")
        exit(1)


# Ottiene informazioni prodotto
def __get_product_data(ps, id: str):

    try:
        data = ps.get('products', id)
    except:
        print("[E] Errore ottenimento prodotto dal webservice")
        exit(1)

    product = data['product']
    qnt = product['quantity']

    # Rimuove elementi non scrivibili e che causano errori
    product.pop('manufacturer_name')
    product.pop('position_in_category') # <- altrimenti si bugga
    product.pop('quantity')

    return (data, qnt)


# Rimuove la categoria DAILY
def __remove_daily_category(data):

    categories = data["product"]["associations"]["categories"]['category']
    num = len(categories)

    if num >= 2:
        for i in range(num):
            if categories[i]['id'] == str(PRESTASHOP_DAILY_ID):
                del categories[i]


# Aggiunge la categoria DAILY
def __insert_daily_category(data):

    categories = data["product"]["associations"]["categories"]
    if len(categories['category']) != 1:
        print("[E] Prodotto non DAILY ha più di una categoria: non supportato.")
        exit(1)

    prev_category_id = categories['category']['id']
    categories.pop('category')

    categories['category'] = [{'id' : PRESTASHOP_DAILY_ID}, {'id': prev_category_id}]


# Ottiene precedente offerta DAILY
def __get_previous_product(ps) -> str:

    try:
        data = ps.get('categories', PRESTASHOP_DAILY_ID)
    except:
        print("[E] Errore ottenimento categoria daily dal webservice")
        exit(1)

    product = data['category']['associations']['products']['product']
    return product['id']

# Aggiorna categoria del prodotto
def update_category_product(ps, new_product):

    # Ottiene ID del prodotto precedentemente in categoria DAILY
    # e lo rimuove dalla categoria
    old_id = __get_previous_product(ps)
    (old_product, _) = __get_product_data(ps, old_id)
    __remove_daily_category(old_product)

    # Aggiunge nuovo prodotto alla categoria DAILY
    __insert_daily_category(new_product)

    # Aggiorna alla fine per evitare stati incoerenti
    ps.edit('products', old_product)
    ps.edit('products', new_product)

#



# Ottiene prodotto casuale dalla lista
def get_random_product(ps):

    # Ottiene lista prodotti
    try:
        products = ps.search('products')
    except PrestaShopAuthenticationError as e:
        print("[E] Errore ottenimento catalogo dal webservice:" + str(e))
        exit(1)

    num = len(products)
    print("[I] Trovati " + str(num) + " prodotti")

    # Scegliamo a caso un prodotto, confermiamo il suo funzionamento
    # e al limite ne proviamo a scegliere un'altro (TODO)

    found = False
    while not found:
      
        id = random.choice(products)
        print("[I] Controllo prodotto " + str(id))
        (product_data, qnt) = __get_product_data(ps, id)
        product = product_data['product']
    
        # Solo prodotti attivi
        if product['active'] != '1':
            continue

        # Solo prodotti presenti in magazzino
        if product['available_for_order'] == '0':
            continue

        # Solo prodotti con un nome
        if product['meta_title']['language'][0]['value'] == '':
            continue

        found = True


    link = PRESTASHOP_PRODUCT_LINK.format(id = product['id'])
    print("[I] Prodotto {a}, link_shop: {b}".format(a = product['id'], b = link))
    return product_data
