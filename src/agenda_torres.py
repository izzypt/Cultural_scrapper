# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    agenda_torres.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: simao <simao@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/28 18:45:21 by simao             #+#    #+#              #
#    Updated: 2023/10/28 19:36:17 by simao            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import scrapy

class SintraSpider(scrapy.Spider):
    name = "agenda_torres"
    start_urls = [
        "https://teatrocine-tvedras.pt/agenda/categoria/37",
        "https://teatrocine-tvedras.pt/agenda/categoria/33",
        "https://teatrocine-tvedras.pt/agenda/categoria/35"
    ]

    def parse(self, response):
        eventos = response.css('div.listagem-eventos')
        for evento in eventos:
            categoria = evento.css('div.categoria-evento::text').get()
            titulo = evento.css('span.coluna-titulo::text').get()
            data = evento.css('span.data::text').get()
            yield {
                "Categoria": categoria.strip() if categoria else None,
                "Titulo": titulo.strip() if titulo else None,
                "Data": data.strip() if data else None,
                "Local": "Torres Vedras",
                "Link": "https://teatrocine-tvedras.pt" + evento.css('div a::attr(href)').get(),
            }

        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)