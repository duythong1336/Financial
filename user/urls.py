from django.urls import path
from user import views
urlpatterns = [
    path('user/register/', views.CreateUserView.as_view(), name = 'register-user'),
    path('user/verify/', views.VerifyEmailView.as_view(), name = 'verify-email'),
    path('user/check-email/',views.CheckEmailForgotPassword.as_view(), name = 'check-email-forgot-password'),
    path('user/verify-code/',views.VerifyCodeForRetrivePasswordView.as_view(), name = 'verify-code-forretrive-password'),
    path('user/recover-password/',views.RecoverPassword.as_view(), name = 'recover-password'),
    path('test/', views.Test.as_view(), name = 'test'),
]