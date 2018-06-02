from django.shortcuts import render
from web.models import Post


def post_list(request):
    posts = Post.objects.order_by('-play_counts')[:24]
    return render(request, 'post_list.html', {'post': posts})