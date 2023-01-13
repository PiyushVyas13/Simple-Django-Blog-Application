from django.db import models
from django.contrib.auth.models import User 
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile-pics/", blank=True)

    profile_thumbnail = ImageSpecField(source='profile_picture', processors=[ResizeToFill(100,50)], format='JPEG', options={'quality':60})

    def __str__(self):
        return self.user.username 
