# BiblioSmart - Sistema de Biblioteca Virtual

BiblioSmart es una plataforma web desarrollada en Python con Django para la gestión de recursos educativos del Colegio UNI. El proyecto implementa una arquitectura MVT y utiliza Programación Multiparadigma (Orientada a Objetos, Lógica y Funcional).

## Requisitos Previos

Antes de ejecutar el proyecto, asegúrate de tener instalado lo siguiente en tu sistema:

1. **Python 3.8+**: [Descargar Python](https://www.python.org/downloads/)
2. **SWI-Prolog**: Es **obligatorio** tener instalado SWI-Prolog para que el motor lógico (`PySwip`) funcione correctamente. 
   - [Descargar SWI-Prolog](https://www.swi-prolog.org/Download.html)
   - *Nota para Windows:* Asegúrate de marcar la casilla "Add SWI-Prolog to the system PATH" durante la instalación.

## Instrucciones de Despliegue Local

Sigue estos pasos en tu terminal (Símbolo del sistema, PowerShell o la terminal de VS Code) para ejecutar el proyecto en tu computadora.

### 1. Ubicarse en el proyecto
Abre la carpeta raíz del proyecto (donde se encuentra el archivo `manage.py`) en tu terminal.

### 2. Crear y activar un entorno virtual (Recomendado)
Para evitar conflictos con otras librerías, crea un entorno virtual:
```bash
# Crear el entorno virtual (solo la primera vez)
python -m venv venv

# Activar el entorno virtual en Windows:
venv\Scripts\activate
# Activar el entorno virtual en Mac/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias
Instala Django y PySwip (el puente para Prolog). Si cuentas con un archivo `requirements.txt`, ejecuta el segundo comando.
```bash
pip install django pyswip

# O si cuentas con un archivo requirements.txt:
# pip install -r requirements.txt
```

### 4. Aplicar las migraciones de la base de datos
Este comando crea las tablas necesarias en la base de datos (SQLite3 por defecto) basándose en los modelos del proyecto.
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crear un súper usuario (Administrador / Bibliotecario)
Para acceder al panel de administración y al Dashboard de bibliotecario, necesitas crear una cuenta con permisos de administrador:
```bash
python manage.py createsuperuser
```
*(Sigue las instrucciones en consola para asignar un nombre de usuario, correo y contraseña).*

### 6. Ejecutar el servidor de desarrollo
Finalmente, levanta el servidor de Django:
```bash
python manage.py runserver
```

### 7. Acceder a la aplicación
Abre tu navegador web y visita la siguiente dirección:
- **Sitio público/Login:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Panel de Admin (Opcional):** [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

## Consideraciones Técnicas
- **Base de Datos:** SQLite3 (Entorno de desarrollo local).
- **Lógica de Negocio (Prolog):** Las reglas de validación lógica se encuentran en `apps/prestamos/prolog/reglas.pl`.
- **Framework:** Django 5.x.
