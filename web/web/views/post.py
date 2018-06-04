from django.core.paginator import Paginator
from django.shortcuts import render
from web.models import Post


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
    return render(request, 'post_list.html',  locals())