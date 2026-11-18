# Backend de LibroMundo

API de catálogo desarrollada con Django REST Framework y SQLite para el Laboratorio 13.

## Preparar el entorno en Windows

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py makemigrations catalog
python manage.py migrate
python manage.py seed_catalog
python manage.py runserver
```

Servicios disponibles:

- `http://127.0.0.1:8000/api/health/`
- `http://127.0.0.1:8000/api/categories/`
- `http://127.0.0.1:8000/api/products/`
- `http://127.0.0.1:8000/admin/`

Las categorías y productos se administran desde Django Admin. El frontend consulta los endpoints públicos de lectura y vuelve a cargar los datos al actualizar la página.
