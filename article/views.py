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
from decimal import Decimal


# def index(request):
#     return HttpResponse("<h3>Hello world<h3>")


# fuction for history
def history(request):
    return render(request, 'article/history_of_user.html')

def test(request):
    return HttpResponse("<h3>Programm working<h3>")


def watched_films(shops_list, jenre):
    watched_films = []
    for w in shops_list:
        for w2 in w.movie_genre.all():
            if jenre == w2:
                watched_films.append(w)
    watched_films = set(watched_films)
    return watched_films


def find_recomendation(list_genre, block_list, jenre):
    try:
        new_movie = []
        for m in block_list:
            for g in m.movie_genre.all():
                if len(new_movie) == 2:
                    return new_movie
                if jenre == g:
                    print(m.movie_genre)
                    new_movie.append(m)
        return new_movie
    except:
        return None


def index(request):
    latest_movies = Block.objects.order_by('-movie_numberOfClicks')[0:8:1]
    jenres = Jenre.objects.order_by('-jenre')
    cinema = Cinema.objects.order_by('-cinema_name')

    shop_list = []
    list_genre = []
    count_of_max_genre = 0
    max_genre = ""
    try:
        currernt_user = User.objects.get(username=request.user.username)
        shops = currernt_user.shop_set.all()
        for shop in shops:
            for new_movie in shop.of_movie.movie_genre.all():
                list_genre.append(new_movie.jenre)

        for qwerty in list_genre:
            count = list_genre.count(qwerty)
            if count > count_of_max_genre:
                count_of_max_genre = count
                max_genre = qwerty

        jenre = Jenre.objects.get(jenre=max_genre)

        shops_list = []
        for movie_shop in shops:
            shops_list.append(movie_shop.of_movie)
        block_list = list(Block.objects.all())
        for movie in shops_list:
            for movie_block in block_list:
                if movie_block.movie_name == movie.movie_name:
                    block_list.remove(movie)

        x = find_recomendation(list_genre, block_list, jenre)
        y = watched_films(shops_list, jenre)
        recent = ""
        for l in y:
            recent += l.movie_name + " "

        if x is not None:
            return render(request, 'article/list.html', dict(latest_movies=latest_movies, jenres=jenres, cinema=cinema, special_movies=x, special_movie_jenre=jenre, recent = recent))
        else:
            return render(request, 'article/list.html', dict(latest_movies=latest_movies, jenres=jenres, cinema=cinema))
    except:
        return render(request, 'article/list.html', dict(latest_movies=latest_movies, jenres=jenres, cinema=cinema))




def table(request):
    return render(request, 'article/scheduleoffilms.html')


# Create your views here.

def movie_view(request,movie_name):
    try:
        movie = Block.objects.get(movie_name = movie_name)
        movie.movie_numberOfClicks +=1
        movie.save()
        user = User.objects.get(id = request.user.id)
        rating = Rating.objects.get(of_movie = movie, of_user = user)
        return render(request, "article/movie_view.html", {"movie":movie, "rating" : rating})
    except:
        return render(request, "article/movie_view.html", {"movie":movie})


def jenre_view(request, jenre):
    movie = Block.objects.filter(movie_genre=Jenre.objects.get(jenre=jenre))
    return render(request, "article/jenre.html", {"movie_by_jenres": movie})


def cinema_view(request, cinema_name):
    cinema = Cinema.objects.get(cinema_name=cinema_name)
    return render(request, "article/cinema_view.html", {"cinema": cinema})


def buyticket(request,movie_name):
    try:
        movie = Block.objects.get(movie_name = movie_name)
        user = User.objects.get(username = request.POST.get('username'))
        shop = Shop(of_user = user, of_movie = movie, date = timezone.now() )
        shop.save()
        return HttpResponseRedirect(reverse_lazy('movie_view', args=(movie.movie_name,)))
    except:
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

def buy_place(request,cinema_name):
    cinema = Cinema.objects.get(cinema_name = cinema_name)
    rooom = Room.objects.get(id=4)
    status = request.POST.getlist('buy_place')

    for info in status:

        if info != "False":
            info = str(info).split(' ')
            cor_x = int(info[0])
            cor_y = int(info[1])
            status = bool(info[2])
            new_place = Place(of_room = rooom, cor_x = cor_x, cor_y = cor_y, status = status)
            new_place.save()

    return HttpResponseRedirect(reverse_lazy('booking', args=(cinema.cinema_name,)))

def afisha(request):
    # return HttpResponse("HELLO WORLD")
    return render(request, 'article/kino1.html')

def booking(request,cinema_name):
    rooom = Room.objects.get(id=4)
    cinema = Cinema.objects.get(cinema_name = cinema_name)
    places_1 = Place.objects.filter(of_room = rooom, cor_x = int(1))
    places_2 = Place.objects.filter(of_room = rooom, cor_x = int(2))
    places_3 = Place.objects.filter(of_room = rooom, cor_x = int(3))
    numbers = [1,2,3,4,5,6,7,8]
    have ={}
    check = False
    for num in numbers:
        for place in places_1:
            if place.cor_y == num :
                have[num] = 1
            else:
                if check == False:
                    have[num] = 0
                    check = True
        check = False

    return render(request,'article/booking.html', {"cinema":cinema, 'places_1':places_1, 'places_2':places_2,'places_3':places_3,'numbers':numbers, 'have':have})

def get_info_about_cinema(request, cinema_name):
    cinema = Cinema.objects.get(cinema_name = cinema_name)
    return render(request,'article/cinemaInfoPage.html', {"cinema":cinema})


def Check(request):
    user = User.objects.get(username = request.user.username)
    return render(request, 'article/scheduleoffilms.html', dict(user=user))

def set_rating(request, movie_id):
    movie = get_object_or_404(Block, pk=movie_id)
    ratings = Rating.objects.filter(of_movie=movie)
    user = User.objects.get(id=request.user.id)

    # for i in ratings:
    #     if i.of_user == user:
    #         return HttpResponseRedirect(reverse('movie_view', args=(movie.movie_name, )))

    rating_num = int(request.POST['new_rating'])
    new_rating = Rating(of_user=user, of_movie=movie, rating=rating_num)
    new_rating.save()

    sum_of_rating = movie.movie_rating * len(ratings) + rating_num
    if len(ratings) == 0:
        movie.movie_rating = sum_of_rating / (len(ratings) + 1)
    else:
        movie.movie_rating = sum_of_rating / (len(ratings) + 1)
    movie.movie_rating = round(movie.movie_rating,2)
    movie.save()


    return HttpResponseRedirect(reverse_lazy('movie_view', args=(movie.movie_name, )))
