from rest_framework import routers
from users.api.views import  UserViewSet, PasswordResetViewSet

router = routers.DefaultRouter()
router.register('users', UserViewSet, basename='users')
router.register('password-reset', PasswordResetViewSet, basename='password-reset')
