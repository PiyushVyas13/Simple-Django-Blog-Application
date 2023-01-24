from django.urls import path 
from . import views 

app_name = "api"

urlpatterns = [
    path('', views.api_overview, name="overview"),
    path('blogs/', views.list_blog, name="blogs-list"),
    path('blogs/<int:id>', views.blog_detail, name="blog-detail"),
]