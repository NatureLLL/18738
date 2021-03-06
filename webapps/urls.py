"""webapps URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
import django.contrib.auth.views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
import grumblr.views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('grumblr/', include('grumblr.urls')),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',grumblr.views.activate, name='activate'),
    path('', django.contrib.auth.views.LoginView.as_view()),
    url(r'^reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        grumblr.views.reset_password, name='reset_password'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
