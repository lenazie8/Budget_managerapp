from django import forms
from .models import CelOszczednosciowy, Transakcja, Budzet
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from datetime import date

class CelOszczednosciowyForm(forms.ModelForm):
    class Meta:
        model = CelOszczednosciowy
        fields = ['nazwa', 'kwota_docelowa', 'obecna_kwota']

class TransakcjaForm(forms.ModelForm):
    class Meta:
        model = Transakcja
        fields = ['typ', 'kwota', 'data', 'opis', 'kategoria']

class BudzetForm(forms.ModelForm):
    class Meta:
        model = Budzet
        fields = ['kategoria', 'miesiac', 'limit']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Nazwa użytkownika",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Nazwa użytkownika",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password1 = forms.CharField(
        label="Hasło",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password2 = forms.CharField(
        label="Potwierdź hasło",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")