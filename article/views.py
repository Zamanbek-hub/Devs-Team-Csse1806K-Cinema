from django.shortcuts import render, redirect
from django.http import HttpResponse
from article.models import *
from django.shortcuts import render, get_object_or_404
from article.forms import RegistrationForm, LoginForm
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.contrib.auth.models import User
from decimal import Decimal
from django.core.mail import send_mail
from django.conf import settings



# fuction for history
def history(request):
    user = User.objects.get(username=request.user.username)
    shops = user.shop_set.order_by('-date')
    return render(request, 'article/history_of_user.html', {"shops":shops})



# functions for index
def watched_films(shops_list, jenre):
    watched_films = []
    for w in shops_list:
        for w2 in w.movie_genre.all():
            if len(watched_films) == 2:
                break
            if jenre == w2:
                watched_films.append(w)
    watched_films = set(watched_films)
    return watched_films


def find_recomendation( block_list, jenre):
    try:
        new_movie = []
        for m in block_list:
            for g in m.movie_genre.all():
                if len(new_movie) == 2:
                    return new_movie
                if jenre == g:
                    new_movie.append(m)
        return new_movie
    except:
        return None

def add_3_recomend_film(block_list, shops_list, jenre):
    list_3_recomend = []
    for movie_1 in block_list:
        for genre_1 in movie_1.movie_genre.all():
            for genre_last_movie in shops_list[0].movie_genre.all():
                if genre_1.jenre == genre_last_movie.jenre and genre_last_movie.jenre != jenre.jenre:
                    list_3_recomend.append(movie_1)
                    list_3_recomend.append(genre_last_movie)
                    return list_3_recomend

def index(request):

    latest_movies = Block.objects.order_by('-movie_numberOfClicks')[0:12:1]
    jenres = Jenre.objects.order_by('-jenre')
    cinema = Cinema.objects.order_by('-cinema_name')

    list_genre = []
    shops_list = []
    block_list = list(Block.objects.all())

    count_of_max_genre = 0
    max_genre = ""

    try:
        currernt_user = User.objects.get(username=request.user.username)
        shops = currernt_user.shop_set.all()                          # all purchases of  current user

        for shop in shops:
            for new_movie in shop.of_movie.movie_genre.all():           # Добавление всех жанров
                list_genre.append(new_movie.jenre)

        for qwerty in list_genre:
            count = list_genre.count(qwerty)        # Находим максимальный жанр
            if count > count_of_max_genre:
                count_of_max_genre = count
                max_genre = qwerty

        jenre = Jenre.objects.get(jenre=max_genre)



        for movie_shop in shops:
            shops_list.append(movie_shop.of_movie)      # Берем только фильмы



        for movie in shops_list:
            for movie_block in block_list:
                if movie_block.movie_name == movie.movie_name:
                    block_list.remove(movie)

        x = find_recomendation(block_list, jenre)
        y = watched_films(shops_list, jenre)

        for movie in x:
            for movie_block in block_list:                            # Удаление уже рекомендованные фильмы
                if movie_block.movie_name == movie.movie_name:
                    block_list.remove(movie)


        for f1 in shops_list:               # Удаление с списка все просмотренные фильмы
            for f2 in block_list:
                if f1 == f2:
                    block_list.remove(f1)


        shops_list.reverse()
        list_3_recomend = (add_3_recomend_film(block_list, shops_list, jenre))

        if list_3_recomend is not None:
             x.append(list_3_recomend[0])

        recent = ""
        for l in y:
            recent += l.movie_name + " "

        if x is not None:
            return render(request, 'article/main.html', dict(latest_movies=latest_movies, jenres=jenres, cinema=cinema, special_movies=x, special_movie_jenre=jenre, recent = recent))
        else:
            return render(request, 'article/main.html', dict(latest_movies=latest_movies, jenres=jenres, cinema=cinema))
    except:
        return render(request, 'article/main.html', dict(latest_movies=latest_movies, jenres=jenres, cinema=cinema))





