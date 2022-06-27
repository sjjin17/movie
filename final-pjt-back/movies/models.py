from django.db import models
from django.conf import settings

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MoviePeople(models.Model):
    name = models.CharField(max_length=100)
    also_known_as = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Provider(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=100)
    overview = models.TextField()
    poster_path = models.TextField()
    now_playing = models.BooleanField(default=False)
    release_date = models.DateField()
    popularity = models.FloatField()  # ERD에서는 IntegerField로 적었지만 선호도와 평점은 소수점이 있으므로 FloatField로 작성하였습니다.
    vote_average = models.FloatField()
    runtime = models.IntegerField()
    video_path = models.TextField()
    save_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='save_movies')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_movies')  
    genres = models.ManyToManyField(Genre, related_name='movies_genres')
    actors = models.ManyToManyField(MoviePeople, related_name='movies_actors')   # related_name이 genre와 같아도 되는지 몰라서 일단 임의지정했습니다.
    directors = models.ManyToManyField(MoviePeople, related_name='movies_directors')
    watch_providers = models.ManyToManyField(Provider, related_name='movies_providers') 

    def __str__(self):
        return self.title


class OneLineComment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    content = models.CharField(max_length=50)
    star_rate = models.FloatField()
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_line_reviews')

    def __str__(self):
        return self.content
    




