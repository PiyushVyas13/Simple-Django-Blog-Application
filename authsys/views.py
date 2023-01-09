from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpRequest
from .forms import UserForm, CombinedForm
from django.contrib.auth.models import User 

# Create your views here.
def index(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        print(user.profile.profile_picture.url)
        if user is not None:
            login(request, user)
            return redirect("blog:index")
        else:
            return HttpResponse("Get the hell outta here!")
    return render(request, "authsys/index.html", {})

def register_user(request):
    form = CombinedForm()
    if request.method == "POST":
        form = CombinedForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user:User = form.save(commit=False)
            user.profile.profile_picture = request.FILES['profile-pic']
            user.save()
            return redirect("authapp:index")
            
        else:
            print("form is not valid")
    
    return render(request, "authsys/register.html", {"form":form})

def logout_user(request: HttpRequest):
    if(request.user.is_authenticated):
        logout(request) 
        return redirect("blog:index")
    else:
        return HttpResponse("You are not logged in")
    

