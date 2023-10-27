import scrapy

class CascaisSpider(scrapy.Spider):
    name = "agenda_cascais"
    start_urls = [
        "https://360.cascais.pt/pt/agenda/musica",
        "https://360.cascais.pt/pt/agenda/teatro",
        "https://360.cascais.pt/pt/agenda/danca"

    ]

    def parse(self, response):
        categoria = response.css('.search-results-text::text').get()
        for event in response.css('.result-row.col-sm-4.image-sub-title'):
            yield {
                "Categoria": categoria,
                "Titulo": event.css('div.field-sub-title::text').get().strip(),
                "Data": event.css('::attr(data-filter-title)').get().strip(),
                "Local" : "Cascais",
                "Link": event.css('a.cover-link::attr(href)').get(),
            }

        next_page = response.css('li.next a::attr("href")').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
    