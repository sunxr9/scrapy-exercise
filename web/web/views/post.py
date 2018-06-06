from hashlib import md5

from django.core.paginator import Paginator
from django.shortcuts import render
from django.utils.functional import cached_property
from web.models import Post
from web.models import Comment

import redis
r = redis.Redis()


@cached_property
def count(self):
    sql, params = self.object_list.query.sql_with_params()
    sql = sql % params
    cache_key = md5(sql.encode('utf-8')).hexdigest()
    cache_counts = r.get(cache_key)
    if not cache_counts:
        cache_counts = self.object_list.count()
        r.setex(cache_key, cache_counts, 60 * 5)
    return int(cache_counts)


Paginator.count = count


def show_list(request, page=1):
    cur_page = int(page)
    posts = Post.objects.order_by('-play_counts')
    paginator = Paginator(posts, 24)
    posts = paginator.page(cur_page)
    page_num = 5
    first_page = 1
    last_page = paginator.num_pages
    if cur_page - page_num / 2 < 1:
        display_pages = range(cur_page, cur_page + page_num)
    elif cur_page + page_num /2 > last_page:
        display_pages = range(cur_page - page_num, cur_page + 1)
    else:
        display_pages = range(cur_page - page_num // 2, cur_page + page_num // 2 + 1)
    display_pages = list(display_pages)
    if posts.has_next():
        next_page = posts.next_page_number()
    if posts.has_previous():
        previous_page = posts.previous_page_number()
    if first_page not in display_pages:
        display_pages.insert(0, first_page)
    for post in posts:
        post.composers = post.get_composers()

        # for composers in post.composers:
        #     print('composers.values()', composers.values())
        #     print(type(composers))
        #     print('composers.avatar', composers['avatar'].values())
        #     print("composer.cid", composers.cid)

    return render(request, 'post_list.html',  locals())


def post_detail(request, pid):
    post = Post.get(pid=pid)
    composers = post.get_composers()
    return render(request, 'post_detail.html', {'post': post, 'composers': composers})


def get_comments(request):
    # 接受参数id ，page
    pid = request.GET.get('id')
    page = int(request.GET.get('page'))
    comment_list = Comment.objects.filter(pid=pid).order_by('-created_at')
    paginator = Paginator(comment_list, 10)
    comments = paginator.page(page)
    for comment in comments:
        if comment.reply:
            comment.reply = Comment.get(commentid=comment.reply)
    return render(request, 'comments.html', locals())

