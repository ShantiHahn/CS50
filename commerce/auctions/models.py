from django.contrib.auth.models import AbstractUser
from django.db import models
from commerce import settings 

class Auction_listing(models.Model):

    active = models.BooleanField(default=True)
    seller = models.ForeignKey(settings.AUTH_USER_MODEL,default=1, on_delete= models.CASCADE, null=True)
    title = models.CharField(max_length=20)
    description = models.TextField()
    image = models.URLField(null=True)
    open_close= models.BooleanField(default=True)
    category = models.CharField(max_length= 50, null=True)

    def __str__(self):
        return f"{self.title} Description: {self.description} Category: {self.category}"


class User(AbstractUser):
    watchlist = models.ManyToManyField(Auction_listing)


class Bid(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1, on_delete= models.CASCADE, null=True)
    auction = models.ForeignKey(Auction_listing, on_delete= models.CASCADE)
    bid = models.FloatField(default=0)

    def __str__(self):
        return f" {self.auction.title} : bid {self.bid} from {self.user} id = {self.id}"

class Comment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1, on_delete= models.CASCADE)
    auction = models.ForeignKey(Auction_listing, on_delete= models.CASCADE)
    comment = models.TextField()


    def __str__(self):
        return f" {self.user} : said {self.comment} on {self.auction.title}"

# class Watchlist(models.Model):

#     user = models.ForeignKey(settings.AUTH_USER_MODEL,default=1, on_delete= models.CASCADE)
#     listing = models.ManyToManyField(Auction_listing, on_delete=models.CASCADE)

#     def __str__(self):
#         return f" {self.user} : has added {self.listing} "