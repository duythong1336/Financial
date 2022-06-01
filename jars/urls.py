from django.urls import path
from jars import views
urlpatterns = [
    path('user/jars/', views.GetJarsFollowUserView.as_view(), name = 'user-jars'),
    path('user/jars/<int:pk>/', views.GetUpdateJarsView.as_view(), name = 'get-detail-jars'),
    path('user/jars/<int:pk>/outcome/', views.AddOutcomeToJar.as_view(),name = 'add-incomes-to-jar'),
]