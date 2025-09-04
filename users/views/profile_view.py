from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User


from ..models.profile_model import Profile
from ..serializers.profile_serializer import ProfileSerializer
from rest_framework import permissions

class ProfileDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, username, format=None):
        user = get_object_or_404(User, username=username)
        profile = get_object_or_404(Profile, user=user)
        serializer = ProfileSerializer(profile)
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
    
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth.models import User
from ..models.profile_model import Profile
from ..serializers.profile_serializer import ProfileUpdateSerializer, ProfilePictureUpdateSerializer


class ProfileUpdateView(generics.UpdateAPIView):
    
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

    # --- ADICIONE/SOBRESREVA O MÉTODO 'update' ---
    def update(self, request, *args, **kwargs):
        # Primeiro, executa a lógica de atualização padrão para salvar os dados
        super().update(request, *args, **kwargs)
        
        # Em seguida, pega a instância do usuário atualizado
        instance = self.get_object()
        
        # E retorna uma resposta formatada com o ProfileSerializer completo
        profile_data = ProfileSerializer(instance.profile, context={'request': request}).data
        return Response(profile_data)

class ProfilePictureUpdateView(generics.UpdateAPIView):
    serializer_class = ProfilePictureUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    # --- ADICIONE ESTA LINHA ---
    parser_classes = [MultiPartParser, FormParser]
    
    def get_object(self):
        return self.request.user.profile

    def update(self, request, *args, **kwargs):
        print("\n" + "="*50)
        print("DENTRO DA ProfilePictureUpdateView")
        print("Conteúdo de request.data:", request.data)
        print("Conteúdo de request.FILES:", request.FILES)
        print("="*50 + "\n")
        super().update(request, *args, **kwargs)
        
        instance = self.get_object()
        profile_data = ProfileSerializer(instance, context={'request': request}).data
        return Response(profile_data)