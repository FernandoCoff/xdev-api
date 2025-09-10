from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    RegisterView,
    LoginView,
    ProfileDetailView,
    ProfileFollowView,
    ProfileUpdateView,
    ProfilePictureUpdateView,
    MyProfileView,
    ProfileViewSet 
)


router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile-search')


urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', LoginView.as_view(), name='auth_login'),
    path('profile/me/', MyProfileView.as_view(), name='my_profile'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/<str:username>/follow/', ProfileFollowView.as_view(), name='profile_follow'),
    path('profile/me/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/me/update-picture/', ProfilePictureUpdateView.as_view(), name='profile_update_picture'),
    path('', include(router.urls)),
]