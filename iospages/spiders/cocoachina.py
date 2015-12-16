# -*- coding:utf-8 -*-
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.selector import Selector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from iospages.items import IospagesItem
import codecs
import html2text
class CocoaChina(CrawlSpider):
    name = "cocoachina"
    start_urls = [
        "http://www.cocoachina.com"
    ]
    rules = (
        Rule(SgmlLinkExtractor(allow = (r'http://www.cocoachina.com/ios/\d{8}/\d+.html',)),callback="parse_page",follow=True),
        )

    def parse_page(self, response):

        sel = Selector(response)
        item = IospagesItem()
        details = sel.xpath("//div[@id='detailbody']")
        content = ""
        if details.count >  0:
            content = html2text.html2text(details[0].extract())
            pass
        titles = sel.xpath('//title/text()').extract()
        title = ""

        if titles.count ==0 :
            return item
        else:
            title = titles[0].encode('utf-8')

        item['title'] = title
        if content != "":
            filename =  title + ".html"
            with codecs.open(filename,"w","utf-8-sig") as f:
                f.write(content)
                f.close()

        return item
