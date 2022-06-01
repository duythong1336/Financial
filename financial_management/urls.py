"""financial_management URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from auth_jwt.views import CustomTokenObtainView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(
        [
            path('', include('user.urls')),
            # path('', include('income.urls')),
            # path('', include('jars.urls'))
            path('', include('wallet.urls')),
            path('', include('jars.urls')),
            path('', include('in_come.urls')),
            path('', include('out_come.urls')),
            path('login/', CustomTokenObtainView.as_view(), name='token_obtain_pair'),
        ]
    ))
]
