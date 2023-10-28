# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    agenda_sintra.py                                   :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: simao <simao@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/28 18:45:27 by simao             #+#    #+#              #
#    Updated: 2023/10/28 18:45:28 by simao            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import scrapy

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
        categoria = response.css('.sp-page-title-heading::text').get()
        for event in response.css('div.ic-list-event'):
            data_text = event.css('span.ic-single-next::text').get()
            local_text = event.css('div.ic-place::text').get()
            yield {
                "Categoria": categoria,
                "Titulo": event.css('a.ic-text-decoration-none::attr(title)').get(),
                "Data": data_text.strip() if data_text else None, 
                "Local": local_text.strip() if local_text else None,
                "Link": "ccolgacadaval.pt" + event.css('a.ic-text-decoration-none::attr(href)').get(),
            }

        next_page = response.css('a[rel="next"]::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)

