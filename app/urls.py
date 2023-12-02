from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('department', views.department, name='department'),
    path('department/<slug:slug>/', views.single_department, name='single_department'),
    path('doctors', views.doctors, name='doctors'),
    path('contact', views.contact, name='contact'),
    path('post', views.post, name='post'),
    path('single/<slug:slug>/', views.single_post, name='single_post'),
    path('post/<slug:slug>', views.single_blog, name =  'single_blog'),
]

