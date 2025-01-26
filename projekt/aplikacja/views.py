from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Kategoria, ProfilUzytkownika, CelOszczednosciowy, Transakcja, Budzet, Powiadomienie
from .forms import BudzetForm, CelOszczednosciowyForm, TransakcjaForm, CustomAuthenticationForm, CustomUserCreationForm
from datetime import date
from django.db import models
from django.db.models import Sum
from django import forms
from datetime import date


@login_required
def dashboard(request):
    budzety = Budzet.objects.filter(uzytkownik=request.user)
    for budzet in budzety:
        miesiac = budzet.miesiac
        suma_transakcji = Transakcja.objects.filter(
            uzytkownik=request.user,
            kategoria=budzet.kategoria,
            data__month=miesiac,
            typ='Wydatek'
        ).aggregate(Sum('kwota'))['kwota__sum'] or 0
        budzet.suma_transakcji = suma_transakcji
        budzet.przekroczony = suma_transakcji > budzet.limit

    cele = CelOszczednosciowy.objects.filter(uzytkownik=request.user)
    transakcje = Transakcja.objects.filter(uzytkownik=request.user).order_by('-data')

    typ_filter = request.GET.get('typ')
    if typ_filter:
        transakcje = transakcje.filter(typ=typ_filter)

    query = request.GET.get('q')
    if query:
        transakcje = transakcje.filter(opis__icontains=query)

    return render(request, 'folder_aplikacji/dashboard.html', {
        'budzety': budzety,
        'cele': cele,
        'transakcje': transakcje,
        'typ_filter': typ_filter,
        'query': query,
    })
def dashboard_view(request):
    return render(request, 'folder_aplikacji/dashboard.html')

def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'folder_aplikacji/home.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'folder_aplikacji/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'folder_aplikacji/logowanie.html', {'form': form})
    
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Budzet, CelOszczednosciowy, Transakcja
from .forms import BudzetForm, CelOszczednosciowyForm, TransakcjaForm

@login_required
def cele_list(request):
    cele = CelOszczednosciowy.objects.filter(uzytkownik=request.user)
    return render(request, 'folder_aplikacji/cele_list.html', {'cele': cele})

@login_required
def cel_add(request):
    if request.method == 'POST':
        form = CelOszczednosciowyForm(request.POST)
        if form.is_valid():
            cel = form.save(commit=False)
            cel.uzytkownik = request.user
            if cel.obecna_kwota >= cel.kwota_docelowa:
                cel.data_osiagniecia = date.today()
            cel.save()
            create_notification(request.user, f"Nowy cel oszczędnościowy '{cel.nazwa}' został dodany.")
            return redirect('cele_list')
    else:
        form = CelOszczednosciowyForm()
    return render(request, 'folder_aplikacji/cel_form.html', {'form': form})

@login_required
def cel_edit(request, pk):
    cel = get_object_or_404(CelOszczednosciowy, pk=pk, uzytkownik=request.user)
    if request.method == 'POST':
        form = CelOszczednosciowyForm(request.POST, instance=cel)
        if form.is_valid():
            cel = form.save(commit=False)
            if cel.obecna_kwota >= cel.kwota_docelowa:
                cel.data_osiagniecia = date.today()
            else:
                cel.data_osiagniecia = None
            cel.save()
            return redirect('cele_list')
    else:
        form = CelOszczednosciowyForm(instance=cel)
    return render(request, 'folder_aplikacji/cel_form.html', {'form': form})

@login_required
def cel_delete(request, pk):
    cel = get_object_or_404(CelOszczednosciowy, pk=pk, uzytkownik=request.user)
    if request.method == 'POST':
        cel.delete()
        return redirect('cele_list')
    return render(request, 'folder_aplikacji/cel_confirm_delete.html', {'cel': cel})

@login_required
def transakcja_add(request):
    if request.method == 'POST':
        form = TransakcjaForm(request.POST)
        if form.is_valid():
            transakcja = form.save(commit=False)
            transakcja.uzytkownik = request.user
            transakcja.save()
            check_budget_exceeded(transakcja)
            return redirect('dashboard')
    else:
        form = TransakcjaForm()
    return render(request, 'folder_aplikacji/transakcja_form.html', {'form': form})

@login_required
def budzety_list(request):
    budzety = Budzet.objects.filter(uzytkownik=request.user)
    return render(request, 'folder_aplikacji/budzety_list.html', {'budzety': budzety})

