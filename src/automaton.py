
from time                                    import sleep
from pyvirtualdisplay                        import Display
from selenium                                import webdriver
from selenium.webdriver.support.ui           import WebDriverWait
from selenium.common.exceptions              import TimeoutException
from selenium.webdriver.support              import expected_conditions as EC
from selenium.webdriver.chrome.options       import Options
from selenium.webdriver.common.by            import By
from selenium.common.exceptions              import WebDriverException

# Secondi da aspettare per il caricamento di ogni elemento 
# sono molto generoso coi tempi, tanto alle 1 di notte non c'è
# fretta nell'aspettare il caricamento 
TIMEOUT_SEC = 180

# Aggiunge prodotto alla categoria DAILY
def prestashop_set_daily(old_product_name: str, new_product_name: str, login_email: str, login_passw: str, remove_old = True):

    #display = Display(visible = 0, size = (1920, 1080))
    #display.start()

    options = Options()
    options.add_argument("--headless")
    options.Headless = True

    print("[I] Creazione webdriver Chrome... ", end = '', flush = True)
    driver = webdriver.Chrome(executable_path = "/usr/bin/chromedriver", chrome_options = options)
    print("completato.")

    print("[I] Login in prestashop... ", end = '', flush = True)
    __login(driver, login_email, login_passw)
    print("completato.")

    print("[I] Accesso alla lista dei prodotti (potrebbe metterci un po')... ", end = '', flush = True)
    __visit_products_list_page(driver)
    print("completato.")

    print("[I] Accesso alla pagina " + new_product_name + "... ", end = '', flush = True)
    __visit_product_page(driver, new_product_name)
    print("completato.")

    print("[I] Settaggio della categoria DAILY a " + new_product_name + "... ", end = '', flush = True)
    __flip_save_daily_category(driver)
    print("completato.")

    # Rimuove il precedente prodotto solo se richiesto
    if remove_old:

        print("[I] Accesso alla lista dei prodotti... ", end = '', flush = True)
        __visit_products_list_page(driver)
        print("completato.")

        print("[I] Accesso alla pagina di " + old_product_name + "... ", end = '', flush = True)
        __visit_product_page(driver, old_product_name)
        print("completato.")

        print("[I] Rimozione della categoria DAILY di " + old_product_name + "... ", end = '', flush = True)
        __flip_save_daily_category(driver)
        print("completato.")

    print("[I] Chiusura webdriver")
    driver.quit()


# Crea crawler ed esegue login
def __login(driver, login_email, login_passw):

    driver.get("https://www.caneva937.com/admin21/")

    email = driver.find_element_by_id("email")
    passw = driver.find_element_by_id("passwd")
    buttn = driver.find_element_by_id("submit_login")

    email.send_keys(login_email)
    passw.send_keys(login_passw)

    buttn.click()

# Va nella sezione prodotti
def __visit_products_list_page(driver):

    # Attente il caricamento della pagina...
    try:
        condition = EC.presence_of_element_located((By.ID, "subtab-AdminCatalog"))
        WebDriverWait(driver, timeout = TIMEOUT_SEC).until(condition)

    except TimeoutException:
        print("[E] Timeout caricamento pagina")
        return

    catalog = driver.find_element_by_id("subtab-AdminCatalog")
    catalog = catalog.find_element_by_tag_name("a")

    link = catalog.get_attribute('href')
    print("[I] Link = " + link)
    driver.get(link)

# Va nella pagina del prodotto
def __visit_product_page(driver, product_name: str):
    print("[I] Ottenimento colonna filtro\n")

    # Attente il caricamento della pagina...
    #try:
    #    condition = EC.visibility_of_element_located((By.NAME, "filter_column_name"))
    #    WebDriverWait(driver, timeout = TIMEOUT_SEC).until(condition)
    #
    #except TimeoutException:
    #    print("[E] Timeout caricamento pagina")
    #    return

    # Resettiamo il filtro per evitare ricerche passate non cancellate
    sleep(5)
    print("[I] Resettaggio filtro al default\n")
    
    #f1 = driver.find_element_by_id("filter_column_id_product_min")
    #f2 = driver.find_element_by_id("filter_column_id_product_max")
    #f3 = driver.find_element_by_name("filter_column_reference")
    #f4 = driver.find_element_by_name("filter_column_name_category")
    #f5 = driver.find_element_by_id("filter_column_price_min")
    #f6 = driver.find_element_by_id("filter_column_price_max")
    #f7 = driver.find_element_by_id("filter_column_sav_quantity_min")
    #f8 = driver.find_element_by_id("filter_column_sav_quantity_max")

    #f1.clear()
    #f2.clear()
    #f3.clear()
    #f4.clear()
    #f5.clear()
    #f6.clear()
    #f7.clear()
    #f8.clear()

    print("[I] Inserimento dati ricerca\n")
    filter = driver.find_element_by_name("filter_column_name")
    button = driver.find_element_by_name("products_filter_submit")

    filter.clear()
    filter.send_keys(product_name)
    button.click()

    # Attente il caricamento della pagina...
    try:
        print("[I] Ricerca in corso\n")
        condition = EC.presence_of_element_located((By.LINK_TEXT, product_name))
        WebDriverWait(driver, timeout = TIMEOUT_SEC).until(condition)

    except TimeoutException:
        print("[E] Timeout caricamento pagina")
        return

    print("[I] Prodotto trovato\n")
    item = driver.find_element_by_link_text(product_name)
    link = item.get_attribute("href") 
    driver.get(link)

DAILY_CHECKBOX_XPATH = "//input[@value='146' and @type='checkbox']"
SAVE_BUTTON_XPATH = "//button[@type = 'submit' and span[text() = 'Salva']]"

# Setta la categoria daily per il prodotto
def __flip_save_daily_category(driver):

    # Attente il caricamento della pagina...
    try:
        condition = EC.presence_of_element_located((By.XPATH, DAILY_CHECKBOX_XPATH))
        WebDriverWait(driver, timeout = TIMEOUT_SEC).until(condition)

    except TimeoutException:
        print("[E] Timeout caricamento pagina")
        return

    checkbox = driver.find_element_by_xpath(DAILY_CHECKBOX_XPATH)
    save = driver.find_element_by_xpath(SAVE_BUTTON_XPATH)
    
    # Scrolliamo la pagina fino al fondo, speriamo di trovarlo
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    
    try:
        condition = EC.element_to_be_clickable((By.XPATH, DAILY_CHECKBOX_XPATH))
        WebDriverWait(driver, timeout = TIMEOUT_SEC).until(condition)

    except TimeoutException:
        print("[E] AGAGAGA")
        return

    # Qualche errore strano per la troppa velocità, ma così funziona
    sleep(2)
    #driver.execute_script("arguments[0].click();", checkbox)
    checkbox.click()
    sleep(2)
    #driver.execute_script("arguments[0].click();", save)
    save.click()
    sleep(2)


