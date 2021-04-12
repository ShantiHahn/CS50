from django.contrib import admin
from django.contrib.auth.admin import UserAdmin # depuis la 
from .models import User, Auction_listing, Bid, Comment
# Register your models here.

admin.site.register(User)
admin.site.register(Auction_listing)
admin.site.register(Bid)
admin.site.register(Comment)