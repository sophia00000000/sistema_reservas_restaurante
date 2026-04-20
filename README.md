# Sistema de Reservas de Restaurante (Mini Proyecto)

Mini proyecto educativo para entender patrones creacionales con una app web local.

Tecnologias usadas:
- Python (Flask)
- SQLite
- HTML
- CSS
- JavaScript

## Objetivo

Construir un sistema sencillo de reservas con 2 roles:
- Cliente: registro, login y creacion de reservas.
- Administrador: login, gestion de restaurantes, mesas, horarios y visualizacion de reservas.

## Patrones de diseno aplicados

### 1) Singleton
Archivo: `datos/ConexionDB.py`

- `ConexionDB` asegura una sola instancia de conexion a SQLite.
- La conexion inicializa tablas automaticamente y crea un admin demo.

### 2) Factory Method
Archivo: `negocio/factories.py`

- `UsuarioFactory` define la interfaz.
- `ClienteFactory` crea objetos `Cliente`.
- `AdminFactory` crea objetos `Administrador`.

### 3) Builder
Archivo: `negocio/builders.py`

- `ReservaBuilder` construye la reserva paso a paso.
- `ReservaDirector` encapsula una receta de construccion estandar.

## Estructura por capas

```text
sistema_reservas_restaurante/
  app.py
  requirements.txt
  README.md
  datos/
    ConexionDB.py
    dao/
      base_dao.py
      usuario_dao.py
      cliente_dao.py
      administrador_dao.py
      restaurante_dao.py
      mesa_dao.py
      horario_dao.py
      disponibilidad_dao.py
      reserva_dao.py
  negocio/
    builders.py
    factories.py
    services.py
    modelos/
      __init__.py
      usuario.py
      cliente.py
      administrador.py
      reserva.py
  presentacion/
    controllers/
      common.py
      main_controller.py
      auth_controller.py
      cliente_controller.py
      admin_controller.py
    templates/
      base.html
      login.html
      register.html
      cliente_reservas.html
      admin_panel.html
    static/
      css/style.css
      js/app.js
```

## Flujo funcional minimo

### Cliente
1. Se registra en `/register`.
2. Inicia sesion en `/login`.
3. En `/cliente/reservas`:
   - selecciona restaurante,
   - selecciona mesa,
   - define fecha/hora,
   - ingresa numero de personas,
   - guarda la reserva.

### Administrador
1. Inicia sesion en `/login`.
2. En `/admin/panel`:
   - crea restaurantes,
   - crea mesas,
   - define horarios,
   - visualiza reservas registradas.

## Requisitos

- Python 3.10+ (recomendado 3.11 o superior)
- pip

## Instrucciones para correr el proyecto (local)

1. Abrir terminal en la carpeta del proyecto.
2. Crear entorno virtual (opcional pero recomendado):

```bash
python -m venv .venv
```

3. Activar entorno virtual:

Windows PowerShell:
```powershell
.venv\Scripts\Activate.ps1
```

4. Instalar dependencias:

```bash
pip install -r requirements.txt
```

5. Ejecutar la app:

```bash
python app.py
```

6. Abrir en navegador:

```text
http://127.0.0.1:5000
```

## Credenciales demo administrador

- Email: `admin@local.com`
- Password: `admin123`

Estas credenciales se crean automaticamente la primera vez que inicia la base de datos.

## Base de datos

- Archivo SQLite: `reservas.db` (se crea automaticamente en la raiz del proyecto).
- Si quieres reiniciar datos de prueba:
  1. Cierra la app.
  2. Borra `reservas.db`.
  3. Ejecuta de nuevo `python app.py`.

## Notas de diseno

- Se priorizo simplicidad para fines academicos.
- Los controladores Flask se separaron en Blueprints dentro de `presentacion/controllers/`.
- La capa `negocio/services.py` contiene la logica de aplicacion.
- Los DAOs centralizan operaciones SQL por entidad.
- Las vistas estan limitadas a formularios esenciales para cumplir el enunciado.

