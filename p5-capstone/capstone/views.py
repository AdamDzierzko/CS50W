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

from .models import User, Movie, Coment, Grade, Actor, Genere, ActorMovie


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
        return render(request, "capstone/login.html", { } )


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
            return render(request, "capstone/register.html", {
                "message": "Passwords must match."
            })
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "capstone/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "capstone/register.html", { } )

def index(request):

    movies = Movie.objects.all()
    movies = movies.order_by("-timestamp").all()
    f = 1   # show all movies
    movieactors = ActorMovie.objects.all()
    actors = Actor.objects.all()

    user = request.user
    grades = Grade.objects.all()
    gr = []
    for grade in grades:
        for movie in movies:
            if ( grade.user_id == user and grade.movie_id.id == movie.id):
                a = movie.id
                gr.append(a)

    g_mo = {}
    for movie in movies:
        g = 0
        if movie.numberOfGrades :
            movie_grades = Grade.objects.filter(movie_id=movie)
            sum = 0
            for mg in movie_grades:
                sum = sum + mg.grade
            g = sum / movie.numberOfGrades
            round(g,1)
        u = request.user.id
        g_mo[movie.id] = [g,u]

    print(g_mo)
    coment_id = -1
    g = 0

    return render(request, "capstone/index.html", {
        "movies": movies,
        "f": f,
        "movieactors": movieactors,
        "actors" : actors,
        "gr" : gr,
        "g_mo" : g_mo,
        "coment_id": coment_id,
        "grades": grades,
        "g": g,
    } )

@csrf_exempt
@login_required
def addmovie(request):

    if request.method == "POST":

        data = json.loads(request.body)

        actors = data.get("actors", "")
        genere_id = data.get("genere", "")
        title = data.get("title", "")
        director = data.get("director", "")
        description = data.get("description", "")
        year = data.get("year", "")

        movie = Movie()
        movie.genere = Genere.objects.get(pk=genere_id)
        movie.user = request.user
        movie.title = title
        movie.director = director
        movie.description = description
        movie.year = year
        movie.timestamp = datetime.datetime.now()
        movie.numberOfComents = 0
        movie.numberOfGrades = 0
        movie.save()

        for i in range(len(actors)):
            actormovie = ActorMovie()
            actormovie.movie_id = Movie.objects.get(pk=movie.id)
            actormovie.actor_id = Actor.objects.get(pk=actors[i])
            actormovie.save()

        return JsonResponse({"message": "OK"}, status=201)

    else:
        maxyear = datetime.datetime.now().year
        f = 2       # add new movie
        generes = Genere.objects.all()
        actors = Actor.objects.all()

        return render(request, "capstone/index.html", {
            "maxyear" : maxyear,
            "f" : f,
            "generes": generes,
            "actors": actors,
        } )


@csrf_exempt
@login_required
def edit_movie(request, movie_id):

    if request.method == "PUT":

        data = json.loads(request.body)
        actors = data.get("actors", "")
        genere_id = data.get("genere", "")
        title = data.get("title", "")
        director = data.get("director", "")
        description = data.get("description", "")
        year = data.get("year", "")

        movie = Movie.objects.get(pk=movie_id)
        movie.genere = Genere.objects.get(pk=genere_id)
        movie.title = title
        movie.director = director
        movie.description = description
        movie.year = year
        movie.timestamp = datetime.datetime.now()
        movie.save()

        am = ActorMovie.objects.filter(movie_id=movie)
        am.delete()

        for i in range(len(actors)):
            actormovie = ActorMovie()
            actormovie.movie_id = Movie.objects.get(pk=movie.id)
            actormovie.actor_id = Actor.objects.get(pk=actors[i])
            actormovie.save()

        return JsonResponse({"message": "OK"}, status=201)

    else:
        movie = Movie.objects.get(pk=movie_id)
        maxyear = datetime.datetime.now().year
        f = 6  # edit movie
        generes = Genere.objects.all()
        actors = Actor.objects.all()

        a = ActorMovie.objects.filter(movie_id=movie)
        actormovie = []
        for am in a:
            actormovie.append(am.actor_id)

        return render(request, "capstone/index.html", {
            "maxyear": maxyear,
            "f": f,
            "generes": generes,
            "actors": actors,
            "movie": movie,
            "actormovie": actormovie,
        })

def config(request):

    f = 3       # config
    generes = Genere.objects.all()
    generes = generes.order_by("genere_name").all()

    actors = Actor.objects.all()
    actors = actors.order_by("actor_name").all()

    return render(request, "capstone/index.html", {
        "actors": actors,
        "generes": generes,
        "f": f
    } )

