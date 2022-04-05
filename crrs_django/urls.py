"""crrs_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from upserve import views
from django.views.generic.base import RedirectView

app_name = 'upserve'

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', RedirectView.as_view(url='/index')),
    path('', views.MyIndexView.as_view(), name="my_index_view"),
    path('searchresults', views.MySearchResultsView.as_view(), name="my_searchresults_view"),
    path('home', views.MyIndexLoggedView.as_view(), name="my_indexlogged_view"),
    path('room_info', views.RoomInfo.as_view(), name="room_info"),
    path('home/room_info', views.RoomInfoLogged.as_view(), name="room_info_logged"),
    path('home/searchresults', views.MyIndexLogged_SearchResultsView.as_view(), name="my_indexlogged-searchresults_view"),
    path('home/accountsettings', views.MyIndexLogged_AccountSettings.as_view(), name="my_indexlogged-accountsettings_view"),
    path('home/reservations', views.MyIndexLogged_Reservations.as_view(), name="my_indexlogged-reservations_view"),
    path('login', views.MyLoginView.as_view(), name="my_login_view"),
    path('signup', views.MySignUpView.as_view(), name="my_signup_view"),
    path('dashboard', views.MyAdminDashboardView.as_view(), name="my_admindashboard_view"),
    path('dashboard/users', views.MyUsersView.as_view(), name="my_users_view"),
    path('dashboard/rooms', views.MyRoomsView.as_view(), name="my_rooms_view"), 
    path('dashboard/reservations', views.MyReservationsView.as_view(), name="my_reservations_view"),
    # path('updateUser/<pk>',display.UpdateUser.as_view(),name='updateUser'),
    # path('deleteUser/<pk>',display.DeleteUser.as_view(),name='deleteUser'),
]