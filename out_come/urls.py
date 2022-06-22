from django.urls import path
from out_come import views
urlpatterns = [
    path('user/outcomes/', views.CreateAndListOutComeView.as_view(), name = 'user-outcomes'),
    path('user/outcomes/<int:pk>/', views.GetDetailUpdateOutComeView.as_view(), name='detail-update-outcome'),
    path('user/outcomes/enable/', views.GetlistOutcomeEnableAddtoJar.as_view(), name = 'enable-outcome'),
    path('user/outcomes/updateJar/', views.UpdateJarForOutComeView.as_view(), name = 'update-jar-for-outcome'),
]