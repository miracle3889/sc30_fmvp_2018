import scrapy


class QuotesSpider(scrapy.Spider):
    name = "author"

    start_urls = [
        'http://quotes.toscrape.com',
    ]

    def parse(self, response):
        for a in response.css(".author + a"):
            yield response.follow(a, callback=self.parse_author)
        for href in response.css("li.next a"):
            yield response.follow(href, callback=self.parse)

    def parse_author(self, response):
        def extract_with_css(query):
            return response.css(query).extract_first().strip()

        yield {
            'name': extract_with_css('h3.author-title::text'),
            'birthdate': extract_with_css('.author-born-date::text'),
            'bio': extract_with_css('.author-description::text'),
        }

