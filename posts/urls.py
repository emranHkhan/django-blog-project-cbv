from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.AddPostCreateView.as_view(), name='add_post'),
    path('edit/<int:id>/', views.UpdatePostView.as_view(), name='edit_post'),
    path('details/<int:id>/', views.DetailPostView.as_view(), name='detail_post'),
    path('delete/<int:id>/', views.DeletePostView.as_view(), name='delete_post'),
]
