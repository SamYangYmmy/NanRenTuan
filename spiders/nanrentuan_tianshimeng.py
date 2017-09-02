#coding:utf-8

from scrapy import Request
from scrapy.spiders import Spider
from NanRenTuan.items import NanrentuanItem
import logging
import NanRenTuan.settings

class NanRenTuan_TianShiMeng(Spider):
    name='NanRenTuan_Spider'
    base_url='http://nanrenvip.net'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }

    def start_requests(self):
        url = 'http://nanrenvip.net/find.html'
        yield Request(url, headers=self.headers)

    def parse(self,response):
        actresses=response.xpath('//div[@class="tab-content"]/div/ul/li')
        for actress in actresses[0:200]:
            actress_url=self.base_url+'/'+actress.xpath('./a/@href').extract()[0]
            yield Request(url=actress_url, callback=self.parse_actress)

    def parse_actress(self, response):
        #logging.info(response.body)
        #item = NanrentuanItem()
        movies = response.xpath('//ul[@class="dfghj clear"]/li') #选取所有包含class='grid_view' 的ol 属性的值里面的li元素
        for movie in movies:
            #item['Fanhao']=movie.xpath('.//div[@class="list_text"]/span/date/a/b/text()').extract()[0]   # . 选取当前结点
            #item['name']=movie.xpath('.//div[@class="list_text"]/span/p/text()').extract()[0]
            #item['date']=movie.xpath('.//div[@class="list_text"]/span/date/text()').extract()[0]
            #yield item
            #test_date=movie.xpath('.//div[@class="list_text"]/span/date/text()').extract()[0]
            fanhao_url=self.base_url+movie.xpath('.//div[@class="list_text"]/span/date/a/@href').extract()[0]
            # 进入番号子页，爬取图片信息
            if fanhao_url:
                yield Request(url=fanhao_url,callback=self.parse_fanhao) #执行yield会将movie循环的结果保存并向外抛一个迭代对象request，这个对象会传递到下载器里面
        next_url = response.xpath('.//div[@class="dede_pages"]/ul/li[last()-1]/a/@href').extract() # 拿取最后一个li元素的前一个，为next，即对应的下一页
        if next_url:
            next_url = self.base_url + next_url[0]
            yield Request(url=next_url, callback=self.parse_actress)

    def parse_fanhao(self, response):
        item = NanrentuanItem()
        item['Fanhao']=response.xpath('//div[@class="article"]/h1/text()').extract()[0]
        #date=response.xpath('//div[@class="article"]/div[1]/p/span/text()')
        item['date']=response.xpath('//div[@class="article"]/div[1]/p/span/text()').extract()[0].split(u"：")[-1]
        item['actress_name']=response.xpath('//div[@class="article"]/div[1]/p/span[2]/a/text()').extract()[0]
        #name=response.xpath('//div[@class="con"]/p/img/@alt')
        if response.xpath('//div[@class="con"]/p/img/@alt'):
            item['name'] = response.xpath('//div[@class="con"]/p/img/@alt').extract()
            item['image_urls'] = response.xpath('//div[@class="con"]/p/img/@src').extract()
        else:
            item['name'] = response.xpath('//div[@class="con"]/img/@alt').extract()
            item['image_urls'] = response.xpath('//div[@class="con"]/img/@src').extract()
        yield item







