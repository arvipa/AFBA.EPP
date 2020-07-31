"""cap_ui_tool URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import include, re_path, path
from rest_framework_swagger.views import get_swagger_view
from django.views.generic.base import TemplateView
from django.conf.urls import url

schema_view = get_swagger_view(title='AFBA EPP API')

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^', include('AFBA_EPP.urls')),
    path(r'swagger/', schema_view),
    path('', TemplateView.as_view(template_name="Index.html"), name='index')
 #   url(r'^.*', TemplateView.as_view(template_name="Index.html"), name="Index")
]
