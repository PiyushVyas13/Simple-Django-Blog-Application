from django.db import models
from django.contrib.auth.models import User 
from easy_thumbnails.fields import ThumbnailerImageField
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
   # profile_picture = models.ImageField(upload_to="profile-pics/", blank=True)
    bio = models.TextField(blank=True)
    profile_thumbnail = ThumbnailerImageField(upload_to="profile-pics/", blank=True)

   
    def __str__(self):
        return self.user.username 