@csrf_exempt
@login_required
def addgenere(request):

    data = json.loads(request.body)
    genere_name = data.get("genere_name", "")
    genere = Genere()
    genere.genere_name = genere_name
    genere.save()

    return JsonResponse({"message": "OK"}, status=201)

@csrf_exempt
@login_required
def addactor(request):

    data = json.loads(request.body)
    actor_name = data.get("actor_name", "")
    actor = Actor()
    actor.actor_name = actor_name
    actor.save()

    return JsonResponse({"message": "OK"}, status=201)

@login_required
def delete_movie(request, movie_id):

    grades = Grade.objects.filter(movie_id=movie_id)
    grades.delete()

    actormovie = ActorMovie.objects.filter(movie_id=movie_id)
    actormovie.delete()

    coments = Coment.objects.filter(movie_id=movie_id)
    coments.delete()

    movie = Movie.objects.get(pk=movie_id)
    movie.delete()

    return HttpResponseRedirect(reverse("index"))

@csrf_exempt
@login_required
def addgrade(request):

    data = json.loads(request.body)
    grade = data.get("grade", "")
    movie_id = data.get("movie_id", "")

    movie = Movie.objects.get(pk=movie_id)

    g = Grade()
    g.user_id = request.user
    g.movie_id = movie
    g.grade = grade
    g.save()

    movie.numberOfGrades = movie.numberOfGrades + 1
    movie.save()

    return JsonResponse({"message": "OK"}, status=201)

@csrf_exempt
@login_required
def edit_grade(request, grade_id):

    if request.method == "PUT":

        data = json.loads(request.body)
        grade = data.get("grade", "")

        g = Grade.objects.get(pk=grade_id)
        g.grade = grade
        g.save()

        return JsonResponse({"message": "OK"}, status=201)

    else:

        movies = Movie.objects.all()
        movies = movies.order_by("-timestamp").all()
        f = 1  # show all movies
        movieactors = ActorMovie.objects.all()
        actors = Actor.objects.all()

        user = request.user
        grades = Grade.objects.all()
        gr = []
        for grade in grades:
            for movie in movies:
                if (grade.user_id == user and grade.movie_id.id == movie.id):
                    a = movie.id
                    gr.append(a)

        g_mo = {}
        for movie in movies:
            if movie.numberOfGrades:

                movie_grades = Grade.objects.filter(movie_id=movie)
                sum = 0
                for mg in movie_grades:
                    sum = sum + mg.grade
                g = sum / movie.numberOfGrades
                round(g, 1)
                u = request.user.id
                g_mo[movie.id] = [g, u]

        coment_id = -1
        g = 1

        return render(request, "capstone/index.html", {
            "movies": movies,
            "f": f,
            "movieactors": movieactors,
            "actors": actors,
            "gr": gr,
            "g_mo": g_mo,
            "coment_id": coment_id,
            "grades": grades,
            "grade_id": grade_id,
            "g": g,
        })

@csrf_exempt
@login_required
def edit_grade_com(request, movie_id):

    m = Movie.objects.filter(id=movie_id)
    movie = m[0]
    f = 4  # show movie coment
    movieactors = ActorMovie.objects.all()
    actors = Actor.objects.all()

    grade = Grade.objects.filter(user_id=request.user).filter(movie_id=movie_id)[0]
    cg = 1

    movie_coments = Coment.objects.filter(movie_id=movie)


    return render(request, "capstone/index.html", {
        "movie": movie,
        "f": f,
        "movieactors": movieactors,
        "actors": actors,
        "coments": movie_coments,
        "cg": cg,
        "grade": grade
    })



def coment_index(request, movie_id):

    m = Movie.objects.filter(id=movie_id)
    movie = m[0]
    f = 4  # show movie coment
    movieactors = ActorMovie.objects.all()
    actors = Actor.objects.all()

    user = request.user
    grades = Grade.objects.all()
    gr = []
    for grade in grades:
        if (grade.user_id == user and grade.movie_id.id == movie.id):
            a = movie.id
            gr.append(a)
    g_mo = {}

    if movie.numberOfGrades:
        movie_grades = Grade.objects.filter(movie_id=movie)
        sum = 0
        for mg in movie_grades:
            sum = sum + mg.grade
        g = sum / movie.numberOfGrades
        round(g, 1)
        u = request.user.id
        g_mo[movie.id] = [g, u]


    movie_coments = Coment.objects.filter(movie_id=movie)


    return render(request, "capstone/index.html", {
        "movie": movie,
        "f": f,
        "movieactors": movieactors,
        "actors": actors,
        "gr": gr,
        "g_mo": g_mo,
        "coments": movie_coments,
        "grades": grades,
    })

