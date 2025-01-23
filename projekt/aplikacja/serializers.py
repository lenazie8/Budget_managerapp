from rest_framework import serializers
from .models import Kategoria, ProfilUzytkownika, CelOszczednosciowy, Transakcja, Budzet

class KategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kategoria
        fields = '__all__'

class ProfilUzytkownikaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilUzytkownika
        fields = '__all__'

class CelOszczednosciowySerializer(serializers.ModelSerializer):
    class Meta:
        model = CelOszczednosciowy
        fields = '__all__'

class TransakcjaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transakcja
        fields = '__all__'

class BudzetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Budzet
        fields = '__all__'