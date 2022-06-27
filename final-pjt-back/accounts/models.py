from django.db import models
from django.contrib.auth.models import AbstractUser
from movies.models import Genre


class User(AbstractUser):
    profile_img = models.ImageField(upload_to='profile-images/', default='default.jpg')
    nickname = models.CharField(max_length=15, unique=True)
    hate_genre =  models.ManyToManyField(Genre, related_name='hate_user')
    followings = models.ManyToManyField('self', symmetrical=False, related_name='followers')

