from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('register', views.register),
    path('login', views.login),

    path('shows', views.shows),
    path('shows/new', views.create_show),
    path('shows/<int:show_id>', views.view_show),#for details of show
    path('shows/edit/<int:show_id>', views.edit_show),
    path('shows/delete/<int:show_id>', views.delete_show),
    path('logout', views.logout),

    
]
