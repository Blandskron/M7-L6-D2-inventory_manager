# Sistema MVC de Inventario (CRUD + CSRF)

## Cobertura del aula

Este proyecto cumple los resultados 6, 6.1, 6.2 y 6.3: emplea los modelos `Product` y `Movement` como capa de acceso a datos, vistas y templates MVC para CRUD completo, y el ORM de Django mediante `objects.all()`, `get_object_or_404()`, `form.save()`, `delete()`, `select_related()` y `F()`.

- CSRF: todos los formularios POST incluyen `{% csrf_token %}` y el middleware CSRF está activo.
- Enrutamiento: las rutas se incluyen desde el proyecto e incorporan parámetros, por ejemplo `products/edit/<int:id>/` y `movements/delete/<int:id>/`.
- Relaciones: cada `Movement` está asociado a un `Product` por `ForeignKey`; al crear, editar o eliminar un movimiento el stock se ajusta de manera consistente.
- Pruebas: `python manage.py test` verifica CRUD, CSRF, rutas parametrizadas, ORM y stock.

## 1) Crear entorno virtual

```bash
python -m venv venv
```

## 2) Activar entorno virtual

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## 3) Actualizar pip

```bash
python -m pip install --upgrade pip
```

## 4) Instalar Django

```bash
pip install django
```

## 5) Crear proyecto

```bash
django-admin startproject inventory_manager
```

## 6) Entrar al proyecto

```bash
cd inventory_manager
```

## 7) Crear aplicación

```bash
python manage.py startapp inventory
```

## 8) Agregar la app en `inventory_manager/settings.py`

En `INSTALLED_APPS` agregar:

```python
'inventory',
```

## 9) Crear rutas de la app

Crear/editar el archivo:

* `inventory/urls.py` (pegar el código del proyecto)

## 10) Incluir rutas de la app en el `urls.py` del proyecto

Editar `inventory_manager/urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    path('', include('inventory.urls')),
]
```

## 11) Crear modelos, formularios y vistas

Crear/editar estos archivos:

* `inventory/models.py`
* `inventory/forms.py`
* `inventory/views.py`

Pegar el código correspondiente en cada archivo.

## 12) Crear templates

Crear la carpeta:

* `inventory/templates/inventory/`

Crear estos archivos dentro:

* `base.html`
* `product_list.html`
* `product_form.html`
* `product_confirm_delete.html`
* `movement_list.html`
* `movement_form.html`
* `movement_confirm_delete.html`

Pegar el código correspondiente en cada template.

## 13) Crear migraciones

```bash
python manage.py makemigrations
```

## 14) Aplicar migraciones

```bash
python manage.py migrate
```

## 15) Crear superusuario (opcional)

```bash
python manage.py createsuperuser
```

## 16) Ejecutar servidor

```bash
python manage.py runserver
```

## 17) Abrir rutas en navegador

* Productos: `http://127.0.0.1:8000/products/`
* Movimientos: `http://127.0.0.1:8000/movements/`

## Ejecutar con Docker

Desde la raíz del repositorio:

```bash
docker compose up --build
```

El `entrypoint.sh` aplica migraciones y crea el superusuario en el primer inicio. Configura `DJANGO_SUPERUSER_USERNAME`, `DJANGO_SUPERUSER_EMAIL` y `DJANGO_SUPERUSER_PASSWORD` en un archivo `.env` para reemplazar las credenciales de ejemplo. La base SQLite queda persistida en el volumen `inventory_data`.
