import scrapy


class QuotesSpider(scrapy.Spider):
    name = "quotes"

    start_urls = [
        'http://quotes.toscrape.com',
    ]

    def parse(self, response):
        for quote in response.css("div.quote"):
            yield {
                'text': quote.css("span.text::text").extract_first().strip(),
                'author': quote.css("small.author::text").extract_first().strip(),
                'tags': quote.css("div.tags a.tag::text").extract(),
            }
        for a in response.css("li.next a"):
            yield response.follow(a, callback=self.parse)
