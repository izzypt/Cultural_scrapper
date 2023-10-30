# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    agenda_cascais.py                                  :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: simao <simao@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/28 18:45:40 by simao             #+#    #+#              #
#    Updated: 2023/10/29 23:12:20 by simao            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import scrapy
from utils import output_file
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.getcwd()), '.env')
load_dotenv(dotenv_path=dotenv_path)

class CascaisSpider(scrapy.Spider):
    name = "agenda_cascais"
    start_urls = [
        "https://360.cascais.pt/pt/agenda/musica",
        "https://360.cascais.pt/pt/agenda/teatro",
        "https://360.cascais.pt/pt/agenda/danca"

    ]

    def parse(self, response):
        print("Parse da agenda de Cascais...")
        categoria = response.css('.search-results-text::text').get()
        for event in response.css('.result-row.col-sm-4.image-sub-title'):
            titulo = event.css('::attr(data-filter-title)').get().replace(',','')
            data = str(event.css('div.field-sub-title::text').get()).replace("'"," ")
            data_inicial = data.split('-')[0] if len(data.split(' - ')) == 2 else 'N/A'
            data_final = data.split('-')[1] if len(data.split(' - ')) == 2 else data
            local = "Cascais"
            link = event.css('a.cover-link::attr(href)').get()
            yield {
                "Categoria": categoria.strip() if categoria else 'N/A',
                "Titulo": titulo.strip() if titulo else 'N/A',
                "Data": data.strip() if data else 'N/A',
                "Local" : local,
                "Link": link.strip() if link else 'N/A',
            }
            with open(output_file(), "a") as file:
                file.write(f"{categoria.strip() if categoria else 'N/A'},{titulo.strip() if titulo else 'N/A'},N/A,{data_inicial},{data_final.strip() if data else 'N/A'},{local},{link}\n")
        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
    