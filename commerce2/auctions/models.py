from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction_listing(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    image = models.URLField()

    def __str__(self):
        return f"{self.title} Image: {self.image} Description: {self.description}"
    

class Bid(models.Model):

    auction = models.OneToOneField(Auction_listing, on_delete= models.CASCADE)
    bid = models.FloatField()

    def __str__(self):
        return f" {self.auction} : bid {self.bid}"

class Comments(models.Model):

    auction = models.OneToOneField(Auction_listing, on_delete= models.CASCADE)
    comment = models.TextField(max_length=300)


    def __str__(self):
        return f" {self.auction} : bid {self.comment}"
