from enum import unique
from turtle import title
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=60, unique=True)
    description = models.CharField(max_length=512)
    start_bid = models.DecimalField(max_digits=8, decimal_places=2)
    highest_bid = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        default=0
    )    
    img_url = models.URLField(max_length=200)
    
    def __str__(self):
        return f"Title: \"{self.title}\". Bid starting @ ${self.start_bid}, current bid ${self.highest_bid}" 

class Bid(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)    
    current_bid = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        blank=True
    )

    def __str__(self):
        return f"User_id={self.user}, Listing_id={self.listing}"

class Comment():
    pass

class Watchlist(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    listing = models.ForeignKey('Listing', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"User_id={self.user}, Listing_id={self.listing}"