from django.shortcuts import render

from web.models import Composer


def oneuser(request, cid):
    composer = Composer.get(cid=cid)
    posts = composer.get_posts(num=2)
    return render(request, 'oneuser.html', locals())


def homepage(request, cid):
    composer = Composer.get(cid=cid)
    first_post, *rest_posts = composer.get_posts()
    return render(request, 'homepage.html', locals())