"""first URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from app01 import views
from django.conf import settings
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login$', views.login),
    url(r'^login_aj', views.login_ajax),
    url(r'^date/', views.date),
    url(r'^index/', views.index),
    url(r'^ajax/', views.ajax),
    url(r'^ajax_register/', views.ajax_register),
    url(r'^jqurey_ajax/', views.jqurey_ajax),
    url(r'^jqurey_get/', views.jqurey_get),
    url(r"one_to_one",views.one_to_one),
    url(r"modelform$",views.Modelform),
    url(r"edit-obj-(\d+)",views.editmodelform),
    url(r"test_signal",views.test_signal),
    url(r"cache",views.cache_test),
    url(r"video-(?P<lv_id>\d+)-(?P<cg_id>\d+)$",views.video,name="video"),
    url(r"video-(?P<dr_id>\d+)-(?P<cg_id>\d+)-(?P<lv_id>\d+)",views.video2,name="video2"),
    url(r"^editor$",views.editor)


]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        # For django versions before 2.0:
        url(r'^__debug__/', include(debug_toolbar.urls)),

    ] + urlpatterns