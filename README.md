# Budget_managerapp
## **Jak zacząć**

**Wymagania wstępne**

Upewnij się, że w systemie zainstalowane są następujące elementy:

- Python 3.8 lub nowszy
- Git
- Edytor kodu 
- pip (menedżer pakietów Pythona)

---

**Instrukcje konfiguracji**

#### **Krok 1: Sklonuj repozytorium**

Sklonuj projekt z repozytorium GitHub:
```bash
git clone <repository-url>
cd personal_budget_management
```

#### **Krok 2: Utwórz wirtualne środowisko**

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

masOC/Linux:
```bash
python3 -m venv venv
źródło venv/bin/activate
```

#### **Krok 3: Instalacja potrzebnych paczek**

Zainstaluj wymagane paczki za pomocą pip:


```bash
pip install djangorestframework
```

#### **Krok 4: Zastosowanie migracji**

```bash
python manage.py makemigrations
python manage.py migrate
```

#### **Krok 5: Uruchomienie serwera**

```bash
python manage.py runserver
```
Odwiedź aplikację pod adresem `http://localhost:8000`

