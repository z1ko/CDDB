
from daily                                     import Product, get_random_product
from selenium                                  import webdriver
from selenium.webdriver.support.ui             import WebDriverWait

# Aggiunge prodotto alla categoria DAILY
def prestashop_set_daily(product: Product):

    driver = __login()
    driver = __visit_products_list_page(driver)
    driver = __visit_product_page(driver, product)
    driver = __set_daily_category(driver)

    pass

# Crea crawler ed esegue login
def __login():

    driver = webdriver.Firefox(executable_path="/usr/bin/geckodriver")
    driver.get("caneva937.com/admin21/")

    email = driver.find_element_by_id("email")
    passw = driver.find_element_by_id("passwd")
    buttn = driver.find_element_by_id("submit_login")

    email.send_keys("ettore.caneva1@gmail.com")
    passw.send_keys("ettore2015")
    buttn.click()

    wait = WebDriverWait(driver, 5)
    return driver

# Va nella sezione prodotti
def __visit_products_list_page(driver):

    catalog = driver.find_element_by_id("subtab-AdminCatalog")
    catalog.find_element_by_tag_name("a")

    link = catalog.get_attribute('href')
    driver.get(link)
    
    wait = WebDriverWait(driver, 5)
    return driver

# Va nella pagina del prodotto
def __visit_product_page(driver, product: Product):

    filter = driver.find_element_by_name("filter_column_name")
    button = driver.find_element_by_name("products_filter_submit")

    filter.send_keys(product.name)
    button.click()

    wait = WebDriverWait(driver, 5)
    item = driver.find_element_by_link_text(product.name)
    
    link = item.get_attribute("href") 
    driver.get(link)

    wait = WebDriverWait(driver, 5)
    return driver

# Setta la categoria daily per il prodotto
def __set_daily_category(driver):

    category = driver.find_element_by_link_text("DAILY")
    category = category.find_element_by_xpath("..")
    category = category.find_element_by_tag_name("input")
    category.click()

    # Di gran lunga la ricerca più difficile
    save = driver.find_element_by_xpath("//button[@type = 'submit' and span[text() = 'Salva']]")
    save.click()

    wait = WebDriverWait(driver, 5)
    return driver

# =========================================================
# DEBUG

product = get_random_product("https://caneva937.com/facebookproductad5281274deb672fd9e51ef774aab73fd1.it.shop1.xml")
prestashop_set_daily(product)