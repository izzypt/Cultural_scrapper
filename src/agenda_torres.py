# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    agenda_torres.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: simao <simao@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/28 18:45:21 by simao             #+#    #+#              #
#    Updated: 2023/10/28 23:53:25 by simao            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import scrapy

FILE_PATH = "agenda_cultural.csv"

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
            titulo = evento.css('span.coluna-titulo::text').get()
            local = "Torres Vedras",
            data = evento.css('span.data::text').get()
            link = "https://teatrocine-tvedras.pt" + evento.css('div a::attr(href)').get()
            yield {
                "Categoria": categoria.strip() if categoria else None,
                "Titulo": titulo.strip() if titulo else None,
                "Data": data.strip() if data else None,
                "Local": local,
                "Link": link,
            }
            with open(FILE_PATH, "a") as file:
                file.write(f"{categoria.strip() if categoria else 'N/A'},{titulo.strip() if titulo else 'N/A'},N/A,{data.strip() if data else 'N/A'},N/A,{local},{link}\n")

        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)