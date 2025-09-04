# seu_app_de_auth/views.py

from rest_framework import generics, permissions
from ..serializers import ProfileSerializer
from ..models.profile_model import Profile 

# ... (suas outras views: LoginView, RegisterView, etc.) ...

class MyProfileView(generics.RetrieveAPIView):
    """
    View que retorna o perfil do usuário atualmente autenticado.
    """
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Simplesmente retorna o perfil associado ao usuário da requisição.
        return self.request.user.profile