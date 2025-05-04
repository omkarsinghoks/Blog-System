from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    # author = models.CharField(max_length=50)
    author = models.ForeignKey(User, on_delete=models.CASCADE) 
    added_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)
    # author = models.ForeignKey(User, on_delete=models.CASCADE)

    published_at = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    # age=models.IntegerField(default=0)
    def __str__(self):
        return self.title

# c