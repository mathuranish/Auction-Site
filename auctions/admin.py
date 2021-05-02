from django.contrib import admin

from .models import User,Comments,Bid,Auction_Listings
# Register your models here.

admin.site.register(User)
admin.site.register(Auction_Listings)
admin.site.register(Comments)
admin.site.register(Bid)