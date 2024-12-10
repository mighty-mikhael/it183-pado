from rest_framework import serializers
from .models import Post, LikeDislike

class PostSerializer(serializers.ModelSerializer):
    likes_count = serializers.SerializerMethodField()
    dislikes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'image', 'author', 'likes_count', 'dislikes_count', 'created_at', 'updated_at']

    def get_likes_count(self, obj):
        return obj.likes_count()

    def get_dislikes_count(self, obj):
        return obj.dislikes_count()

class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = ['id', 'user', 'post', 'is_like']
