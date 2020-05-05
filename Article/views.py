from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article
from Post.models import Post
import pdb
import math
import requests
import json
import numpy as np

#fucntion to check results
def resultFunc(score, mu, sigma2):
    n = np.size(sigma2, 1)
    m = np.size(sigma2, 0)
    if n == 1 or m == 1:
         sigma2 = np.diag(sigma2[0, :])
    X = score - mu;
    pi = math.pi
    det = np.linalg.det(sigma2)
    inv = np.linalg.inv(sigma2)
    val = np.reshape((-0.5)*np.sum(np.multiply((X@inv),X), 1),(np.size(X, 0), 1))
    p = np.power(2*pi, -n/2)*np.power(det, -0.5)*np.exp(val)
    return p

# Create your views here.
def checkArticle(request):
    form = ArticleForm()
    if request.method == "POST":
        print('inside post')
        form = ArticleForm(request.POST)
        if form.is_valid():
            print('form is valid')
            # try:
            title = form.cleaned_data["title"]
            link = form.cleaned_data["link"]
            body = form.cleaned_data["body"]
            posted = form.cleaned_data["posted"]

            data = {
                'url' : link,
                'title' : title,
                'content' : body,
            }
            #idhar se karna replace
            if request.user.is_authenticated:
                article = Article(title=title, link=link, body=body, user=request.user)
            else:
                article = Article(title=title, link=link, body=body)
            #yahan tak karna h change
            #article.save()
            response = requests.post(url = 'http://localhost:8080/fakebox/check', data = data)
            temp = json.loads(response.text)
            result = {}

            #prediction driver code
            u = np.array([[0.68244157, 0.68253419]])
            var = np.array([[0.01124549, 0.02151113]])
            # print(f'mean: {u} and sigma: {var}')

            #res = result(np.array([0.889, 0.908]), u, sigma2)
            res = resultFunc(np.array([temp['content']['score'], temp['title']['score']]), u, var)
            print(f'the result is {res}')
            

            if(res > 0.33):
                article.fake = False
                print(f'True')
                result['status'] = 'Real'
                result['article'] = article
                result['score'] = temp['title']['score'] + temp['content']['score']
                result['resp'] = temp
            else:
                article.fake = True
                print(f'False')
                result['status'] = 'Fake'
                result['article'] = article
                result['score'] = temp['title']['score'] + temp['content']['score']
                result['resp'] = temp
            
            print(f"The news is {result['status']}")
            article.save()

            if posted is True:
                print('posted if was true')
                p = Post(article=article)
                p.save()
            return render(request, "evaluated.html", {'result': result})

            # except:
            #     print('in exception')
        else:
            print('form is invalid')

    return render(request, "checkarticle.html", {'form': form})

#changes from here!!!!!
# @login_required
def viewArticle(request):
    if request.user.is_anonymous:
        return redirect('/login')
    else:
        #changes end here!!!!!!
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
