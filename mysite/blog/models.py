from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')  # Add author field
    liked_users = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    disliked_users = models.ManyToManyField(User, related_name='disliked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for post creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for the last update

    def likes_count(self):
        return self.liked_users.count()

    def dislikes_count(self):
        return self.disliked_users.count()

    def __str__(self):
        return self.title



class LikeDislike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)  # Ensure this is referencing Post
    is_like = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'post')  # Prevent a user from liking/disliking multiple times