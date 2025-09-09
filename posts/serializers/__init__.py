from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Post, Comment

User = get_user_model()

class AuthorSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(source='profile.profile_picture', read_only=True, required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'avatar']

class CommentSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    created_since = serializers.CharField(source='get_display_time', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'created_since']
        read_only_fields = ['author', 'post']


class PostSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    like_count = serializers.IntegerField(read_only=True)
    comment_count = serializers.IntegerField(read_only=True)
    created_since = serializers.CharField(source='get_display_time', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 
            'author', 
            'content', 
            'created_at',
            'created_since',
            'likes',
            'like_count', 
            'comments',
            'comment_count'
        ]
        
        read_only_fields = ['author', 'likes', 'comments']
