from django.urls import path
from wallet import views
urlpatterns = [
    path('user/wallet/', views.CreateGetWalletFollowUserView.as_view(), name = 'get-create-wallet'),
    path('user/wallet/<int:pk>/', views.GetDetailUpdateWalletView.as_view(), name = 'get-detail-update-wallet'),
    path('user/wallet/<int:pk>/incomes/', views.AddIncomeToWallet.as_view(), name = 'add-income-to-wallet')
]