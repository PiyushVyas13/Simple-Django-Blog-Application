from django.urls import path 
from . import views 
app_name = "blog"

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create_post, name="create"),
    path('update/<int:post_id>', views.update_post, name="update"),
    path('delete/<int:post_id>', views.delete_post, name="delete"),
    path('search/', views.SearchPost.as_view(), name="search"),
    path('post/<int:post_id>', views.detail, name="detail"),
    path('comment/<int:post_id>', views.add_comment, name="comment"),
    path('like/<int:post_id>', views.like_post, name="like"),
    path('rss/feed', views.LatestPostsFeed(), name="latest_rss"),
    path('dislike/<int:post_id>', views.dislike_post, name="dislike"),
    path('<int:user_id>/profile', views.user_profile, name="profile"),

]