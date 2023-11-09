# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    agenda-mafra.py                                    :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: simao <simao@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/28 18:45:21 by simao             #+#    #+#              #
#    Updated: 2023/11/09 20:40:02 by simao            ###   ########.fr        #
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
        "https://www.cm-mafra.pt/pages/1134",
    ]

    def parse(self, response):
        events = response.css('ul.grid-x.grid-margin-x.grid-margin-y.xsmall-up-1.small-up-2.medium-up-2.large-up-3 li')

        for event in events:
            event_id = event.css('a::attr(href)').extract_first()
            dates = event.css('div.dates.widget_field div.widget_value span::text').extract()
            title = event.css('div.title.widget_field h2::text').extract_first()
            summary = event.css('div.summary.widget_field div.widget_value div::text').extract_first()
            categoria = event.css('div.categories.widget_field div.widget_value span::text').extract()
            link = "teste"

            with open(output_file(), "a") as file:
                file.write(f"{categoria if categoria else 'N/A'},{title if title else 'N/A'},N/A,N/A,{dates if dates else 'N/A'},Mafra,{link}\n")
        # Pagination
        next_page = response.css('div.pagination a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse)