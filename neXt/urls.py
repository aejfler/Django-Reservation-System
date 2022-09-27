"""neXt_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import reservations.views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', reservations.views.start, name="home"),
    path('room/new/', reservations.views.add_room, name="add_room"),
    path('rooms/', reservations.views.list_of_rooms, name="rooms"),
    path('room/delete/<int:room_id>/', reservations.views.delete_room, name="delete_room"),
    path('room/modify/<int:room_id>/', reservations.views.modify_room, name="modify_room"),
    # path('room/reserve/<int:room_id>/', reservations.views.reservation, name="reserve_room"),
    path('room/<int:room_id>/', reservations.views.detail_view, name="room_detail"),
    path('room/reservation/<int:pk>/', reservations.views.reservation, name="reservation"),
    path('reservation/cancel/<int:pk>/', reservations.views.cancel_reservation, name="cancel_reservation"),
    path('room/available/', reservations.views.availability, name="available"),
    path('reservations/', reservations.views.all_reservations, name="reservations"),

]
