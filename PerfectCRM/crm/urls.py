
from django.conf.urls import url
from crm import views
from django.contrib import admin
urlpatterns = [
    url(r'^$',views.index,name="sales_index"),
    url(r'^customers$',views.customer_list,name="customer_index"),
    url(r'^customer/(\d+)/enrollment/$',views.enrollment,name="customer_enrollment"),
    url(r'^payment/(\d+)/', views.payment,name="payment"),
    url(r'^customer/registration/(\d+)/(\w+)/$',views.registre,name="customer_registre"),
    url(r'^contract_review/(\d+)/$',views.contact_review,name="contact_review"),
    url(r'^enrollment_rejection/(\d+)/$',views.enrollment_rejection,name="enrollment_rejection"),


]
