from turtle import title
from django.contrib.auth.models import AbstractUser
from django.db import models
from views import listing

class User(AbstractUser):
    pass

class Listing():
    title = models.CharField(max_length=30)
    description = models.TextField(max_length=512)
    starting_bid = models.DecimalField(max_length=12)
    current_bid = models.DecimalField(max_length=12)
    img_url = models.URLField()
    
    def __str__(self):
        return f"Title: {self.title},\n description: {self.description}, \n Starting bid: {self.starting_bid}, \n Image: {self.img_url}" 

class Bid(listing):
    pass

class Comment():
    pass

