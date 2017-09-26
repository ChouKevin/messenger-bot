import scrapy
import logging
from ipeenCrawl.items import *

class restaurantSpider(scrapy.Spider):
    """docstring for ClassName"""
    name = 'restaurant'

    def start_requests(self):
        urls = [
            'http://www.ipeen.com.tw/search/taiwan/000/1-0-0-0/?p=1',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        def getCate(query):
            return [href.css(query).xpath('.//a[1]/text()').extract_first(),
                    href.css(query).xpath('.//a[2]/text()').extract_first()]
        item_href = response.css('section.lbsResult article.serItem div.serShop')
        for href in item_href:
            yield response.follow(href.css('a.a37::attr(href)').extract_first(), self.parseRestaurant,
                                  meta={'name':href.css('a.a37::text').extract_first(),
                                        'cate':getCate('li.cate')})
        next_page = response.css('div.allschool_pagearea label.next_p_one a.ga_tracking::attr(href)')
        # for href in next_page:
        #     yield response.follow(href, self.parse)

    def parseRestaurant(self, response):
        hours = response.css('div.hours span ::text').extract()
        score = self.calcu_score(response.css('dl.rating meter::attr(value)').extract(),
                                 response.css('dl.rating meter::attr(max)').extract())
        yield response.follow(response.url, self.parse_comment_section, dont_filter=True)
        # if not hours:
        #     hours = response.css('div.hours p ::text').extract()
        # r_item = RestaurantItem()
        # r_item['rid'] = response.url
        # r_item['name'] = response.meta['name']
        # r_item['classify'] = response.meta['cate']
        # r_item['tel'] = response.css('div.brief p.tel a::text').extract_first()
        # r_item['avgCost'] = response.css('div.brief p.cost::text').extract_first()
        # r_item['hours'] = hours
        # r_item['environmentRate'] = score[2]
        # r_item['serviceRate'] = score[1]
        # r_item['tasteRate'] = score[0]
        # r_item['address'] = response.css('a.whole-map::attr(href)').extract_first()
        # yield r_item
        # self.parse_comment_section(response)

    def parse_comment_section(self, response):
        comments_section = response.css('div.row > div > section.review-list')
        comments_href = comments_section.css('div.text p.summary a::attr(href)').extract()
        comments_page = comments_section.css('div.page-block a::attr(href)').extract()
        page_button = comments_section.css('div.page-block span::text').extract()
        for href in comments_href:
            yield response.follow(href, self.parse_comment)
        if page_button and page_button[-1] == u'\u4e0b\u4e00\u9801':
            logging.info('Finished Page : {0}'.format(comments_page[-1]))
            return
        if comments_page:
            yield response.follow(comments_page[-1], self.parse_comment_section)

    def parse_comment(self, response):
        user_comment = UserComment()
        selector = 'div.brief div.scalar p span.score-bar '
        score = self.calcu_score(response.css(selector + 'meter::attr(value)').extract(),
                                 response.css(selector + 'meter::attr(max)').extract(),
                                 _range=1)
        line = response.css('section > div > div.description p *::text').extract()
        if not line:
            line = response.css('section > div > div.description span *::text').extract()
        comment = ''
        for string in line:
            comment += string
        user_comment['rid'] = response.css('header div div.info div.brief p:nth-child(1) a::attr(href)').extract_first()
        user_comment['rate'] = score[0]
        user_comment['uid'] = response.css('div > figure > figcaption > h3 > a::attr(href)').extract_first()
        user_comment['context'] = comment
        yield user_comment

    def calcu_score(self, score_list, max_score_list, _range=3):
        score = []
        for i in range(_range):
            try:
                score.append(float(score_list[i])/float(max_score_list[i]))
            except IndexError:
                score.append(0)
        return score
