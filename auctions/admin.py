from django.contrib import admin
from .models import Bid, Category, Comment, Listing, User, Watchlist

# Register your models here.
admin.site.register(Bid)
admin.site.register(Category)
admin.site.register(Comment)
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Watchlist)
