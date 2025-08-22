from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (
    UserViewSet,
    LeagueViewSet,
    PlayerProfileViewSet,
    RegisterView,
    CustomTokenObtainPairView,
    ChangePasswordView,
    LogoutView,
    MeView,
)


router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'leagues', LeagueViewSet, basename='league')
router.register(r'players', PlayerProfileViewSet, basename='player')

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("me/", MeView.as_view(), name="me"),

    
    path("", include(router.urls)),
]