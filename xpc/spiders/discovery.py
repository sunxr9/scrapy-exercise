# -*- coding: utf-8 -*-
import json

import scrapy
from scrapy import Request
from ..items import PostItem, CommentItem, ComposerItem, CopyrightItem
from scrapy_redis.spiders import RedisSpider

class DiscoverySpider(RedisSpider):
    name = 'discovery'
    allowed_domains = ['xinpianchang.com']
    # start_urls = ['http://www.xinpianchang.com/channel/index/sort-like']

    # scrapy默认使用服务器返回的cookies，会修改settings中配置的kooies，
    # scrapy根据response中的dont_merge_cookies属性判断是否使用配置文件中设置的headers信息
    # 重写start——requests方法，在第一次请求的时候就会携带dont_merge_cookies属性
    # def start_requests(self):
    #     for url in self.start_urls:
    #         request = Request(url, dont_filter=True)
    #         request.meta['dont_merge_cookies'] = True
    #         yield request

    # 继承redisSpider 出现cookies还是被修改之后重写次方法
    def make_requests_from_url(self, url):
        request = Request(url, dont_filter=True)
        request.meta["dont_merge_cookies"] = True
        return request

    def parse(self, response):
        # 作品路径
        post_url = 'http://www.xinpianchang.com/a%s?from=ArticleList'
        # 主页中所有作品的信息级
        post_list = response.xpath('//ul[@class="video-list"]/li')
        for post in post_list:
            # 获取每个作品的id信息
            pid = post.xpath('./@data-articleid').get()
            # print(post_url % post)
            # 发起每个详情页信息 请求
            request = Request(post_url % pid, callback=self.parse_post)
            # 将作品id 传入
            request.meta['pid'] = pid
            # Xpath
            request.meta['thumbnail'] = post.xpath('./a/img/@_src').get()
            # css
            # 缩略图传递
            # request.meta['thumbnail'] = post.css('a img::attr(src)').get()
            # 持续时长
            request.meta['duration'] = post.xpath('.//span[contains(@class, "duration")]/text()').get()
            request.meta['dont_merge_cookies'] = True
            yield request
        # 作品列表页的下一页
        next_page = response.xpath("//a[@title='下一页']/@href").get()
        if next_page:
            # 请求
            request = Request(next_page, callback=self.parse)
            # 携带这个属性，scrapy就不会删除sttings中配置的请求header信息
            request.meta["dont_merge_cookies"] = True
            yield request

    def parse_post(self, response):
        # print(response.text)
        post = PostItem()
        # 作品id
        pid = response.meta["pid"]
        post['pid'] = pid
        # 缩略图
        post['thumbnail'] = response.meta['thumbnail']
        # 时长
        minutes, seconds, *_ = response.meta["duration"].split("'")
        post['duration'] = int(minutes) * 60 + int(seconds)
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
        post['category'] = "-".join([strip(cate) for cate in cates])
        # 创建时间
        post['created_at'] = response.xpath('//span[contains(@class, "update-time")]/i/text()').get()
        # 点击次数
        post['play_counts'] = response.xpath('//i[contains(@class, "play-counts")]/@data-curplaycounts').get()
        # 喜欢次数
        post['like_counts'] = response.xpath('//span[contains(@class, "like-counts")]/@data-counts').get()
        # 详情
        post['description'] = strip(response.xpath('//p[contains(@class, "desc")]/text()').get())
        yield post

        # 作品的创作人列表
        creator_list = response.xpath('//div[contains(@class, "filmplay-creator")]/ul/li')
        # 作品人路径
        user_url = 'http://www.xinpianchang.com/u%s?from=articleList'
        for creator in creator_list:
            u_id = creator.xpath('.//a/@data-userid').get()
            # u_url = creator.xpath('.//a/@href').get()
            # print(u_url)
            # 获取作者详细信息
            request = Request(user_url % u_id, callback=self.auth_parse)
            request.meta['u_id'] = u_id
            yield request
            cr = CopyrightItem()
            cr['pcid'] = '%s_%s' %(u_id, pid)
            # 创建关联xinxi
            # 用户id
            cr['cid'] = u_id
            # 作品id
            cr['pid'] = pid
            # 当前用户在当前作品中的工作
            cr['roles'] = creator.xpath('.//span[contains(@class, "roles")]/text()').get()
            yield cr
        comment_url = 'http://www.xinpianchang.com/article/filmplay/ts-getCommentApi?id=%s&ajax=0&page=1'
        request = Request(comment_url % pid, callback=self.parse_comment)
        request.meta['pid'] = pid
        yield request

    def parse_comment(self, response):

        result = json.loads(response.text)
        comments = result['data']['list']
        for c in comments:
            comment = CommentItem()
            # 评论id
            comment["commentid"] = c['commentid']
            # 作品id
            comment['pid'] = response.meta['pid']
            # 用户id
            comment['cid'] = c['userInfo']['userid']
            # 评论用户名
            comment['uname'] = c['userInfo']['username']
            # 评论头像
            comment['avatar'] = c['userInfo']['face']
            # 时间
            comment['created_at'] = c['addtime']
            #
            comment['content'] = c['content']
            # 喜欢次数
            comment['like_counts'] = c['count_approve']
            if c['reply']:
                comment['reply'] = c['reply']['commentid']
            yield comment

            # 判断有没有下一页，
            next_page = result['data']['next_page_url']
            if next_page:
                # 递归抓取所有评论
                request = Request(next_page, callback=self.parse_comment)
                # 将作品id传入
                request.meta['pid'] = response.meta['pid']
                yield request

    def auth_parse(self, response):
        composer = ComposerItem()
        # 用户id
        composer['cid'] = response.meta['u_id']
        # 头部背景
        composer['banner'] = response.xpath('//div[@class="banner-wrap"]/@style').get()[21:-1]
        # 头像
        composer['avatar'] = response.xpath('//span[@class="avator-wrap-s"]/img/@src').get()
        # 用户名
        composer['name'] = response.xpath('//p[contains(@class, "creator-name")]/text()').get()
        # 介绍
        composer['intro'] = response.xpath('//p[contains(@class, "creator-desc")]/text()').get()
        # 喜欢人数
        composer['like_counts'] = clean(response.xpath('//span[contains(@class, "like-counts")]/text()').get())
        # 粉丝
        composer['fans_counts'] = clean(response.xpath('//span[contains(@class, "fans-counts")]/text()').get())
        # 关注人数
        # composer['follow_counts'] = response.xpath('//span[contains(@class, "follow-wrap")]/span[2]/text()').get()
        composer['follow_counts'] = clean(response.xpath('//span[@class="follow-wrap"]/span[2]/text()').get())
        # 地址
        # composer['location'] = response.xpath('//p[contains(@class, "creator-detail")]/span[5]/text()').get()
        composer['location'] = response.xpath('//span[contains(@class, "icon-location")]/following-sibling::span[1]/text()').get()
        # 职业名称
        # composer['career'] = response.xpath('//p[contains(@class, "creator-detail")]/span[7]/text()').get()
        composer['career'] = response.xpath('//span[contains(@class, "icon-career")]/following-sibling::span[1]/text()').get()
        yield composer


def strip(s):
    if s:
        return s.strip()


def clean(string):
    if string:
        return string.replace(",", '')
    else:
        return ''