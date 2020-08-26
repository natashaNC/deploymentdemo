from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from django.db.models import Q
from .models import User, Post

# Create your views here.
def index(request):
    return render(request, "index.html")

def register(request):
    print(request.POST)
    validationErrors= User.objects.regValidator(request.POST)
    if len(validationErrors)>0:
        for value in validationErrors.values():
            messages.error(request, value)
        return redirect("/")
    else:
        #encrypt the password thennnnnn create the user
        # hash1 = bcrypt.hashpw('test'.encode(), bcrypt.gensalt()).decode()
        securedthebag= bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
        newUser = User.objects.create(firstName = request.POST['fname'], email = request.POST['email'], password = securedthebag)
        request.session['loggedInId'] = newUser.id
        return redirect("/home")


def login(request):
    print(request.POST)
    #send the request.POST TO THE VALIDATOR
    validationErrors= User.objects.loginValidator(request.POST)
    if len(validationErrors)>0:
        for value in validationErrors.values():
            messages.error(request, value)
        return redirect("/")
    else:
        print(validationErrors)
        usersWithemail = User.objects.filter(email= request.POST['email'])
        request.session['loggedInId']= usersWithemail[0].id
        return redirect("/home")

def home(request):
    if 'loggedInId' not in request.session:
        messages.error(request, "You must log in first. Who dis.")
        return redirect("/")
    context = {
        'loggedinuser' : User.objects.get(id=request.session['loggedInId']),
        'allposts': Post.objects.all(),
        'likedPosts': Post.objects.filter(Q(likes= User.objects.get(id=request.session['loggedInId'])) | Q(uploader=User.objects.get(id=request.session['loggedInId']))),
        'notlikedPosts': Post.objects.exclude(Q(likes= User.objects.get(id=request.session['loggedInId'])) | Q(uploader=User.objects.get(id=request.session['loggedInId'])))
    }
    # User.objects.filter(Q(income__gte=5000) | Q(income__isnull=True))
    return render(request, "home.html", context )


def addpost(request):
    return render(request, "addpost.html" )


def createRant(request):
    print(request.POST)
    validationErrors= Post.objects.postValidator(request.POST)
    if len(validationErrors)>0:
        for value in validationErrors.values():
            messages.error(request, value)
        return redirect("/addPost")
    newpost = Post.objects.create(content = request.POST['rant'], uploader= User.objects.get(id=request.session['loggedInId']))
    return redirect("/home")


def likeRant(request,rantId):
    #make the many to many join
    print(rantId)
    liker = User.objects.get(id=request.session['loggedInId'])
    rant = Post.objects.get(id=rantId)

    # liker.posts_liked.add(rant)
    rant.likes.add(liker)

    #redirect
    return redirect("/home")

def unlikeRant(request,rantId):
    #make the many to many join
    print(rantId)
    liker = User.objects.get(id=request.session['loggedInId'])
    rant = Post.objects.get(id=rantId)

    # liker.posts_liked.add(rant)
    rant.likes.remove(liker)

    #redirect
    return redirect("/home")

def showRant(request, rantId):

    context = {
        'rantObj': Post.objects.get(id=rantId)
    }
    return render(request, "showrant.html", context)
def logout(request):
    request.session.clear()
    return redirect("/")