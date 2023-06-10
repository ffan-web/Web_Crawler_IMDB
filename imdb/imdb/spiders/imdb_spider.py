import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from imdb.items import ImdbItem
import csv

class ImdbSpider(CrawlSpider):
    name = "imdb"
    allowed_domains = ["imdb.com"]
    rules = (
        Rule(LinkExtractor(restrict_xpaths=("//*[@id='main']/div/div[4]/a")),
            process_links=lambda links: filter(lambda l: 'Next' in l.text, links),
            callback='parse',
            follow=True),
    )

    def start_requests(self):
        start_url = "http://www.imdb.com/search/title?year=2014,2014&title_type=feature&sort=moviemeter,asc"
        yield scrapy.Request(start_url)

    def parse(self, response):
        for i in range(1, 51):
            item = ImdbItem()
            try:
                sxpath = "//*[@id='main']/div/div[3]/div/div[" + str(i) + "]/div[3]/h3/a/text()"
                #print(" [Xpath] ------------- " + sxpath)
                item['Title'] = response.xpath(sxpath).extract()[0]
                print(" [Movie Title] ------------- " + item['Title'])
                dxpath = "//*[@id='main']/div/div[3]/div/div[" + str(i) + "]/div[3]/p[3]/a[1]/text()"
                item['Director'] = response.xpath(dxpath).extract()[0]
                #print(" [ Director  ] ------------- " + item['Director'])
                rxpath = "//*[@id='main']/div/div[3]/div/div[" + str(i) + "]/div[3]/div/div[1]/strong/text()"
                item['Rating'] = response.xpath(rxpath).extract()[0]
                #print(" [ Rating ] -----------------" + item['Rating'])
                gxpath = "//*[@id='main']/div/div[3]/div/div[" + str(i) + "]/div[3]/p[1]/span[5]/text()"
                item['Genre'] = response.xpath(gxpath).extract()[0].strip()
                #print(" [ Genre ] -----------------" + item['Genre'])
                cxpath = "//*[@id='main']/div/div[3]/div/div[" + str(i) + "]/div[3]/p[1]/span[1]/text()"
                item['Certificate'] = response.xpath(cxpath).extract()[0]
                #print(" [ Certificate ] -----------------" + item['Certificate'])
                yxpath = "//*[@id='main']/div/div[3]/div/div[" + str(i) + "]/div[3]/h3/span[2]/text()"
                ystr = response.xpath(yxpath).extract()[0]
                lenystr = len(ystr)
                item['Year'] = response.xpath(yxpath).extract()[0][lenystr-5:lenystr-1]
                #print(" [ year ] -----------------" + item['Year'])

                with open("../results.csv", "a", newline='') as outfile:
                    writer = csv.writer(outfile)
                    writer.writerow([item['Title'], item['Year'], item['Director'], item['Genre'], item['Certificate'], item['Rating']])

            except:
                print("Error -----------------------------------")

