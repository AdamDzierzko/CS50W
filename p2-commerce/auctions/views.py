from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Category, Listing, Watchlist, Bid, Comment

from .models import User


def index(request):

    listings = Listing.objects.all()
    user_id = request.user.id
    watchlist = Watchlist.objects.filter(user_id = user_id)
    w = []
    for i in range(len(watchlist)):
        if not watchlist[i].listing_id.id in w:
            w.append(watchlist[i].listing_id.id)

    bids = Bid.objects.all()
    price = []

    for j in range(len(bids)):
        if not bids[j].listing_id in price:
            price.append(bids[j].listing_id.id)

    return render(request, "auctions/index.html", {
        "listings" : listings,
        "watchlist" : w,
        "bids" : bids,
        "price" : price
    })


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

def create(request):
    if request.method == "POST":

        listing = Listing()
        listing.title = request.POST["title"]
        listing.description = request.POST["description"]
        listing.price = request.POST["start"]
        listing.start = request.POST["start"]
        listing.image = request.POST["image"]
        listing.owner = request.user.username
        listing.category = Category.objects.get(pk=request.POST["category"])
        listing.save()

        return redirect('index')
    else:
        return render(request, "auctions/create.html", {
            "categories" : Category.objects.all()
        })

def categories(request):

    if request.method == "POST":

        cat = Category()
        cat.categoryName = request.POST["categoryName"]
        cat.save()

        return render(request, "auctions/index.html")
    else:
        return render(request, "auctions/categories.html", {
            "categories" : Category.objects.all()
        })

def category(request, categoryName):

    aa = Category.objects.filter(categoryName = categoryName)
    name = aa[0].id
    b = Listing.objects.filter(category = name)

    user_id = request.user.id
    watchlist = Watchlist.objects.filter(user_id = user_id)
    w = []
    for i in range(len(watchlist)):
        if not watchlist[i].listing_id.id in w:
            w.append(watchlist[i].listing_id.id)

    bids = Bid.objects.all()
    price = []

    for j in range(len(bids)):
        if not bids[j].listing_id in price:
            price.append(bids[j].listing_id.id)

    return render(request, "auctions/category.html", {
        "listings" : b,
        "category" : categoryName,
        "watchlist": w,
        "bids": bids,
        "price": price
    })

def watchlist(request, user_id):

    listings = Listing.objects.all()
    watchlist = Watchlist.objects.filter(user_id = user_id)
    w = []
    for i in range(len(watchlist)):
        if not watchlist[i].listing_id.id in w:
            w.append(watchlist[i].listing_id.id)

    bids = Bid.objects.all()
    price = []

    for j in range(len(bids)):
        if not bids[j].listing_id in price:
            price.append(bids[j].listing_id.id)

    return render(request, "auctions/watchlist.html", {
        "listings" : listings,
        "watchlist" : w,
        "bids": bids,
        "price": price
    })

def addToWatchlist(request, listing_id):

    user_id = request.user.id
    user = User.objects.filter(id = user_id).first()
    listing = Listing.objects.filter(id = listing_id).first()

    watchlist = Watchlist()
    watchlist.user_id = user
    watchlist.listing_id = listing
    watchlist.save()

    return redirect('watchlist', user_id)

def removeFromWatchlist(request, listing_id):

    user_id = request.user.id

    watch = Watchlist.objects.filter(user_id = user_id, listing_id = listing_id)
    watch.delete()

    return redirect('watchlist', user_id)

def one(request, id):

    el = Listing.objects.filter(id = id).first()
    a = []
    a.append(el)

    com = Comment.objects.filter(listing_id = el.id)

    bids = Bid.objects.all()
    price = []

    for j in range(len(bids)):
        if not bids[j].listing_id in price:
            price.append(bids[j].listing_id.id)

    user_id = request.user.id
    user_name = request.user.username
    watchlist = Watchlist.objects.filter(user_id = user_id)
    w = []
    for i in range(len(watchlist)):
        if not watchlist[i].listing_id.id in w:
            w.append(watchlist[i].listing_id.id)

    mes = 0

    return render(request, "auctions/one.html", {
        "listings" : a,
        "comments": com,
        "watchlist": w,
        "bids" : bids,
        "price" : price,
        "us" : user_name,
        "mes": mes
    })

def riseBid(request, listing_id):

    user_id = request.user.id

    user = User.objects.filter(id = user_id).first()
    listing = Listing.objects.filter(id = listing_id).first()


    a = Bid.objects.filter(listing_id = listing_id).first()
    if a == None:
        bid = Bid()
        bid.user_id = user
        bid.listing_id = listing
        bid.bid = request.POST["bid"]
        bid.numberOfBids = 1
        bid.save()
    else:
        a.user_id = user
        a.listing_id = listing
        if a.bid < float(request.POST["bid"]):
            a.bid = request.POST["bid"]

        else:
            b = []
            b.append(listing)
            com = Comment.objects.filter(listing_id=listing.id)

            bids = Bid.objects.all()
            price = []

            for j in range(len(bids)):
                if not bids[j].listing_id in price:
                    price.append(bids[j].listing_id.id)

            user_name = request.user.username
            watchlist = Watchlist.objects.filter(user_id=user_id)
            w = []
            for i in range(len(watchlist)):
                if not watchlist[i].listing_id.id in w:
                    w.append(watchlist[i].listing_id.id)

            mes = 1

            return render(request, "auctions/one.html", {
                "listings": b,
                "comments": com,
                "watchlist": w,
                "bids": bids,
                "price": price,
                "us": user_name,
                "mes": mes
            })

        a.numberOfBids += 1
        a.save()

    return redirect('one', id=listing_id)

def addComment(request, listing_id):

    user_id = request.user.id

    user = User.objects.filter(id = user_id).first()
    listing = Listing.objects.filter(id = listing_id).first()

    com = Comment()
    com.user_id = user
    com.listing_id = listing
    com.comment = request.POST["comment"]
    com.save()

    return redirect('one', id=listing_id)

def close(request, listing_id):

    listing = Listing.objects.filter(id = listing_id).first()

    listing.status = 0
    listing.save()

    return redirect('one', id=listing_id)

def winns(request):

    user_id = request.user.id

    listings = Listing.objects.all()
    bids = Bid.objects.filter(user_id = user_id)

    return render(request, "auctions/winns.html", {
        "listings": listings,
        "bids": bids
        })

def my(request):

    user_name = request.user.username
    listings = Listing.objects.filter(owner = user_name)

    bids = Bid.objects.all()

    return render(request, "auctions/my.html", {
        "listings": listings,
        "bids": bids
    })
