import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.core.paginator import Paginator


from .models import User, Post, Follow, Like


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@csrf_exempt
@login_required
def add(request):

    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)

    text = data.get("text", "")
    post = Post()
    post.user = request.user
    post.text = text
    post.timestamp = datetime.datetime.now()
    post.save()

    return JsonResponse({"message": "Email sent successfully."}, status=201)

def index(request):
    posts = Post.objects.all()
    posts = posts.order_by("-timestamp").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    like = Like.objects.filter(user_id = request.user.id)
    likes = []
    for l in like:
        likes.append(l.post_id.id)

    id = -1
    w = 1           # index
    return render(request, "network/index.html", {
        "page_obj" : posts,
        "id" : id,
        "likes" : likes,
        "w" : w
    })

@csrf_exempt
@login_required
def edit(request, id):

    if request.method == "PUT":

        data = json.loads(request.body)
        postid = data.get("postid", "")
        post = Post.objects.get(id = postid)
        post.text = data.get("text", "")
        post.save()

        return JsonResponse({"message": "Email sent successfully."}, status=201)

    else:
        posts = Post.objects.all()
        posts = posts.order_by("-timestamp").all()

        paginator = Paginator(posts, 10)
        page_number = request.GET.get('page')
        posts = paginator.get_page(page_number)

        like = Like.objects.filter(user_id=request.user.id)
        likes = []
        for l in like:
            likes.append(l.post_id.id)

        w = 1  # edit
        return render(request, "network/index.html", {
            "page_obj" : posts,
            "id" : id,
            "likes": likes,
            "w" : w
        })

@csrf_exempt
@login_required
def like(request, id):

    post = Post.objects.get(id=id)
    post.numberOfLikes = post.numberOfLikes + 1
    post.save()

    like = Like()
    like.user_id = request.user
    like.post_id = post
    like.save()

    return JsonResponse({"message": "Email sent successfully."}, status=201)

@csrf_exempt
@login_required
def dislike(request, id):

    post = Post.objects.get(id=id)
    post.numberOfLikes = post.numberOfLikes -1
    post.save()

    like = Like.objects.get(user_id= request.user, post_id=post)
    like.delete()

    return JsonResponse({"message": "Email sent successfully."}, status=201)

def profil(request, id):

    posts = Post.objects.filter(user = id)
    posts = posts.order_by("-timestamp").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    like = Like.objects.filter(user_id = request.user.id)
    likes = []
    for l in like:
        likes.append(l.post_id.id)

    followed = []
    follow = Follow.objects.filter(follower_id = request.user.id)

    for f in follow:
        followed.append(f.following_id)
    w = 2   # profil

    profil = User.objects.get(id=id)

    return render(request, "network/index.html", {
        "page_obj" : posts,
        "id" : id,
        "likes" : likes,
        "w" : w,
        "followed" : followed,
        "profil" : profil
    })

@csrf_exempt
@login_required
def follow(request, id):

    follow = Follow()
    follow.follower_id = request.user
    follow.following_id = id
    follow.save()

    user = User.objects.get(id = request.user.id)
    user.numberOfFollowing = user.numberOfFollowing + 1
    user.save()

    user = User.objects.get(id = id)
    user.numberOfFollowers = user.numberOfFollowers + 1
    user.save()

    return JsonResponse({"message": "Email sent successfully."}, status=201)

@csrf_exempt
@login_required
def unfollow(request, id):

    follow = Follow.objects.filter(follower_id = request.user.id, following_id=id)
    follow.delete()

    user = User.objects.get(id = request.user.id)
    user.numberOfFollowing = user.numberOfFollowing - 1
    user.save()

    user = User.objects.get(id = id)
    user.numberOfFollowers = user.numberOfFollowers - 1
    user.save()

    return JsonResponse({"message": "Email sent successfully."}, status=201)

def following(request):

    followed = []
    follow = Follow.objects.filter(follower_id=request.user.id)
    for f in follow:
        followed.append(f.following_id)

    posts = Post.objects.filter(user__in = followed)
    posts = posts.order_by("-timestamp").all()

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)

    like = Like.objects.filter(user_id = request.user.id)
    likes = []
    for l in like:
        likes.append(l.post_id.id)

    id = -1
    w = 3           # following
    return render(request, "network/index.html", {
        "page_obj" : posts,
        "id" : id,
        "likes" : likes,
        "w" : w
    })
