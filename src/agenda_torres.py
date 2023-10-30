# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    agenda_torres.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: simao <simao@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/28 18:45:21 by simao             #+#    #+#              #
#    Updated: 2023/10/29 23:59:33 by simao            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import scrapy
from utils import output_file, add_current_year
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.getcwd()), '.env')
load_dotenv(dotenv_path=dotenv_path)

class SintraSpider(scrapy.Spider):
    name = "agenda_torres"
    start_urls = [
        "https://teatrocine-tvedras.pt/agenda/categoria/37",
        "https://teatrocine-tvedras.pt/agenda/categoria/33",
        "https://teatrocine-tvedras.pt/agenda/categoria/35"
    ]

    def parse(self, response):
        print("Parse da agenda de Torres...")
        eventos = response.css('div.listagem-eventos')
        for evento in eventos:
            categoria = evento.css('div.categoria-evento::text').get()
            titulo = evento.css('span.coluna-titulo::text').get().replace(',', '|')
            data = evento.css('span.data::text').get()
            link = "https://teatrocine-tvedras.pt" + evento.css('div a::attr(href)').get()
            yield {
                "Categoria": categoria.strip() if categoria else None,
                "Titulo": titulo.strip() if titulo else None,
                "Data": data.strip() if data else None,
                "Link": link,
            }
            with open(output_file(), "a") as file:
                file.write(f"{categoria.strip() if categoria else 'N/A'},{titulo.strip() if titulo else 'N/A'},N/A,N/A,{add_current_year(data.strip()) if data else 'N/A'},Torres Vedras,{link}\n")

        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)