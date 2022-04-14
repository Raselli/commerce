from turtle import title
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(
        max_length=60
    )
    
    description = models.CharField(
        
        max_length=512
    )
    
    start_bid = models.DecimalField(
        max_digits=8, 
        decimal_places=2
    )
    
    current_bid = models.DecimalField(
        max_digits=8, 
        decimal_places=2,
        default = 0
    )    
    
    img_url = models.URLField(
        max_length=200
    )
    
    def __str__(self):
        return f"Title: \"{self.title}\". Bid starting @ ${self.start_bid}, current bid ${self.current_bid}" 

class Bid():
    pass

class Comment():
    pass

