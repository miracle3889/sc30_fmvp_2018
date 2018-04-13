import scrapy


class QuotesSpider(scrapy.Spider):
    """
    豆瓣电影top250
    """
    name = "film250"

    start_urls = [
        'https://movie.douban.com/top250',
    ]

    def parse(self, response):
        for a in response.css("div.item"):
            def extract_with_css(query):
                return a.css(query).extract_first().strip()

            yield {
                'index': extract_with_css('div.pic em::text'),
                'title': extract_with_css('div.hd span.title::text'),
                'rate': extract_with_css('div.star .rating_num::text'),
            }

        for href in response.css("span.next a"):
            yield response.follow(href, callback=self.parse)

