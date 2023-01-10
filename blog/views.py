from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from .forms import PostCreationForm
from .models import Post, Comment
from django.views import View
from django.db.models import Q 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed 
# Create your views here.
def index(request):
    posts = Post.objects.all().order_by("-created")
    return render(request, "blog/index.html", {"posts":posts})

@login_required(login_url="authapp:index")
def create_post(request: HttpRequest):
    form = PostCreationForm()
    if request.method == "POST":
        form = PostCreationForm(request.POST, request.FILES)
        if(form.is_valid()):
            post:Post = form.save(commit=False)
            post.user = request.user 
            post.save()
            return redirect("blog:index")
    return render(request, "blog/newpost.html", {"form":form}) 

@login_required(login_url="authapp:index")
def delete_post(request, post_id):
    posts = Post.objects.all()
    post = Post.objects.get(pk=post_id)
    post.delete()
    return redirect("blog:index")

@login_required(login_url="authapp:index")
def update_post(request:HttpRequest, post_id:int):
    post = Post.objects.get(pk=post_id)
    
    form = PostCreationForm(instance=post)
    if request.method == "POST":
        form = PostCreationForm(request.POST, request.FILES, instance=post)
        if(form.is_valid()):
            post = form.save(commit=False)
            post.user = request.user 
            post.save()
            return redirect("blog:index")
    return render(request, "blog/updatepost.html", {"post_id":post_id, "form":form}) 

class SearchPost(View):
    def get(self, request):
        data = request.GET.get('q', '')
        posts = Post.objects.filter(Q(title__icontains=data)|Q(content__icontains=data)).order_by("-created")
        
        return render(request, "blog/index.html", {"posts":posts})

def detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    user_has_commented = Comment.objects.filter(user=request.user, post=post).exists() if request.user.is_authenticated else True 
    user_has_liked = post.liked_by.filter(id=request.user.id).exists() if request.user.is_authenticated else True
    user_has_disliked = post.disliked_by.filter(id=request.user.id).exists() if request.user.is_authenticated else True
    return render(request, "blog/detail.html", {"post":post, "user_has_commented":user_has_commented, "user_has_liked":user_has_liked, "user_has_disliked":user_has_disliked})

@login_required(login_url="authapp:index")
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    comment =Comment.objects.create(user=request.user, post=post, content=request.POST.get('comment', ''))
    comment.save()
    return redirect("blog:detail", post_id)

@login_required(login_url="authapp:index")
def like_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if(post.liked_by.filter(id=request.user.id).exists()):
        return HttpResponse("What the hell?")
    else:
        post.liked_by.add(request.user)
        return redirect("blog:detail", post_id)

@login_required(login_url="authapp:index")
def dislike_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    if(post.disliked_by.filter(id=request.user.id).exists()):
        return HttpResponse("Why the hell?")
    else:
        post.disliked_by.add(request.user)
        return redirect("blog:detail", post_id)

class LatestPostsFeed(Feed):
    title = 'Latest Blog Posts'
    link = '/blog/'
    description = 'This is the latest feed of posts'

    def items(self):
        return Post.objects.order_by("-created")[:5]
    
    def item_title(self, item):
        return item.title 
    
    def item_description(self, item):
        return item.content 
    
    def item_link(self, item):
        return '/blog/post/{}'.format(item.id)