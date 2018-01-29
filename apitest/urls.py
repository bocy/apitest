"""apitest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import path
from django.conf.urls import url, include
from rest_framework import routers
# from api.views import CaseViewSet
from api import views

# router = routers.DefaultRouter()
# router.register(r'testcase', CaseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # url('^', include(router.urls)),
    url('caselist/', views.CaseList.as_view()),
    url('testcase/(?P<pk>[0-9]+)/$', views.CaseDetail.as_view()),
    url('testserver/(?P<pk>[0-9]+)/$', views.ServerDetail.as_view()),
    url('serverlist/', views.ServerList.as_view()),
    url('runtest/', views.TestRun.as_view()),
    url('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]
