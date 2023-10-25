from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exceptions
from selenium.webdriver.firefox.options import Options
import time

FILE_PATH = "agenda_lx.csv"
with open(FILE_PATH, "w") as file:
    file.write("Categoria,Título,Subtítulo,Inicio,Fim,Local,Link\n")

options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
driver.get("https://www.agendalx.pt/?archive=agenda&categories=artes&categories=musica&categories=teatro&categories=cinema&categories=danca&categories=stand-up-comedy&s=&type=event")
title = driver.title

while True:
    try:
        next_button = WebDriverWait(driver, 25, 2).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/div/div[2]/div/div[4]/button"))
        )
        next_button.click()
        print("Clicked on the next button. Loading more data...")
        time.sleep(2)
    except:
        print("No more 'Next' button available or it's not clickable.\n Finished scraping.")
        break

elements = driver.find_elements(By.CLASS_NAME, 'accordion-list__item')

# Extract the information
for element in elements:
    try:
        title = element.find_element(By.CLASS_NAME, 'accordion-list__full-link').get_attribute('title').replace(',', ' - ')
    except:
        title = "N/A"
    try:
        subtitulo = element.find_element(By.CLASS_NAME, 'title.title--whisper.accordion-list__subtitle').text.replace(',', ' - ')
    except:
        subtitulo = "N/A"
    try:
        categoria = element.find_element(By.CLASS_NAME, 'subject').text.replace(',', ' - ')
    except:
        categoria = "N/A"
    try:
        date = element.find_element(By.CLASS_NAME, 'signpost__date').text.replace(',', ' - ')
        start_date = date.split(' a ')[0] if len(date.split(' a ')) == 2 else date
        end_date = date.split(' a ')[1] if len(date.split(' a ')) == 2 else date
    except:
        start_date = "N/A"
        end_date = "NA"
    try:
        local = element.find_element(By.CLASS_NAME, 'signpost__venue').text.replace(',', ' - ')
    except:
        local = "N/A"
    try:
        link = element.find_element(By.CLASS_NAME, 'accordion-list__full-link').get_attribute('href')
    except:
        link = "N/A"
    print("A escrever para o CSV...")
    with open(FILE_PATH, "a") as file:
        file.write(f"{categoria},{title},{subtitulo},{start_date},{end_date},{local},{link}\n")

driver.quit()