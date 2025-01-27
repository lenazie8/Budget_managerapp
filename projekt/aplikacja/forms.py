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
    
    def clean_kwota_docelowa(self):
        kwota_docelowa = self.cleaned_data.get('kwota_docelowa')
        if kwota_docelowa <= 0:
            raise forms.ValidationError("Kwota docelowa musi być liczbą dodatnią.")
        return kwota_docelowa

    def clean_obecna_kwota(self):
        obecna_kwota = self.cleaned_data.get('obecna_kwota')
        kwota_docelowa = self.cleaned_data.get('kwota_docelowa')
        if obecna_kwota < 0:
            raise forms.ValidationError("Kwota obecna nie może być ujemna.")
        if kwota_docelowa is not None and obecna_kwota > kwota_docelowa:
            raise forms.ValidationError("Kwota obecna nie może być większa niż kwota docelowa.")
        return obecna_kwota

class TransakcjaForm(forms.ModelForm):
    class Meta:
        model = Transakcja
        fields = ['typ', 'kwota', 'data', 'opis', 'kategoria']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'date-input', 'placeholder': 'RRRR-MM-DD'}),
            'opis': forms.Textarea(attrs={'class': 'opis-input', 'rows': 1, 'cols': 50}),
        }
    
    def clean_kwota(self):
        kwota = self.cleaned_data.get('kwota')
        if kwota <= 0:
            raise forms.ValidationError("Kwota musi być liczbą dodatnią.")
        return kwota

    def clean_data(self):
        data = self.cleaned_data.get('data')
        if data > date.today():
            raise forms.ValidationError("Transakcja nie może być z przyszłości.")
        return data

class BudzetForm(forms.ModelForm):
    class Meta:
        model = Budzet
        fields = ['kategoria', 'miesiac', 'limit']

    def clean_limit(self):
        limit = self.cleaned_data.get('limit')
        if limit <= 0:
            raise forms.ValidationError("Limit musi być liczbą dodatnią.")
        return limit
        
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