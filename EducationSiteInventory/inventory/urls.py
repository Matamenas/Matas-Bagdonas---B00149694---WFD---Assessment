from django.urls import path
from . import views

urlpatterns = [

    # teacher side of things
    path('', views.teacher_dashboard, name='teacher_dashboard'),
    path('request-item/', views.request_item, name='request_item'),
    path('my-requests/', views.my_requests, name='my_requests'),
    path('register/', views.register, name='register'),
    # admin side of things
    path('inventory/', views.item_list, name='item_list'),
    path('inventory/add/', views.add_item, name='add_item'),
    path('inventory/edit/<int:pk>/', views.edit_item, name='edit_item'),
    path('inventory/delete/<int:pk>/', views.delete_item, name='delete_item'),
    path('requests/', views.view_requests, name='view_requests'),
    path('requests/<int:request_id>/approve/', views.approve_requests, name='approve_request'),
    path('requests/<int:request_id>/reject/', views.reject_requests, name='reject_request'),


]

