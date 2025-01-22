from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Kategoria(models.Model):
    KATEGORIE_CHOICES = [
        ('codzienne_wydatki', 'Codzienne wydatki'),
        ('darowizna', 'Darowizna'),
        ('edukacja', 'Edukacja'),
        ('jedzenie_poza_domem', 'Jedzenie poza domem'),
        ('osobiste', 'Osobiste'),
        ('platnosci', 'Płatności'),
        ('praca', 'Praca'),
        ('rachunki', 'Rachunki'),
        ('rozrywka', 'Rozrywka'),
        ('transport', 'Transport'),
        ('uslugi', 'Usługi'),
        ('zakupy_spozywcze', 'Zakupy spożywcze'),
    ]

    nazwa = models.CharField(max_length=100, choices=KATEGORIE_CHOICES)

    def __str__(self):
        return self.get_nazwa_display()

class ProfilUzytkownika(models.Model):
    uzytkownik = models.OneToOneField(User, on_delete=models.CASCADE)
    limit_budzetu = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.uzytkownik.username

class CelOszczednosciowy(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    nazwa = models.CharField(max_length=100)
    kwota_docelowa = models.DecimalField(max_digits=10, decimal_places=2)
    obecna_kwota = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    data_osiagniecia = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nazwa

class Transakcja(models.Model):
    TYP_TRANSAKCJI = (
        ('Przychód', 'Przychód'),
        ('Wydatek', 'Wydatek'),
    )

    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    typ = models.CharField(max_length=10, choices=TYP_TRANSAKCJI)
    kwota = models.DecimalField(max_digits=10, decimal_places=2)
    data = models.DateField()
    opis = models.TextField(blank=True, null=True)
    kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.uzytkownik.username} - {self.typ}: {self.kwota} ({self.kategoria})"

class Budzet(models.Model):
    MIESIACE_CHOICES = [
        ('01', 'Styczeń'),
        ('02', 'Luty'),
        ('03', 'Marzec'),
        ('04', 'Kwiecień'),
        ('05', 'Maj'),
        ('06', 'Czerwiec'),
        ('07', 'Lipiec'),
        ('08', 'Sierpień'),
        ('09', 'Wrzesień'),
        ('10', 'Październik'),
        ('11', 'Listopad'),
        ('12', 'Grudzień'),
    ]

    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    kategoria = models.ForeignKey(Kategoria, on_delete=models.CASCADE)
    miesiac = models.CharField(max_length=2, choices=MIESIACE_CHOICES)
    limit = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Budżet: {self.kategoria} ({self.get_miesiac_display()})"

class Powiadomienie(models.Model):
    uzytkownik = models.ForeignKey(User, on_delete=models.CASCADE)
    tresc = models.TextField()
    przeczytane = models.BooleanField(default=False)
    data_utworzenia = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Powiadomienie dla {self.uzytkownik.username}: {self.tresc}"