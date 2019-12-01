from django.shortcuts import render, redirect
# from django import forms
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from article.models import *
from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from article.forms import RegistrationForm, LoginForm
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
import datetime
from django.utils import timezone
from django.contrib.auth.models import User
import datetime


# def index(request):
#     return HttpResponse("<h3>Hello world<h3>")


def test(request):
    return HttpResponse("<h3>Programm working<h3>")


def index(request):
    latest_movies = Block.objects.order_by('-movie_numberOfClicks')[0:8:1]
    jenres = Jenre.objects.order_by('-jenre')
    cinema = Cinema.objects.order_by('-cinema_name')
    return render(request, 'article/list.html', dict(latest_movies=latest_movies, jenres=jenres, cinema=cinema))


def table(request):
    return render(request, 'article/scheduleoffilms.html')


# Create your views here.

def movie_view(request,movie_name):
    movie = Block.objects.get(movie_name = movie_name)
    movie.movie_numberOfClicks +=1
    movie.save()
    return render(request, "article/movie_view.html", {"movie":movie})


def jenre_view(request, jenre):
    movie = Block.objects.filter(movie_genre=Jenre.objects.get(jenre=jenre))
    return render(request, "article/jenre.html", {"movie_by_jenres": movie})


def cinema_view(request, cinema_name):
    cinema = Cinema.objects.get(cinema_name=cinema_name)
    return render(request, "article/cinema_view.html", {"cinema": cinema})


def buyticket(request,movie_name):

        movie = Block.objects.get(movie_name = movie_name)
        user = User.objects.get(username = request.POST.get('username'))
        shop = Shop(of_user = user, of_movie = movie)
        shop.save()
        return HttpResponseRedirect(reverse_lazy('movie_view', args=(movie.movie_name,)))


# def category_view(request,category_name):
#     if category_name =

def authorization(request):
    # return HttpResponse("HELLO WORLD")
    return render(request, 'article/authorizationP.html')


def authorization(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)

        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form
    }
    return render(request, 'article/authorizationP.html')


def registration(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        # username = form.cleaned_data['username']
        # password = form.cleaned_data['password']
        # login_user = authenticate(username=username, password=password)
        # if login_user:
        #     login(request, login_user)

        # если мы работаем с формой основанная на модели то надо сделать так
        new_user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        email = form.cleaned_data['email']
        first_name = form.cleaned_data['first_name']
        last_name = form.cleaned_data['last_name']
        new_user.username = username
        new_user.set_password(password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.email = email
        new_user.save()
        login_user = authenticate(username=username, password=password)

        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse_lazy('index'))
    context = {
        'form': form
    }
    return render(request, 'article/registration.html', context)


def auto(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        login_user = authenticate(username=username, password=password)

        if login_user:
            login(request, login_user)
            return HttpResponseRedirect(reverse('index'))
    context = {
        'form': form
    }
    return render(request, 'article/auto.html', context)

def set_Comment(request, movie_name):
    # try:
        if request.POST.get("comment_text") == '':
            return HttpResponse('eMPTY')

        is_heiter = True
        if request.POST.get('heiter') == 'False':
            is_heiter = False

        comment_text = request.POST.get("comment_text")
        comment = Comment(of_user = User.objects.get(username= request.POST.get('username')), comment_text = comment_text,is_heiter = is_heiter, of_movie = Block.objects.get(movie_name=movie_name),comment_date=timezone.now())
        comment.save()
        return HttpResponseRedirect(reverse_lazy('movie_view', args=(Block.objects.get(movie_name=movie_name).movie_name,)))
        # {% url 'set_comment' movie.movie_name %}

        # comment_text ='none'
        # request.POST.set('comment_text') = comment_text
        # return HttpResponseRedirect(reverse('mainapp:movie', args=(moviex.id, )))
        # return HttpResponseRedirect(reverse('movie_view',movie_name))
        # return HttpResponseRedirect(reverse_lazy('movie_view {0}').format(movie_name))
        # return HttpResponseRedirect(reverse('article/movie_view.html' , {"movie":Block.objects.get(movie_name=movie_name)}))
    # except:
    #     return HttpResponse('Unsuccess')


# def listmovies(request,found_movies):
#     return render(request, "article/jenre.html", {"movie_by_jenres": found_movies})
#     return HttpResponseRedirect(reverse_lazy('listmovies', args=(movie, )))

def search(request):
    try:
        searched_text = request.POST.get('searched_text')
        found_movies = []
        # return HttpResponse(searched_text)
        movie = None
        if len(searched_text)>0:
                movie = Block.objects.get(movie_name__contains=searched_text )
        # return HttpResponse("Fail")
        # for movie in movies:
        #     if movie.movie_name.lower().count(searched_text) > 0 or movie.movie_explain.lower().count(searched_text) > 0:
        #         found_movies.append(movie)
        return HttpResponseRedirect(reverse_lazy('movie_view', args=(movie.movie_name,)))
    except:
        return HttpResponse("Have not")



def afisha(request):
    # return HttpResponse("HELLO WORLD")
    return render(request, 'article/kino1.html')

def booking(request):
    return render(request,'article/booking.html')

def get_info_about_cinema(request, cinema_name):
    cinema = Cinema.objects.get(cinema_name = cinema_name)
    return render(request,'article/cinemaInfoPage.html', {"cinema":cinema})
