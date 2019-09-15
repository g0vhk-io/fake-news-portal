"""portal URL Configuration

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
from django.conf.urls import url, include
from django.contrib import admin
from django.urls import path
from .home.views import *
from django.contrib.auth import views as auth_views
from portal import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', index_view),
    path('report/<int:report_id>/', detail_view, name='detail'),
    path('report/update_comment', update_comment, name='update_comment'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^auth/', include('social_django.urls', namespace='social')),
    url(r'^markdownx/markdownify/$', proxy_markdownify_view),
    url(r'^markdownx/upload/$', proxy_markdown_upload_view)
]
