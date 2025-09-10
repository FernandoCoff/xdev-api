from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from ..models import Post, Comment
from ..serializers import PostSerializer, CommentSerializer
from rest_framework import viewsets, status, serializers

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like_toggle(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True
        
        like_count = post.like_count
        return Response({'status': 'ok', 'liked': liked, 'like_count': like_count})

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated], url_path='feed')
    def feed(self, request):

        user = request.user
    
        followed_profiles = user.profile.follows.all()
        
        followed_user_ids = [profile.user.id for profile in followed_profiles]
        
    
        followed_user_ids.append(user.id)
        
        queryset = Post.objects.filter(author_id__in=followed_user_ids)
        
        queryset = queryset.order_by('-created_at')
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
            
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        if 'post_pk' in self.kwargs:
            return Comment.objects.filter(post_id=self.kwargs['post_pk'])
        return Comment.objects.none() 

    def perform_create(self, serializer):
        try:
            post = Post.objects.get(pk=self.kwargs['post_pk'])
            serializer.save(author=self.request.user, post=post)
        except Post.DoesNotExist:
            raise serializers.ValidationError("O post especificado não existe.")