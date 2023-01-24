from django.shortcuts import render
from blog.models import Post  
from rest_framework.decorators import api_view
from rest_framework.response import Response    
from .serializers import PostSerializer
# Create your views here.
@api_view(['GET'])
def api_overview(request):
    api_urls = {
        "List Blogs":"/api/blogs",
        "Blog Detail":"/api/blog/<blog_id>", 
    }
    return Response(api_urls)

@api_view(['GET'])
def list_blog(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def blog_detail(request, id):
    post = Post.objects.get(id=id)
    serializer = PostSerializer(post, many=False)

    return Response(serializer.data)

