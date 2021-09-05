import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintruSpider(scrapy.Spider):
    name = 'labirintru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D0%B8%D1%81%D1%82%D0%BE%D1%80%D0%B8%D1%8F/?price_min=&price_max=&age_min=&age_max=&form-pubhouse=&lit=&stype=0&available=1&preorder=1&paperbooks=1&ebooks=1']

    def parse(self, response: HtmlResponse):
        urls = response.xpath('//a[@class="product-title-link"]/@href').getall()
        next_page = response.xpath('//a[@class="pagination-next__text"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.book_parse)

    def book_parse(self, response: HtmlResponse):
        try:
            author_name, book_name = response.xpath("//h1/text()").get().split(sep=": ", maxsplit=1)
        except ValueError:
            author_name = None
            book_name = response.xpath("//h1/text()").get().split(sep=": ", maxsplit=1)
        try:
            std_price = int(response.xpath('//span[@class="buying-priceold-val-number"]/text()').get())
            sale_price = int(response.xpath('//span[@class="buying-pricenew-val-number"]/text()').get())
        except TypeError:
            sale_price = None
            std_price = int(response.xpath('//span[@class="buying-price-val-number"]/text()').get())
        rating = response.xpath('//div[@id="rate"]/text()').get()
        book_url = response.url
        item = BookparserItem(name=book_name, authors=author_name, url=book_url, std_price=std_price, sale_price=sale_price, rating=rating)
        yield item


