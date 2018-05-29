# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request

class DiscoverySpider(scrapy.Spider):
    name = 'discovery'
    allowed_domains = ['xinpianchang.com']
    start_urls = ['http://www.xinpianchang.com/channel/index/sort-like']

    def parse(self, response):
        # 作品路径
        post_url = 'http://www.xinpianchang.com/a%s?from=ArticleList'
        # 主页中所有作品的信息级
        post_list = response.xpath('//ul[@class="video-list"]/li')
        for i in range(5):
            for post in post_list:
                # 获取每个作品的id信息
                pid = post.xpath('./@data-articleid').get()
                # print(post_url % post)
                # 发起每个详情页信息 请求
                request = Request(post_url % pid, callback=self.parse_post)
                # 将作品id 传入
                request.meta['pid'] = pid
                # Xpath
                # request.meta['thumbnail'] = post.xpath('./a/img/@_src').get()
                # css
                # 缩略图传递
                request.meta['thumbnail'] = post.css('a img::attr(src)').get()
                # 持续时长
                request.meta['duration'] = post.xpath('.//span[contains(@class, "duration")]/text()').get()
                yield request

    def parse_post(self, response):
        # print(response.text)
        post = {}
        # 作品id
        pid = response.meta["pid"]
        post['pid'] = pid
        # 缩略图
        post['thumbnail'] = response.meta['thumbnail']
        # 时长
        post['duration'] = response.meta["duration"]
        # 视频链接
        post['video'] = response.xpath("//video[@id='xpc_video']/@src").get()
        # Xpath
        # 未播放的图片
        post['preview'] = response.xpath('//div[@class="filmplay"]//img/@src').extract_first()
        # Xpath
        # post['title'] = response.xpath('//div[@class="title-wrap"]/h3/text()').get()
        # css
        # 作品标题
        post['title'] = response.css('div[class*=title-wrap] h3::text').get()
        # Xpath
        # 分类
        # cates = response.xpath('//span[contains(@class, "cate")]/a/text()').extract()
        # css
        # 分类
        cates = response.css('span[class*=cate] a::text').extract()
        # print(cates)
        post['category'] = "-".join([cate.strip() for cate in cates])
        # 创建时间
        post['create_at'] = response.xpath('//span[contains(@class, "update-time")]/i/text()').get()
        # 点击次数
        post['play_counts'] = response.xpath('//i[contains(@class, "play-counts")]/@data-curplaycounts').get()
        # 喜欢次数
        post['like_counts'] = response.xpath('//span[contains(@class, "like-counts")]/@data-counts').get()
        # 详情
        post['description'] = response.xpath('//p[contains(@class, "desc")]/text()').get()
        yield post
        # 作品的创作人列表
        creator_list = response.xpath('//ul[contains(@class, "creator-list")]/li')

        user_url = 'http://www.xinpianchang.com/u%s?from=articleList'
        for creator in creator_list:
            u_id = creator.xpath('.//a/@data-userid').get()
            # u_url = creator.xpath('.//a/@href').get()
            # print(u_url)
            # 获取作者详细信息
            request = Request(user_url % u_id, callback=self.auth_parse)
            request.meta['u_id'] = u_id
            yield request
            cr = {}
            # 创建关联xinxi
            # 用户id
            cr['cid'] = u_id
            # 作品id
            cr['pid'] = pid
            # 当前用户在当前作品中的工作
            cr['roles'] = creator.xpath('.//span[contains(@class, "roles")]/text()').get()
            yield cr
        comment_url = 'http://www.xinpianchang.com/article/filmplay/ts-get'
        request = Request(comment_url % pid, callback=self.parse_comment)
        request.meta['pid'] = pid
        yield request

    def parse_comment(self, response):

        result = json.loads(response.text)
        comments = result['data']['list']
        for c in comments:
            comment = {}
            comment["commentid"] = c['commentid']
            comment['pid'] = response.meta['pid']
            comment['cid'] = c['userInfo']['userid']
            comment['uname'] = c['userInfo']['username']
            comment['avatar'] = c['userInfo']['face']
            comment['created_at'] = c['addtime']
            comment['content'] = c['content']
            comment['like_counts'] = c['count_approve']
            if c['replay']:
                comment['replay'] = c['replay']['commentid']
            yield comment

            # 判断有没有下一页，
            next_page = result['data']['next_page_url']
            if next_page:
                # 递归抓取所有评论
                request = Request(next_page, callback=self.parse_comment)
                # 将作品id传入
                request.meta['pid'] = request.meta['pid']
                yield request

    def auth_parse(self, response):
        composer = {}
        # 用户id
        composer['cid'] = response.meta['u_id']
        # 头部背景
        composer['banner'] = response.xpath('//div[@class="banner-wrap"]/@style').get()[21:-1]
        # 头像
        composer['avater'] = response.xpath('//span[@class="avator-wrap-s"]/img/@src').get()
        # 用户名
        composer['name'] = response.xpath('//p[contains(@class, "creator-name")]/text()').get()
        # 介绍
        composer['intro'] = response.xpath('//p[contains(@class, "creator-desc")]/text()').get()
        # 喜欢人数
        composer['lick_counts'] = response.xpath('//span[contains(@class, "like-counts")]/text()').get()
        # 粉丝
        composer['fans_counts'] = response.xpath('//span[contains(@class, "fans-counts")]/text()').get()
        # 关注人数
        composer['follow_counts'] = response.xpath('//span[contains(@class, "follow-wrap")]/span[2]/text()').get()
        # 地址
        composer['location'] = response.xpath('//p[contains(@class, "creator-detail")]/span[5]/text()').get()
        # 职业名称
        composer['career'] = response.xpath('//p[contains(@class, "creator-detail")]/span[7]/text()').get()

        yield composer

def strip(s):
    if s:
        return s.strip()


def clean(string):
    if string:
        return string.replace(",", '')
    else:
        return ''