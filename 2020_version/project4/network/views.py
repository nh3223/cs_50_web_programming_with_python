import json
from django.contrib.auth import authenticate, login, logout, get_user
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post, Follow


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
def compose(request, post_id=None):
    # Get post content
    content = json.loads(request.body).get('content','')
    # Create new post
    if request.method == "POST":
        author = request.user
        post = Post(author=author, content=content)
    # Edit post
    elif request.method == "PUT":
        post = Post.objects.get(pk=post_id)
        post.content = content
    # Return error
    else:
        return JsonResponse({"error": "POST or PUT request required."}, status=400)
    # Save post and return success message
    post.save()
    return JsonResponse({"message": "Posted successfully."}, status=201)

def all_posts(request):
    posts = Post.objects.all()
    return get_posts(posts)

def following_posts(request):
    following_users = [follow.following for follow in Follow.objects.filter(follower=request.user).all()]
    posts = Post.objects.none()
    for user in following_users:
        following_posts = Post.objects.filter(author=user).all()
        posts = posts|Post.objects.filter(author=user).all()
    return get_posts(posts)

def follows(request, user_name):
    current_user = request.user
    user = User.objects.get(username=user_name)
    number_followers = len(Follow.objects.filter(following=user))
    number_following = len(Follow.objects.filter(follower=user))
    following = True if Follow.objects.filter(follower=current_user, following=user) else False
    print(following)
    return JsonResponse({'number_followers': number_followers, 'number_following': number_following, 'following': following})

@csrf_exempt
@login_required
def follow(request, user_name):
    current_user = get_user(request)
    user = User.objects.get(username=user_name)
    
    following = json.loads(request.body).get('following','')
    print(following, current_user, user)
    if following:
        follow_user = Follow(follower=current_user, following=user)
        follow_user.save()
        return JsonResponse({'message': 'User Followed'}, status=201)
    else:
        print('unfollow')
        follow_user = Follow.objects.filter(follower=current_user,following=user)
        follow_user.delete()
        return JsonResponse({'message': 'User Unfollowed'}, status=201)

def profile_posts(request, user_name):
    user = User.objects.get(username=user_name)
    posts = Post.objects.filter(author=user)
    return get_posts(posts)

def get_posts(posts):
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize_post() for post in posts], safe=False)