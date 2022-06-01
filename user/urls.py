from django.urls import path
from user import views
urlpatterns = [
    path('user/register/', views.CreateUserView.as_view(), name = 'register-user'),
    path('user/verify/', views.VerifyEmailView.as_view(), name = 'verify-email'),
    path('test/', views.Test.as_view(), name = 'test'),
]