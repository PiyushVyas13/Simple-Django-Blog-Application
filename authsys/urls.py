from django.urls import path 
from . import views 

app_name = "authapp"

urlpatterns = [
    path('', views.index, name="index"),
    path('register/', views.register_user, name="register"),
    path('logout/', views.logout_user, name="logout"),
]
