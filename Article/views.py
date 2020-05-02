from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article
from Post.models import Post
import pdb
import math


# Create your views here.
def checkArticle(request):
    form = ArticleForm()
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            try:
                title = form.cleaned_data["title"]
                link = form.cleaned_data["link"]
                body = form.cleaned_data["body"]
                posted = form.cleaned_data["posted"]

                article = Article(title=title, link=link, body=body)
                article.save()

                if posted is True:
                    p = Post(article=article)
                    p.save()

                url = "https://localhost:8080/fakebox/check";
                headers = {'Content-Type': "application/x-www-form-urlencoded; charset=utf-8", 'title': title, 'content': body, 'url': link}
                response = requests.post(url, headers=headers)
                if response.status_code == 200:
                    print("Success !!!!!")
                return redirect(request, "evaluated.html", response)

            except:
                pass

    return render(request, "checkarticle.html", {'form': form})


@login_required
def viewArticle(request):
    art_list = Article.objects.filter(user=request.user)
    lst = []
    count = 0;
    for art in art_list:
        if count == 6:
            break
        else:
            ind = math.floor(count/3)
            if count%3 == 0:
                l = []
                lst.append(l)
            lst[ind].append(art)
            # print(ind, " ", count)
            count = count + 1
    print(lst)
    return render(request, "viewarticles.html", {'art_list': art_list, 'list': lst})

def about(request):
    return render(request, "aboutus.html")
