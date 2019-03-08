
from django.conf.urls import url
from student import views

urlpatterns = [

    url(r'^$',views.my_class,name="my_class"),
    url(r'^homework_detail/(\d+)/$',views.homework_detail,name="homework_detail"),
    url(r'^studyrecords/(\d+)/$',views.studyrecords,name="studyrecords"),


]
