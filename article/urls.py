from django.urls import path
from . import views
from article.models import *
from django.views.generic import ListView, DetailView
from django.contrib.auth.views import LogoutView
from django.urls import reverse, reverse_lazy

# app_name = 'article'
urlpatterns = [
    path('', views.index, name='index'),
    # path('cinemas/', views.listCinema, name='listcinema'),
    path('test/', views.test, name='test'),
    path('table/', views.table, name='table'),
    path('authorizationP/', views.authorization, name='authorization'),
    path('movie/<movie_name>/', views.movie_view, name='movie_view'),
    path('movies_by/<jenre>/', views.jenre_view, name='jenre_view'),
    path('cinema/<cinema_name>/', views.cinema_view, name='cinema_view'),
    path('registration/', views.registration, name='registration'),
    path('auto/', views.auto, name='auto'),
    path('search/', views.search, name='search'),
    path('logout/', LogoutView.as_view(next_page=reverse_lazy('index')), name='logout'),
    path('set_comment/<movie_name>', views.set_Comment, name='set_comment'),
    path('buyticket/<movie_name>', views.buyticket, name='buyticket'),
    path('set_rating/<movie_id>', views.set_rating, name='set_rating'),
    path('buy_place/<cinema_name>', views.buy_place, name='buy_place'),
    # path('list/', views.listmovies, name='listmovies'),
    path('afisha/', views.afisha, name='afisha'),
    path('booking/<cinema_name>', views.booking, name='booking'),
    path('info/', views.get_info_about_cinema, name='info'),
    path('check/', views.Check, name='check'),
    path('history/', views.history, name='history'),
]