def movie_view(request,movie_name):
    try:
        latest_movies = Block.objects.order_by('-movie_numberOfClicks')[0:8:1]
        jenres = Jenre.objects.order_by('-jenre')
        cinema = Cinema.objects.order_by('-cinema_name')

        movie = Block.objects.get(movie_name = movie_name)
        movie.movie_numberOfClicks +=1
        movie.save()
        user = User.objects.get(id = request.user.id)
        rating = Rating.objects.get(of_movie = movie, of_user = user)
        return render(request, "article/movie_view.html", dict(movie=movie, rating=rating, latest_movies=latest_movies, jenres=jenres, cinema=cinema, special_movies=x,))
    except:
        return render(request, "article/movie_view.html", {"movie":movie})


def jenre_view(request, jenre):
    movie = Block.objects.filter(movie_genre=Jenre.objects.get(jenre=jenre))
    return render(request, "article/jenre.html", {"movie_by_jenres": movie})


def cinema_view(request, cinema_name):
    cinema = Cinema.objects.get(cinema_name=cinema_name)
    return render(request, "article/cinema_view.html", {"cinema": cinema})



def registration(request):
    try:
        form = RegistrationForm(request.POST or None)

        if form.is_valid():
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

        return render(request, 'article/registration.html', {'form': form})

    except:
        raise Http404('Something maybe you entered the data incorrectly')

def auto(request):
    try:
        form = LoginForm(request.POST or None)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            login_user = authenticate(username=username, password=password)

            if login_user:
                login(request, login_user)
                return HttpResponseRedirect(reverse('index'))

        return render(request, 'article/auto.html', {'form': form})

    except:
        raise Http404('Something maybe you entered the data incorrectly')


def set_Comment(request, movie_name):
    try:
        if request.POST.get("comment_text") == '':
            return HttpResponse('eMPTY')

        is_heiter = True
        if request.POST.get('heiter') == 'False':
            is_heiter = False

        comment_text = request.POST.get("comment_text")
        comment = Comment(of_user = User.objects.get(username= request.POST.get('username')), comment_text = comment_text,is_heiter = is_heiter, of_movie = Block.objects.get(movie_name=movie_name),comment_date=timezone.now())
        comment.save()

        return HttpResponseRedirect(reverse_lazy('movie_view', args=(Block.objects.get(movie_name=movie_name).movie_name,)))

    except:
        raise Http404('Something maybe you entered the data incorrectly')



def set_rating(request, movie_id):
    try:
        movie = get_object_or_404(Block, pk=movie_id)
        ratings = Rating.objects.filter(of_movie=movie)
        user = User.objects.get(id=request.user.id)

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

    except:
        return HttpResponseRedirect(reverse_lazy('movie_view', args=(movie.movie_name, )))


def search(request):

    try:

        searched_text = request.POST.get('searched_text')
        movie = None
        if len(searched_text)>0:
                movie = Block.objects.get(movie_name__contains=searched_text )
        return HttpResponseRedirect(reverse_lazy('movie_view', args=(movie.movie_name,)))

    except:
        raise Http404('Something maybe you entered the data incorrectly')

def buy_place(request,cinema_name):

    try:
        cinema = Cinema.objects.get(cinema_name = cinema_name)
        rooom = Room.objects.get(id=request.POST.get('room.id'))
        movie = Block.objects.get(movie_name=request.POST.get('movie_name'))
        message = ""
        email = request.POST.get('email')
        cinema = "*******" + cinema.cinema_name +  "*******"
        card = "Payed by card: " +  request.POST.get('check')
        type = "Type of tickets: " +  request.POST.get('type')
        room = "Room: " + str(rooom.name) + '\n' + "Places: " + '\n'
        message = cinema + '\n' + card + '\n' + type + '\n' + room
        status = request.POST.getlist('buy_place')
        for info in status:

            if info != "False":
                info = str(info).split(' ')
                cor_x = int(info[0])
                cor_y = int(info[1])
                message += "    " +  info[0] + " row " + info[1] + " place" + '\n'
                status = bool(info[2])
                new_place = Place(of_room = rooom, cor_x = cor_x, cor_y = cor_y, status = status)
                new_place.save()

        return HttpResponseRedirect(reverse_lazy('check', args=(message, email,movie.movie_name)))
                # return HttpResponseRedirect(reverse_lazy('buyticket', args=(movie.movie_name,)))
    except:
        raise Http404('Something maybe you entered the data incorrectly')

