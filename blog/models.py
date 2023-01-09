from django.db import models
from django.contrib.auth.models import User 
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    liked_by = models.ManyToManyField(User, related_name="liked_posts", blank=True)
    # temp = models.CharField(max_length=50, null=True, blank=True)
    image = models.ImageField(blank=True)
    # comments = 
    created = models.DateTimeField(auto_now=True)
    updated = models.DateTimeField(auto_now=True)

    

    def __str__(self):
        return self.title

class Comment(models.Model):
    content = models.CharField(max_length=200)
    
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'post'], name="unique_comment_per_blog")
        ]

    def __str__(self):
        return self.content 


