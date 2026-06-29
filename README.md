# ⚽ WRC26 — Sistema de Gestión de Canchas
### FIFA World Cup 2026
 
---
 
## 👥 Integrantes
 
| Nombre | Área |
|--------|------|
| [Tu nombre] | Backend |
| [Nombre compañero] | Frontend |
| [Nombre compañero] | Documentación y Marketing |
 
---
 
## 🛠️ Lenguajes y Tecnologías
 
| Tecnología | Uso |
|-----------|-----|
| Python 3.14 | Lenguaje backend |
| Django 6.0 | Framework web |
| SQLite | Base de datos |
| HTML5 / CSS3 | Frontend |
| JavaScript | Interactividad |
| Leaflet.js | Mapas y geolocalización |
 
---
 
## 📁 Estructura de Carpetas
 
```
WRC26/
└── Project/
    ├── manage.py
    ├── db.sqlite3
    ├── Project/
    │   ├── settings.py
    │   ├── urls.py
    │   └── wsgi.py
    └── Api/
        ├── models.py        ← Base de datos
        ├── views.py         ← Lógica de negocio
        ├── urls.py          ← Rutas
        ├── forms.py         ← Formularios
        ├── admin.py         ← Panel de administración
        ├── tests.py         ← Tests automáticos
        ├── fixtures/
        │   └── equipos.json ← Carga inicial de datos
        └── Templates/
            └── canchas/
                ├── base.html
                ├── login.html
                ├── registro.html
                ├── inicio.html
                ├── lista_estadios.html
                ├── form_estadio.html
                ├── lista_canchas.html
                ├── detalle_cancha.html
                ├── form_cancha.html
                ├── lista_partidos.html
                ├── form_partido.html
                ├── lista_reservas.html
                ├── form_reserva.html
                ├── lista_equipos.html
                ├── form_equipo.html
                ├── mapa_estadios.html
                └── confirmar_eliminar.html
```
 
---
 
## 🚀 Ejecutar el Proyecto
 
### 1. Clonar el repositorio
```bash
git clone https://github.com/[tu-usuario]/WRC26.git
cd WRC26/Project
```
 
### 2. Instalar dependencias
```bash
pip install django
```
 
### 3. Aplicar migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```
 
### 4. Cargar datos iniciales (48 equipos del mundial)
```bash
python manage.py loaddata equipos.json
```
 
### 5. Crear superusuario
```bash
python manage.py createsuperuser
```
 
### 6. Ejecutar el servidor
```bash
python manage.py runserver
```
 
### 7. Abrir en el navegador
```
http://127.0.0.1:8000/
```
 
---
 
## 🔐 Datos de Acceso
 
| Tipo | Usuario | Contraseña |
|------|---------|------------|
| Administrador | admin | [la que creaste] |
| Operador | [usuario] | [contraseña] |
 
> Para asignar rol de Administrador: entrar al panel `/admin/` → Perfiles → cambiar rol.
 
---
 
## ✅ Funcionalidades
 
- Gestión de estadios con coordenadas geográficas
- Gestión de canchas por estadio
- Gestión de los 48 equipos del Mundial 2026
- Programación de partidos por fase
- Sistema de reservas con validación de horarios
- Mapa interactivo con ubicación de estadios
- Login / Logout / Registro de usuarios
- Control de permisos: Administrador y Operador
 
