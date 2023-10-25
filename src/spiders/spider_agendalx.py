import scrapy

class AgendaLxSpider(scrapy.Spider):
    name = "AgendaLX"
    start_urls = [
        "https://www.agendalx.pt/?archive=agenda&categories=artes&categories=musica&categories=teatro&categories=cinema&categories=danca&categories=stand-up-comedy&s=&type=event",
    ]

    def parse(self, response):
        for event in response.css('li.accordion-list__item'):
            yield {
                "Titulo": event.css('a.accordion-list__full-link::attr(title)').get(),
                "Subtitulo": event.css('h3.title.title--whisper.accordion-list__subtitle::text').get(),
                "Link": event.css('a.accordion-list__full-link::attr(href)').get(),
                "Categoria": event.css('div.signpost__subject span.subject::text').get(),
                "Data": event.css('div.signpost__date::text').get(),
                "Local": event.css('div.signpost__venue::text').get(),
            }