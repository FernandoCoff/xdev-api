from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, viewsets, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from ..models import Profile
from ..serializers import ProfileSerializer, ProfileUpdateSerializer, ProfilePictureUpdateSerializer


class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class ProfileFollowView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, username, format=None):
        user_to_toggle_follow = get_object_or_404(User, username=username)
        profile_to_toggle_follow = user_to_toggle_follow.profile
        current_user_profile = request.user.profile

        if current_user_profile == profile_to_toggle_follow:
            return Response({"error": "Você não pode seguir a si mesmo."}, status=status.HTTP_400_BAD_REQUEST)

        if current_user_profile.follows.filter(pk=profile_to_toggle_follow.pk).exists():
            current_user_profile.follows.remove(profile_to_toggle_follow)
            action = "unfollowed"
        else:
            current_user_profile.follows.add(profile_to_toggle_follow)
            action = "followed"
            
        return Response({"status": action}, status=status.HTTP_200_OK)
    
class ProfileUpdateView(generics.UpdateAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        instance = self.get_object()
        profile_data = ProfileSerializer(instance.profile, context={'request': request}).data
        return Response(profile_data)

class ProfilePictureUpdateView(generics.UpdateAPIView):
    serializer_class = ProfilePictureUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        instance = self.get_object()
        profile_data = ProfileSerializer(instance, context={'request': request}).data
        return Response(profile_data)

class ProfileViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    filter_backends = [SearchFilter]
    search_fields = ['user__username']

    def get_queryset(self):
        return Profile.objects.all().exclude(user=self.request.user)