def set_places(places, x, room,limit):
    check = False

    for y in range(1, limit+1):
        for place in places:
            if place.cor_y == y:
                check = True
                break
        if check == False:
            new_place = Place(of_room = room, cor_x = x, cor_y=y, status=False)
            places.insert(y-1,new_place)
        check = False

    # sorting list
    for i in range(limit-1):
        for j in range(limit-i-1):
            if places[j].cor_y > places[j+1].cor_y:
                places[j], places[j+1] = places[j+1], places[j]

    return places

def buyticket(request,movie_name):
    try:
        movie = Block.objects.get(movie_name = movie_name)
        user = User.objects.get(username = request.user.username)
        shop = Shop(of_user = user, of_movie = movie, date = timezone.now() )
        shop.save()
        return HttpResponseRedirect(reverse_lazy('movie_view', args=(movie.movie_name,)))
    except:
        raise Http404('Something maybe you entered the data incorrectly')

def booking(request,cinema_name):
    try:
        numbers = [1,2,3,4,5,6,7,8]
        rooom = Room.objects.get(id=request.POST.get('room'))
        # return HttpResponse(request.POST.get('movie_name'))
        movie = Block.objects.get(movie_name=request.POST.get('movie_name'))
        user = User.objects.get(username=request.user.username)
        status = request.POST.getlist('buy_place')

        cinema = Cinema.objects.get(cinema_name = cinema_name)
        places_1 = Place.objects.filter(of_room = rooom, cor_x = int(1))
        places_1=list(places_1)

        places_1 = set_places(places_1,int(1),rooom,int(8))
        places_2 = Place.objects.filter(of_room = rooom, cor_x = int(2))
        places_2=list(places_2)

        places_2 = set_places(places_2,int(2),rooom,int(8))
        places_3 = Place.objects.filter(of_room = rooom, cor_x = int(3))
        places_3=list(places_3)

        places_3 = set_places(places_3,int(3),rooom,int(8))
        places_4 = Place.objects.filter(of_room = rooom, cor_x = int(4))
        places_4=list(places_4)

        places_4 = set_places(places_4,int(4),rooom,int(8))
        places_5 = Place.objects.filter(of_room = rooom, cor_x = int(5))
        places_5=list(places_5)

        places_5 = set_places(places_5,int(5),rooom,int(8))
        places_6 = Place.objects.filter(of_room = rooom, cor_x = int(6))
        places_6=list(places_6)

        places_6 = set_places(places_6,int(6),rooom,int(8))
        places_7 = Place.objects.filter(of_room = rooom, cor_x = int(7))
        places_7=list(places_7)

        places_7 = set_places(places_7,int(7),rooom,int(12))
        places_8 = Place.objects.filter(of_room = rooom, cor_x = int(8))
        places_8=list(places_8)

        places_8 = set_places(places_8,int(8),rooom,int(12))
        return render(request,'article/booking.html', {"cinema":cinema, "user":user,"movie":movie,"room":rooom, "places_1":places_1, "places_2":places_2,"places_3":places_3, "places_4":places_4,"places_5":places_5,"places_6":places_6,"places_7":places_7,"places_8":places_8,"numbers":numbers})
    except:
        return HttpResponse("Something maybe you entered the data incorrectly", status=404)


def check(request ,message,email,movie_name):
    try:
        subject = 'We wish you a pleasant viewing !  '
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email,]
        send_mail( subject, message, email_from, recipient_list )
        return HttpResponseRedirect(reverse_lazy('movie_view', args=(movie_name,)))
    except:
        return HttpResponse('Something Wrong')
