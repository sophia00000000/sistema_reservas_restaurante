# Guia Basica de Flask para este proyecto

Este documento esta pensado para ti si nunca has trabajado con frameworks web, endpoints, puertos o peticiones HTTP.

## 1) Que es Flask

Flask es un framework web de Python.

En palabras simples:
- Python por si solo ejecuta scripts en consola.
- Flask permite que Python reciba solicitudes desde un navegador.
- Asi puedes crear una aplicacion web (paginas, formularios, login, etc.).

## 2) Conceptos minimos que debes entender

### Servidor web local

Cuando ejecutas:

```bash
python app.py
```

Flask levanta un servidor local en tu computadora.

### Puerto

por defecto es el `5000`.

Por eso entras con:

```text
http://127.0.0.1:5000
```

### Endpoint (ruta)

Un endpoint es una URL de tu app que hace algo.

Ejemplos de este proyecto:
- `/login`
- `/register`
- `/cliente/reservas`
- `/admin/panel`

Cada endpoint esta conectado a una funcion en Python dentro de los controladores.

### Peticion HTTP

El navegador hace peticiones al servidor.
Los 2 metodos principales que usas aqui son:
- `GET`: pedir una pagina o datos.
- `POST`: enviar datos de formulario (login, registro, crear reserva, etc.).

## 3) Como se usa Flask en este proyecto

Tu proyecto esta dividido por capas:

1. Presentacion
- `presentacion/templates/` (HTML)
- `presentacion/static/` (CSS/JS)
- `presentacion/controllers/` (endpoints Flask)

2. Negocio
- `negocio/services.py` (reglas y casos de uso)
- `negocio/factories.py`, `negocio/builders.py`, `negocio/modelos/`

3. Datos
- `datos/dao/` (consultas SQL)
- `datos/ConexionDB.py` (Singleton de SQLite)

### Flujo real de una peticion

Ejemplo: login

1. El usuario abre `/login` (GET).
2. Flask ejecuta el endpoint en `auth_controller.py` y renderiza `login.html`.
3. Usuario envia formulario (POST) con email/password.
4. El controlador llama a `AuthService` (capa negocio).
5. `AuthService` usa `UsuarioDAO` (capa datos) para buscar usuario en SQLite.
6. Si todo esta bien, Flask guarda datos en `session` y redirige.

## 4) Donde estan tus endpoints

- `presentacion/controllers/main_controller.py`
- `presentacion/controllers/auth_controller.py`
- `presentacion/controllers/cliente_controller.py`
- `presentacion/controllers/admin_controller.py`

Estan organizados con Blueprints.

## 5) Que es un Blueprint

Un Blueprint en Flask sirve para agrupar endpoints por modulo.

En vez de tener todo en `app.py`, separas por responsabilidad:
- Auth
- Cliente
- Admin
- Main

Despues en `app.py` se registran:
- `app.register_blueprint(main_bp)`
- `app.register_blueprint(auth_bp)`
- `app.register_blueprint(cliente_bp)`
- `app.register_blueprint(admin_bp)`

Esto mejora orden y mantenibilidad.

## 6) Como correr y probar el proyecto

1. Instala dependencias:

```bash
pip install -r requirements.txt
```

2. Ejecuta:

```bash
python app.py
```

3. Abre en navegador:

```text
http://127.0.0.1:5000
```

4. Admin demo:
- Email: `admin@local.com`
- Password: `admin123`

## 7) Como leer los mensajes en la terminal

Al correr Flask, veras algo como:

```text
* Running on http://127.0.0.1:5000
```

Eso significa que el servidor esta encendido.
Si cierras la terminal o presionas `Ctrl + C`, el servidor se apaga.

## 8) Errores comunes de principiante

1. "Address already in use" o puerto ocupado
- Ya hay otra app usando ese puerto.
- Cierra la otra app o cambia de puerto.

2. "ModuleNotFoundError"
- Faltan dependencias.
- Reinstala con `pip install -r requirements.txt`.

3. Pagina no abre
- Verifica que Flask siga corriendo en terminal.
- Verifica URL exacta: `http://127.0.0.1:5000`.

## 9) Mini resumen mental

- Flask recibe peticiones del navegador.
- Los endpoints (controladores) deciden que hacer con esa peticion.
- Los servicios aplican reglas de negocio.
- Los DAO leen/escriben en SQLite.
- Flask devuelve HTML al navegador.

Si entiendes ese flujo, ya tienes la base de desarrollo web con Python.
