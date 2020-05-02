from django.urls import path
from . import views
from Post.views import viewPost

urlpatterns = [
	path("check/", views.checkArticle, name="checkArticle"),
	path("view/", views.viewArticle, name="viewArticles"),
	path("posts/", viewPost, name="viewPosts"),
	path("about/", views.about, name="about")
]
