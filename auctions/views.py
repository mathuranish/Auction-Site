from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Bid,Comments,Auction_Listings


def index(request):
    listings= Auction_Listings.objects.filter(is_closed=False) # .filter is used to get all objects.
    data= {
        'listings' : listings,
    }

    return render(request, "auctions/index.html",data)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def create_listings(request):
    if request.method == "POST":
        user= request.user
        title= request.POST["title"] 
        description= request.POST["description"]       
       
        category= request.POST["category"]
        image_url= request.POST["image_url"]

        #saving data in Bid database.
        bid=Bid( bid = float( request.POST["bid"]),user=user)
        bid.save()

        #saving data in Auction_Listings database.
        listing=Auction_Listings(title= title, description=description, owner=user,bid=bid, url= image_url, category=category, is_closed=False)
        listing.save()
        return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/create_listings.html")


def product_page(request, listing_id):
    listing= Auction_Listings.objects.get(pk=listing_id) # .get isto get only one object.
    comments = listing.comments.all()    # stores all comments associated with product.
    
    in_watchlist= request.user in listing.watchlist.all()# check if user has watchlisted this product.
    is_user= request.user.username == listing.owner.username

    data= {
        'listing' : listing,
        'comments' : comments,
        'in_watchlist' : in_watchlist,
        'is_user': is_user,
    }
    return render(request, "auctions/product_page.html",data)


def new_bid(request, listing_id):
    listing= Auction_Listings.objects.get(pk=listing_id)
    current_bid= listing.bid.bid 
    new_bid=float(request.POST["new_bid"])
    if new_bid > current_bid:
        updated_bid= Bid(bid= new_bid, user=request.user)
        updated_bid.save()
        listing.bid= updated_bid
        listing.save()

        data={
            'update_message' : "You are now the heightst bidder",
            'is_updated': True,
            'listing': listing,
        }
        return render(request, "auctions/product_page.html",data)
    else:
        data={
            'update_message' : "Bid Higher!",
            'is_updated': False,
            'listing': listing,
        }
        return render(request, "auctions/product_page.html",data)

def new_comment(request, listing_id):
    listing= Auction_Listings.objects.get(pk=listing_id)
    text=  str(request.POST["comment"])
    comment = Comments(text= text, written_by=request.user,listing=listing)
    comment.save()
    return HttpResponseRedirect(reverse("product_page", args=[listing_id]))


def watchlist(request):
    user= request.user
    listings= user.watchlist.all()
    data ={
        'listings' : listings
    }

    return render(request, "auctions/index.html",data)

def add_to_watchlist(request, listing_id):
    user = request.user
    listing= Auction_Listings.objects.get(pk=listing_id)
    listing.watchlist.add(user)
    return HttpResponseRedirect(reverse("product_page", args=[listing_id]))

def remove_from_watchlist(request, listing_id):
    user = request.user
    listing= Auction_Listings.objects.get(pk=listing_id)
    listing.watchlist.remove(user)
    return HttpResponseRedirect(reverse("product_page", args=[listing_id]))

def close_listing(request, listing_id):
    listing= Auction_Listings.objects.get(pk=listing_id)
    listing.is_closed=True
    listing.save()
    return HttpResponseRedirect(reverse("product_page", args=[listing_id]))

def closed_listings(request):
    listings= Auction_Listings.objects.filter(is_closed=True)
    data= {
        'listings' : listings,
    }

    return render(request, "auctions/index.html",data)

def categories(request):
    woodwork= Auction_Listings.objects.filter(category="Woodwork").count()
    antiques= Auction_Listings.objects.filter(category="Antiques").count()
    famous= Auction_Listings.objects.filter(category="Famous").count()
    tech= Auction_Listings.objects.filter(category="Tech").count()
    data={
        'woodwork_count' : woodwork,
        'antiques_count' : antiques,
        'famous_count' : famous,
        'tech_count' : tech,
    }
    return render(request, "auctions/categories.html", data)

def categories_page(request):
    cat= request.POST['category']
    listings= Auction_Listings.objects.filter(category=cat)
    data= {
        'listings' : listings,
    }

    return render(request, "auctions/index.html",data)
