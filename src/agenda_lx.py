# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    agenda_lx.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: simao <simao@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/28 18:45:34 by simao             #+#    #+#              #
#    Updated: 2023/10/29 23:53:48 by simao            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import time
from utils import mes_EN_to_PT, add_current_year, output_file
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import selenium.common.exceptions as selenium_exceptions
from dotenv import load_dotenv

####################
# LOAD ENVIRONMENT #
####################
dotenv_path = os.path.join(os.path.dirname(os.getcwd()), '.env')
load_dotenv(dotenv_path=dotenv_path)

###########################
# OPEN CSV/ WRITE HEADERS #
###########################
with open(output_file(), "w") as file:
    file.write("Categoria,Título,Subtítulo,Inicio,Fim,Local,Link\n")

##################
# SETUP SELENIUM #
##################
options = webdriver.FirefoxOptions()
options.add_argument('--headless')
driver = webdriver.Firefox(options=options)
driver.get("https://www.agendalx.pt/?archive=agenda&categories=artes&categories=musica&categories=teatro&categories=cinema&categories=danca&categories=stand-up-comedy&s=&type=event")
title = driver.title

##################
# LOOP ALL PAGES #
##################
print("Starting scrape da agenda lx...")
while True:
    try:
        next_button = WebDriverWait(driver, 25, 2).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/main/div/div[2]/div/div[4]/button"))
        )
        next_button.click()
        print("Scrapper loading more data...")
        time.sleep(1)
    except:
        print("No more 'Next' button available or it's not clickable.\n Finished scraping.")
        break


#########################
# EXTRACT/WRITE TO FILE #
#########################
elements = driver.find_elements(By.CLASS_NAME, 'accordion-list__item')
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
        date_split = date.split(' a ')
        start_date = date_split[0] if len(date_split) >= 2 else 'N/A'
        end_date = date_split[1] if len(date_split) >= 2 else date
        if (len(start_date.split(' ')) < 2):
            start_date = 'N/A'
        start_date = add_current_year(mes_EN_to_PT(start_date))
        end_date = mes_EN_to_PT(end_date)
    except Exception as e:
        print(e)
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
    with open(output_file(), "a") as file:
        file.write(f"{categoria},{title},{subtitulo},{start_date},{end_date},{local},{link}\n")
driver.quit()