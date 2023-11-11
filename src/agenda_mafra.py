# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    agenda_mafra.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: simao <simao@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/28 18:45:21 by simao             #+#    #+#              #
#    Updated: 2023/11/11 01:10:40 by simao            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import scrapy
from utils import output_file, add_current_year
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.getcwd()), '.env')
load_dotenv(dotenv_path=dotenv_path)

class MafraSpider(scrapy.Spider):
    name = "agenda_Mafra"
    start_urls = [
        "https://www.cm-mafra.pt/pages/1134",
    ]

    def parse(self, response):
        events = response.css('ul.grid-x.grid-margin-x.grid-margin-y.xsmall-up-1.small-up-2.medium-up-2.large-up-3 li')

        for event in events:
            print("Parse da agenda de Mafra...")
            event_id = event.css('a::attr(href)').extract_first()
            dates = event.css('div.dates.widget_field div.widget_value span::text').extract()
            dates_split = ' '.join(dates).split(' a ')
            initialDate = dates_split[0] if dates_split[0] else 'N/A'
            finalDate = dates_split[1] if len(dates_split) > 1 else 'N/A'
            title = event.css('div.title.widget_field h2::text').extract_first().replace(',', '-')
            categoria = event.css('div.categories.widget_field div.widget_value span::text').extract()
            link = event.css('a::attr(href)').extract_first() or 'N/A'

            categoria = categoria[0] if categoria[-1] not in ['Música', 'Teatro & Espetáculos'] else categoria[-1]
            with open(output_file(), "a") as file:
                file.write(f"{categoria if categoria else 'N/A'},{title if title else 'N/A'},N/A,{add_current_year(initialDate)},{add_current_year(finalDate)},Mafra,{'https://www.cm-mafra.pt' + link if link else 'N/A'}\n")
        # Pagination
        next_page = response.css('div.pagination a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)