@login_required
def budzet_add(request):
    if request.method == 'POST':
        form = BudzetForm(request.POST)
        if form.is_valid():
            budzet = form.save(commit=False)
            budzet.uzytkownik = request.user
            budzet.save()
            create_notification(request.user, f"Nowy budżet na {budzet.get_miesiac_display()} w kategorii '{budzet.kategoria}' został dodany.")
            return redirect('budzety_list')
    else:
        form = BudzetForm()
    return render(request, 'folder_aplikacji/budzet_form.html', {'form': form})

@login_required
def budzet_edit(request, pk):
    budzet = get_object_or_404(Budzet, pk=pk, uzytkownik=request.user)
    if request.method == 'POST':
        form = BudzetForm(request.POST, instance=budzet)
        if form.is_valid():
            form.save()
            create_notification(request.user, f"Budżet na {budzet.get_miesiac_display()} w kategorii '{budzet.kategoria}' został zaktualizowany.")
            return redirect('budzety_list')
    else:
        form = BudzetForm(instance=budzet)
    return render(request, 'folder_aplikacji/budzet_form.html', {'form': form})

@login_required
def budzet_delete(request, pk):
    budzet = get_object_or_404(Budzet, pk=pk, uzytkownik=request.user)
    if request.method == 'POST':
        budzet.delete()
        create_notification(request.user, f"Nowy budżet na {budzet.get_miesiac_display()} w kategorii '{budzet.kategoria}' został dodany.")
        return redirect('budzety_list')
    return render(request, 'folder_aplikacji/budzet_confirm_delete.html', {'budzet': budzet})

def check_budget_exceeded(transakcja):
    miesiac = transakcja.data.strftime('%m')
    budzet = Budzet.objects.filter(
        uzytkownik=transakcja.uzytkownik,
        kategoria=transakcja.kategoria,
        miesiac=miesiac
    ).first()
    
    if budzet:
        suma_transakcji = Transakcja.objects.filter(
            uzytkownik=transakcja.uzytkownik,
            kategoria=transakcja.kategoria,
            data__month=miesiac,
            typ='Wydatek',
        ).aggregate(models.Sum('kwota'))['kwota__sum'] or 0
        
        if suma_transakcji > budzet.limit:
            create_notification(transakcja.uzytkownik, f"Budżet na {budzet.get_miesiac_display()} w kategorii '{budzet.kategoria}' został przekroczony.")

def create_notification(user, tresc):
    Powiadomienie.objects.create(uzytkownik=user, tresc=tresc)

@login_required
def powiadomienia_list(request):
    powiadomienia = Powiadomienie.objects.filter(uzytkownik=request.user).order_by('-data_utworzenia')
    return render(request, 'folder_aplikacji/powiadomienia_list.html', {'powiadomienia': powiadomienia})

@login_required
def oznacz_powiadomienie_przeczytane(request, pk):
    powiadomienie = get_object_or_404(Powiadomienie, pk=pk, uzytkownik=request.user)
    powiadomienie.przeczytane = True
    powiadomienie.save()
    return redirect('powiadomienia_list')

@login_required
def powiadomienie_usun(request, pk):
    powiadomienie = get_object_or_404(Powiadomienie, pk=pk, uzytkownik=request.user)
    if request.method == 'POST':
        powiadomienie.delete()
        return redirect('powiadomienia_list')
    return render(request, 'folder_aplikacji/powiadomienie_confirm_delete.html', {'powiadomienie': powiadomienie})

def check_goal_achieved(cel):
    if cel.data_osiagniecia <= date.today() and cel.obecna_kwota >= cel.kwota_docelowa:
        create_notification(cel.uzytkownik, f"Cel oszczędnościowy '{cel.nazwa}' został osiągnięty.")

from rest_framework import generics
from .models import Kategoria, ProfilUzytkownika, CelOszczednosciowy, Transakcja, Budzet
from .serializers import KategoriaSerializer, ProfilUzytkownikaSerializer, CelOszczednosciowySerializer, TransakcjaSerializer, BudzetSerializer

class KategoriaListCreate(generics.ListCreateAPIView):
    queryset = Kategoria.objects.all()
    serializer_class = KategoriaSerializer

class ProfilUzytkownikaListCreate(generics.ListCreateAPIView):
    queryset = ProfilUzytkownika.objects.all()
    serializer_class = ProfilUzytkownikaSerializer

class CelOszczednosciowyListCreate(generics.ListCreateAPIView):
    queryset = CelOszczednosciowy.objects.all()
    serializer_class = CelOszczednosciowySerializer

class TransakcjaListCreate(generics.ListCreateAPIView):
    queryset = Transakcja.objects.all()
    serializer_class = TransakcjaSerializer

class BudzetListCreate(generics.ListCreateAPIView):
    queryset = Budzet.objects.all()
    serializer_class = BudzetSerializer