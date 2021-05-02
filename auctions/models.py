from django.contrib.auth.models import AbstractUser
from django.db import models



class User(AbstractUser):   
    pass


class Bid(models.Model):
    bid=models.FloatField(default=0)
    user=models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"${self.bid}"

class Auction_Listings(models.Model):
    title= models.CharField(max_length=30)
    description= models.TextField(max_length=500)
    bid= models.ForeignKey(Bid,on_delete=models.CASCADE,default=None,related_name="auction_listings")
    owner= models.ForeignKey(User, on_delete=models.CASCADE,related_name="auction_listings")
    url= models.CharField(max_length=1000)
    category= models.CharField(max_length=15,null=True, blank=True)
    watchlist=models.ManyToManyField(User,related_name="watchlist",null=False,default=None,blank=True)
    is_closed=models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title}: {self.bid}"

class Comments(models.Model):
    text= models.TextField(max_length=400)
    written_by= models.ForeignKey(User, on_delete=models.CASCADE,related_name="comments")
    listing= models.ForeignKey(Auction_Listings, on_delete=models.CASCADE,related_name="comments")