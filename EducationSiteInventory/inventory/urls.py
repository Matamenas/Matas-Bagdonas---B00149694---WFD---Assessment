from django.urls import path
from . import views

urlpatterns = [
    path('', views.teacher_dashboard, name='teacher_dashboard'),
    path('request-item/', views.request_item, name='request_item'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('register/', views.register, name='register'),
]

