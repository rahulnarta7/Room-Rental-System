from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<int:id>/', views.room_detail, name='room_detail'),
    path('add-room/', views.add_room, name='add_room'),
    path('edit-room/<int:id>/', views.edit_room, name='edit_room'),
    path('delete-room/<int:id>/', views.delete_room, name='delete_room'),
    path('register/', views.register, name='register'),
    path('my-listings/', views.my_listings, name='my_listings'),
]