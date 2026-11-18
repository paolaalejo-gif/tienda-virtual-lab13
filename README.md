# LibroMundo - Laboratorio 13

Tienda virtual de libros desarrollada con React + Vite para el frontend y Django REST Framework para el backend. El catálogo muestra productos servidos desde SQLite mediante endpoints REST; las categorías se filtran en la interfaz y los detalles se presentan en un diálogo accesible.

## Estructura

- `frontend/`: React, Vite, Tailwind CSS, shadcn/ui y portadas SVG locales.
- `backend/`: Django REST Framework, aplicación `catalog`, modelos, serializadores, administración y SQLite.

## Ejecutar en Windows

Abre una terminal en la carpeta raíz `tienda-virtual-lab13`.

1. Iniciar el backend:

```powershell
.\backend\.venv\Scripts\python.exe .\backend\manage.py migrate
.\backend\.venv\Scripts\python.exe .\backend\manage.py seed_catalog
.\backend\.venv\Scripts\python.exe .\backend\manage.py runserver 127.0.0.1:8000
```

2. En una segunda terminal, iniciar el frontend:

```powershell
cd frontend
npm install
npm run dev
```

Abre `http://127.0.0.1:5173/`.

## Endpoints

- `GET /api/health/`
- `GET /api/categories/`
- `GET /api/products/`
- `GET /api/products/?category=<id>`
- `http://127.0.0.1:8000/admin/`

Para administrar el catálogo, crea un usuario local con `.\backend\.venv\Scripts\python.exe .\backend\manage.py createsuperuser`. Los modelos `Category` y `Product` están registrados en Django Admin. El comando `seed_catalog` puede ejecutarse varias veces para restaurar o actualizar los datos de demostración.

## Alcance

La práctica cubre la estructura visual del catálogo, componentes React reutilizables, el filtrado por categorías, los modelos relacionados de categoría y producto, los servicios REST y la integración React-Django. El laboratorio deja fuera carrito, pedidos, autenticación de clientes y pagos.
