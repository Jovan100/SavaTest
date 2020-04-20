from django.urls import path
from .views import *

urlpatterns = [
    path('', Login.as_view(), name='register'),
    path('register/', Registration.as_view(), name='register'),
    path('dashboard/', Users.as_view(), name='users_list'),
    path('forgot-password/', ForgotPassword.as_view(), name="forgot-password"),
    path('forgot-password/<str:token>', ChangePassword.as_view(), name="forgot-password"),
    path('forgot-password/email-sent/', EmailSent.as_view(), name='email-sent'),
]
