from django.shortcuts import render

from web.models import Composer

def oneuser(request, cid):
    composer = Composer.objects.get(cid=cid)
    return render(request, 'oneuser.html', locals())