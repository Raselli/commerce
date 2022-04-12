from turtle import title
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing():
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=512)
    starting_bid = models.DecimalField(max_length=12)
    img_url = models.URLField()
    pass

class Bid():
    pass

class Comment():
    pass

