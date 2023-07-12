from django.urls import path
from . import views

urlpatterns = [
    path("", views.ArticleListCreate.as_view(), name="article-home"),
    path("<str:pk>/", views.ArticleUpdate.as_view(), name="article-detail"),
]
