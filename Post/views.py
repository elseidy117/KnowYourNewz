from django.shortcuts import render
from .models import Post
import math


# Create your views here.

def viewPost(request):
    art_list = Post.objects.all()
    lst = []
    count = 0;
    for art in art_list:
        ind = math.floor(count/3)
        if count%3 == 0:
            l = []
            lst.append(l)
        lst[ind].append(art)
        # print(ind, " ", count)
        count = count + 1
    print(lst)
    return render(request, "posts.html", {'art_list': art_list, 'list': lst})
