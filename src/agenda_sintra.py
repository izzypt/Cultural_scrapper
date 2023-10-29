# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    agenda_sintra.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: simao <simao@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/28 18:45:27 by simao             #+#    #+#              #
#    Updated: 2023/10/29 14:29:54 by simao            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import scrapy
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.getcwd()), '.env')
load_dotenv(dotenv_path=dotenv_path)

class SintraSpider(scrapy.Spider):
    name = "agenda_sintra"
    start_urls = [
        "https://ccolgacadaval.pt/agenda/musica",
        "https://ccolgacadaval.pt/agenda/teatro",
        "https://ccolgacadaval.pt/agenda/danca",
        "https://ccolgacadaval.pt/agenda/artes",
        "https://ccolgacadaval.pt/agenda/cinema",
    ]

    def parse(self, response):
        print("Parse da agenda de Sintra...")
        categoria = response.css('.sp-page-title-heading::text').get()
        for event in response.css('div.ic-list-event'):
            titulo = event.css('a.ic-text-decoration-none::attr(title)').get().replace(',', '|')
            data = event.css('span.ic-single-next::text').get()
            local = event.css('div.ic-place::text').get()
            link = event.css('a.ic-text-decoration-none::attr(href)').get()
            yield {
                "Categoria": categoria,
                "Titulo": titulo.strip() if titulo else None,
                "Data": data.strip() if data else None, 
                "Local": local.strip() if local else None,
                "Link": ("https://ccolgacadaval.pt" + link) if link else None,
            }
            with open(os.getenv('OUTPUT_FILE'), "a") as file:
                file.write(f"{categoria.strip() if categoria else 'N/A'},{titulo.strip() if titulo else 'N/A'},N/A,N/A,{data.strip() if data else 'N/A'},{local.strip() if local else 'N/A'},{('https://ccolgacadaval.pt' + link) if link else 'N/A'}\n")
        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

