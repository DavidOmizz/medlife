from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('department', views.department, name='department'),
    path('doctors', views.doctors, name='doctors'),
    path('contact', views.contact, name='contact'),
    path('department/<slug:slug>', views.single_department, name='single_department'),
]