## Posibles mejoras (opcional)

- Confirmacion/cancelacion de reservas por admin.
- Validacion de cruces de horarios mas avanzada.
- Paginacion y filtros en listados.
- Tests unitarios para Builder, Factory y Services.

## casos de uso iniciales 


3 administradores:
admin@local.com / admin123
admin2@local.com / admin234
admin3@local.com / admin345
3 usuarios cliente:
cliente1@local.com / cliente123
cliente2@local.com / cliente234
cliente3@local.com / cliente345
3 restaurantes:
La Terraza
Sushi Norte
Pasta Viva
Horarios por día para cada restaurante.

Mesas base por restaurante:

Mesa 1 (2 personas)
Mesa 2 (4 personas)
Mesa 3 (4 personas)
Mesa 4 (6 personas)


        admins = [
                    {
                        "nombre": "Administrador",
                        "email": "admin@local.com",
                        "password": "admin123",
                        "cargo": "Administrador General",
                        "telefono": "3001000001",
                        "salario": 3500,
                    },
                    {
                        "nombre": "Marta Jaramillo",
                        "email": "admin2@local.com",
                        "password": "admin234",
                        "cargo": "Gerente Operaciones",
                        "telefono": "3001000002",
                        "salario": 3200,
                    },
                    {
                        "nombre": "Diego Ruiz",
                        "email": "admin3@local.com",
                        "password": "admin345",
                        "cargo": "Supervisor",
                        "telefono": "3001000003",
                        "salario": 2800,
                    },
                ]

                clientes = [
                    {
                        "nombre": "Sofia Lopez",
                        "email": "cliente1@local.com",
                        "password": "cliente123",
                        "telefono": "3010000001",
                        "preferencias": "Mesa cerca de ventana",
                    },
                    {
                        "nombre": "Carlos Perez",
                        "email": "cliente2@local.com",
                        "password": "cliente234",
                        "telefono": "3010000002",
                        "preferencias": "Sin gluten",
                    },
                    {
                        "nombre": "Laura Medina",
                        "email": "cliente3@local.com",
                        "password": "cliente345",
                        "telefono": "3010000003",
                        "preferencias": "Zona tranquila",
                    },
                ]

                restaurantes = [
                    {
                        "nombre": "La Terraza",
                        "direccion": "Calle 10 #12-34",
                        "telefono": "6041111111",
                        "descripcion": "Comida tradicional y parrilla",
                        "horarios": [
                            ("Lunes", "12:00", "22:00"),
                            ("Martes", "12:00", "22:00"),
                            ("Miercoles", "12:00", "22:00"),
                            ("Jueves", "12:00", "22:00"),
                            ("Viernes", "12:00", "23:00"),
                            ("Sabado", "12:00", "23:00"),
                            ("Domingo", "12:00", "20:00"),
                        ],
                    },
                    {
                        "nombre": "Sushi Norte",
                        "direccion": "Carrera 45 #8-21",
                        "telefono": "6042222222",
                        "descripcion": "Sushi y cocina asiatica",
                        "horarios": [
                            ("Lunes", "11:30", "21:30"),
                            ("Martes", "11:30", "21:30"),
                            ("Miercoles", "11:30", "21:30"),
                            ("Jueves", "11:30", "21:30"),
                            ("Viernes", "11:30", "22:30"),
                            ("Sabado", "12:00", "22:30"),
                        ],
                    },
                    {
                        "nombre": "Pasta Viva",
                        "direccion": "Avenida 33 #55-78",
                        "telefono": "6043333333",
                        "descripcion": "Pasta artesanal y vinos",
                        "horarios": [
                            ("Martes", "12:00", "21:00"),
                            ("Miercoles", "12:00", "21:00"),
                            ("Jueves", "12:00", "21:00"),
                            ("Viernes", "12:00", "22:00"),
                            ("Sabado", "12:00", "22:00"),
                            ("Domingo", "12:00", "20:00"),
                        ],
                    },