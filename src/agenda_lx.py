# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    agenda_lx.py                                       :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: simao <simao@student.42.fr>                +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/10/28 18:45:21 by simao             #+#    #+#              #
#    Updated: 2023/11/11 00:26:23 by simao            ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import os
import scrapy
import json
from utils import output_file, add_current_year
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(os.getcwd()), '.env')
load_dotenv(dotenv_path=dotenv_path)

class AgendaLXSpider(scrapy.Spider):
    name = "agendalx"
    start_urls = [
        "https://www.agendalx.pt/wp-json/agendalx/v1/events?categories=artes,musica,teatro,cinema,danca,literatura,feiras,stand-up-comedy&per_page=500&_fields=subject,title,subtitle,StartDate,LastDate,venue,link",
    ]
   
    def parse(self, response):
        print("Parse da agenda de Lisboa...")
        with open(output_file(), "w") as file:
            file.write("Categoria,Título,Subtítulo,Inicio,Fim,Local,Link\n")
        data = response.json()
        with open('test.json', "w") as file:
            file.write(json.dumps(response.json(), indent=4))
        for event in data:
            try:
                titulo = event.get('title', {}).get('rendered', None)
                subtitle = event.get('subtitle', [])[0] if event.get('subtitle') else None
                categoria  = event.get('subject', None)
                venue = event.get('venue', {})
                local = list(venue.values())[0].get('name', None) if venue and isinstance(venue, dict) else None
                link = event.get('link', None)
                StartDate = event.get('StartDate', None)
                LastDate = event.get('LastDate', None)
                # Remove commas if any are present
                categoria = categoria.replace(',', '-') if categoria else categoria
                titulo = titulo.replace(',', '-') if titulo else titulo
                subtitle = subtitle.replace(',', '-') if subtitle else subtitle
                local = local.replace(',', '-') if local else local
                
                with open(output_file(), "a") as file:
                    data_line = f"{categoria},{titulo},{subtitle},{StartDate},{LastDate},{local},{link}\n"
                    file.write(data_line)
            except Exception as e:
                print(f"Error writing data to file: {str(e)}")
