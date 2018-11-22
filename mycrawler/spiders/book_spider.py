import scrapy
from mycrawler.items import Article_DetailItem

class BooksSpider(scrapy.Spider):
    name = "books"
    start_urls = ["http://books.toscrape.com/",]


    def parse(self,response):
        item = Article_DetailItem()
        article_list = response.xpath('//article[@class="product_pod"]')
        for article in article_list:
            title = article.xpath('./h3/a/text()').extract_first()
            price  = article.xpath('./div[@class="product_price"]/p[@class="price_color"]/text()').extract_first()

            item['title'] = title
            item['price'] = price
            yield item
        next_url = response.xpath('//li[@class="next"]//a/@href')[0].extract()

        if next_url:
            if "catalogue" in next_url:
                url = str(self.start_urls[0])+str(next_url)
            else:
                url = str(self.start_urls[0])+"catalogue/"+str(next_url)
            print('Debug=========================================', url)
            yield scrapy.Request(url,callback=self.parse)
