from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from aplikacja import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/kategorie/', views.KategoriaListCreate.as_view(), name='kategoria-list-create'),
    path('api/profiluzytkownika/', views.ProfilUzytkownikaListCreate.as_view(), name='profiluzytkownika-list-create'),
    path('api/celeoszczednosciowe/', views.CelOszczednosciowyListCreate.as_view(), name='celeoszczednosciowe-list-create'),
    path('api/transakcje/', views.TransakcjaListCreate.as_view(), name='transakcja-list-create'),
    path('api/budzety/', views.BudzetListCreate.as_view(), name='budzet-list-create'),
    path('api-auth/', include('rest_framework.urls')),
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('cele/', views.cele_list, name='cele_list'),
    path('cele/add/', views.cel_add, name='cel_add'),
    path('cele/edit/<int:pk>/', views.cel_edit, name='cel_edit'),
    path('cele/delete/<int:pk>/', views.cel_delete, name='cel_delete'),
    path('transakcje/add/', views.transakcja_add, name='transakcja_add'),
    path('budzety/', views.budzety_list, name='budzety_list'),
    path('budzety/add/', views.budzet_add, name='budzet_add'),
    path('budzety/edit/<int:pk>/', views.budzet_edit, name='budzet_edit'),
    path('budzety/delete/<int:pk>/', views.budzet_delete, name='budzet_delete'),
    path('powiadomienia/', views.powiadomienia_list, name='powiadomienia_list'),
    path('powiadomienia/oznacz/<int:pk>/', views.oznacz_powiadomienie_przeczytane, name='oznacz_powiadomienie_przeczytane'),
    path('powiadomienia/usun/<int:pk>/', views.powiadomienie_usun, name='powiadomienie_usun'),
]