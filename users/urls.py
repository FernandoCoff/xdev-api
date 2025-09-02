from django.urls import path
from .views import RegisterView
from .views import LoginView
from .views import ProfileDetailView
from .views import ProfileFollowView
from .views import ProfileUpdateView
from .views import ProfilePictureUpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<str:username>/follow/', ProfileFollowView.as_view(), name='profile_follow'),
    path('profile/me/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/me/update-picture/', ProfilePictureUpdateView.as_view(), name='profile_update_picture'),
]