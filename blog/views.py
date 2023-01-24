from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpRequest
from .forms import PostCreationForm
from .models import Post, Comment, Tag
from django.views import View
from django.db.models import Q 
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.contrib.syndication.views import Feed 
from rest_framework.decorators import api_view
from rest_framework.response import Response 

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
            tags = form.cleaned_data['tags']
            tag_list = tags.split(' ')
            for tag in tag_list:
                print(tag)
                tag = tag.strip()
                tag_obj, created = Tag.objects.get_or_create(name=tag)
                if created:
                    tag_obj.save()
                post.tags.add(tag_obj)
            
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
        tag = get_object_or_404(Tag, name=data)
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

@login_required(login_url="authapp:index")
def user_profile(request, user_id):
    user = User.objects.get(id=user_id)
    # avatar = get_thumbnailer(user.profile.profile_thumbnail).get_thumbnail({'size': (50, 50), 'crop': True})
    posts = Post.objects.filter(user=user)
    user_joined = user.date_joined.strftime('%B %Y')
    return render(request, "blog/profile.html",{'user':user, 'posts':posts, 'date_joined':user_joined})

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

