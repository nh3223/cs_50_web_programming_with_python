import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


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
def compose(request, post=None):

    print('Start compose view')
    print(request.method)
    # Adding a post must be via POST or PUT
    if request.method != "POST" and request.method != "PUT":
        print('Not post or put')
        return JsonResponse({"error": "POST or PUT request required."}, status=400)
    
    # Create post
    author = request.user
    print(author)
    content = json.loads(request.body).get('content','')
    print(content)
    if request.method == 'POST':
        post = Post(author=author, content=content)
        print(post.author,post.content)
    else:
        post.content = content
    post.save()

    return JsonResponse({"message": "Posted successfully."}, status=201)

def posts(request, post_view):
    
    # Filter emails returned based on mailbox
    if post_view == "all_posts":
        posts = Post.objects.all()
    
    elif post_view == "following":
        pass
        #emails = Email.objects.filter(
        #    user=request.user, sender=request.user
        #)
    elif post_view == "profile":
        pass
        #emails = Email.objects.filter(
        #    user=request.user, recipients=request.user, archived=True
        #)
    else:
        return JsonResponse({"error": "Invalid Post View"}, status=400)

    # Return emails in reverse chronologial order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize_post() for post in posts], safe=False)