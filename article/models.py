import datetime
from django.utils import timezone
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db import models
# import jsonfield
# from django.db import models
# from django.contrib.postgres.fields import JSONField

class Article(models.Model):
    article_title = models.CharField('Name of article', max_length = 200)
    article_text = models.TextField('Text of Article')
    pub_date = models.DateTimeField('Date of publication')

    def __str__(self):
        return self.article_title

    def was_published_recently(self):
        return self.pub_date >= (timezone.now() - datetime.timedelta(days = 7))


class Jenre(models.Model):
    jenre = models.CharField('Jenre of Movie', max_length = 30)

    def __str__(self):
        return self.jenre

    def get_absolute_url(self):
        return reverse('jenre_view', kwargs={'jenre':self.jenre})

class Cinema(models.Model):
    cinema_name = models.CharField('Name_of_cinema', max_length = 30,)
    area = models.PositiveIntegerField()
    cinema_address = models.CharField('cinema_address', max_length = 30,default='71')
    cinema_poster = models.CharField(max_length=100,default="http://thumbs.dfs.ivi.ru/storage4/contents/8/5/25df26b4ff265c284df18453f62ac7.jpg")
    cinema_movie_discouns = models.FloatField()

    def __str__(self):
        return self.cinema_name

    def get_absolute_url(self):
        return reverse('cinema_view', kwargs={'cinema_name':self.cinema_name})

    def get_absolute_url_to_book(self):
        return reverse('booking', kwargs={'cinema_name':self.cinema_name})

class Block(models.Model):

    move_img = models.ImageField(upload_to="movie_image",blank=True)
    movie_explain =models.TextField('Explain of Movie')
    movie_name=models.CharField('movie_name', max_length = 50)
    movie_rating = models.FloatField(default=0.0)
    movie_numberOfClicks = models.IntegerField(default=0)
    movie_article_date = models.DateTimeField('date published')
    movie_trailer_url = models.CharField("movie_trailer",max_length = 100,default="https://www.youtube.com/embed/L0ttxMz-tyo")
    movie_available = models.BooleanField(default=True)
    movie_genre = models.ManyToManyField(Jenre)
    movie_cinema = models.ManyToManyField(Cinema)
    movie_price = models.PositiveIntegerField()
    movie_duration = models.DurationField(default=timedelta())
    movie_poster_img_url = models.CharField(max_length=100,default="http://thumbs.dfs.ivi.ru/storage4/contents/8/5/25df26b4ff265c284df18453f62ac7.jpg")


    def __str__(self):
        return self.movie_name

    def get_absolute_url(self):
        return reverse('movie_view', kwargs={'movie_name':self.movie_name})

class Room(models.Model):
     of_cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE)
     of_movie = models.ForeignKey(Block, on_delete=models.CASCADE)
     name = models.PositiveIntegerField()

     def __str__(self):
         return "Room: " + str(self.name) + '\n' +"Cinema: " + str(self.of_cinema.cinema_name) + " moviw: " +str(self.of_movie.movie_name)

class Place(models.Model):
     of_room = models.ForeignKey(Room, on_delete=models.CASCADE)
     cor_x = models.PositiveIntegerField()
     cor_y = models.PositiveIntegerField()
     status = models.BooleanField()

     def __str__(self):
         return "Room: " + str(self.of_room.name) + " row: " + str(self.cor_x) + " column: " + str(self.cor_y)

class Comment(models.Model):
    comment_date = models.DateTimeField('Date of set')
    comment_text = models.TextField('Text', max_length = 200)
    of_user = models.ForeignKey(User,on_delete=models.CASCADE, related_name="User")
    of_movie = models.ForeignKey(Block,on_delete=models.CASCADE)
    is_heiter = models.BooleanField(default=True)

    def __str__(self):
        return self.comment_text

    def is_valid(self):
        pass

class Shop(models.Model):
    of_user = models.ForeignKey(User,on_delete=models.CASCADE)
    of_movie = models.ForeignKey(Block,on_delete=models.CASCADE)
    date =  models.DateTimeField('Date of shop')
    def __str__(self):
        return "buyer: " + self.of_user.username + " movie" + self.of_movie.movie_name

class Rating(models.Model):
    of_user = models.ForeignKey(User,on_delete=models.CASCADE)
    of_movie = models.ForeignKey(Block,on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
