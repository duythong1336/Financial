from django.urls import path
from in_come import views
urlpatterns = [
    path('user/incomes/', views.CreateAndListIncomeView.as_view(), name = 'user-imcomes'),
    path('user/incomes/<int:pk>/', views.GetDetailUpdateIncomeView.as_view(), name='detail-update-income'),
    path('user/incomes/enable/',views.GetlistIncomeEnableAddtoWallet.as_view(), name = 'list-incomes-enable'),
    path('user/incomes/wallet/',views.CreateIncomeAndAddToWallet.as_view(), name = 'Add-Income-To-Wallet')
]