@csrf_exempt
@login_required
def addcoment(request):

    data = json.loads(request.body)
    coment_text = data.get("coment_text", "")
    movie_id = data.get("movie_id", "")

    movie = Movie.objects.get(pk=movie_id)

    g = Coment()
    g.user_id = request.user
    g.movie_id = movie
    g.textComent = coment_text
    g.save()

    movie.numberOfComents = movie.numberOfComents + 1
    movie.save()

    return JsonResponse({"message": "OK"}, status=201)

@login_required
def delete_coment(request, coment_id):

    c = Coment.objects.filter(id=coment_id)
    coment = c[0]
    movie_id = coment.movie_id.id
    coment.delete()

    return HttpResponseRedirect(reverse("coment_index", kwargs={'movie_id':movie_id}))

@csrf_exempt
@login_required
def edit_coment(request, coment_id):

    if request.method == "PUT":

        data = json.loads(request.body)
        coment_text = data.get("coment_text", "")

        c = Coment.objects.filter(id=coment_id)
        coment = c[0]
        coment.textComent = coment_text
        coment.save()

        return JsonResponse({"message": "OK"}, status=201)

    else:

        c = Coment.objects.filter(id=coment_id)
        coment = c[0]
        movie_id = coment.movie_id.id

        m = Movie.objects.filter(id=movie_id)
        movie = m[0]
        f = 4  # show movie coment
        movieactors = ActorMovie.objects.all()
        actors = Actor.objects.all()

        user = request.user
        grades = Grade.objects.all()
        gr = []
        for grade in grades:
            if (grade.user_id == user and grade.movie_id.id == movie.id):
                a = movie.id
                gr.append(a)
        g_mo = {}

        if movie.numberOfGrades:
            movie_grades = Grade.objects.filter(movie_id=movie)
            sum = 0
            for mg in movie_grades:
                sum = sum + mg.grade
            g = sum / movie.numberOfGrades
            round(g, 1)
            g_mo[movie.id] = g

        movie_coments = Coment.objects.filter(movie_id=movie)

        return render(request, "capstone/index.html", {
            "movie": movie,
            "f": f,
            "movieactors": movieactors,
            "actors": actors,
            "gr": gr,
            "g_mo": g_mo,
            "coments": movie_coments,
            "coment_id": coment.id
        })

def best(request):

    movies = Movie.objects.all()
    f = 1   # show all movies
    movieactors = ActorMovie.objects.all()
    actors = Actor.objects.all()

    user = request.user
    grades = Grade.objects.all()
    gr = []
    for grade in grades:
        for movie in movies:
            if ( grade.user_id == user and grade.movie_id.id == movie.id):
                a = movie.id
                gr.append(a)

    g_mo = {}
    am = []
    for movie in movies:
        if movie.numberOfGrades :

            movie_grades = Grade.objects.filter(movie_id=movie)
            sum = 0
            for mg in movie_grades:
                sum = sum + mg.grade
            g = sum / movie.numberOfGrades
            round(g, 1)
            u = request.user.id
            g_mo[movie.id] = [g,u]
            am.append(movie.id)

    coment_id = -1
    g = 0

    k = []
    for a in am:
        c = []
        b = g_mo[a][0]
        c.append(a)
        c.append(b)
        k.append(c)

    k.sort(key=takeSecond, reverse=True)

    m = []
    for kk in k:
        for a in movies:
            if a.id == kk[0]:
                m.append(a)

    return render(request, "capstone/index.html", {
        "movies": m,
        "f": f,
        "movieactors": movieactors,
        "actors" : actors,
        "gr" : gr,
        "g_mo" : g_mo,
        "coment_id": coment_id,
        "grades": grades,
        "g": g,
    } )

def mostpopular(request):

    movies = Movie.objects.all()
    movies = movies.order_by("-numberOfGrades").all()
    f = 1   # show all movies
    movieactors = ActorMovie.objects.all()
    actors = Actor.objects.all()

    user = request.user
    grades = Grade.objects.all()
    gr = []
    for grade in grades:
        for movie in movies:
            if ( grade.user_id == user and grade.movie_id.id == movie.id):
                a = movie.id
                gr.append(a)

    g_mo = {}
    for movie in movies:
        if movie.numberOfGrades :

            movie_grades = Grade.objects.filter(movie_id=movie)
            sum = 0
            for mg in movie_grades:
                sum = sum + mg.grade
            g = sum / movie.numberOfGrades
            round(g, 1)
            u = request.user.id
            g_mo[movie.id] = [g,u]

    coment_id = -1
    g = 0

    return render(request, "capstone/index.html", {
        "movies": movies,
        "f": f,
        "movieactors": movieactors,
        "actors" : actors,
        "gr" : gr,
        "g_mo" : g_mo,
        "coment_id": coment_id,
        "grades": grades,
        "g": g
    } )

def takeSecond(elem):
    return elem[1]




