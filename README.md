# Sistema de Reservas de Restaurante

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
- La conexion inicializa tablas automaticamente y crea admin demo.

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
│
├── app.py
├── requirements.txt
├── README.md
│
├── datos/
│   ├── ConexionDB.py
│   └── dao/
│       ├── base_dao.py
│       ├── usuario_dao.py
│       ├── cliente_dao.py
│       ├── administrador_dao.py
│       ├── restaurante_dao.py
│       ├── mesa_dao.py
│       ├── horario_dao.py
│       ├── disponibilidad_dao.py
│       └── reserva_dao.py
│
├── negocio/
│   ├── builders.py
│   ├── factories.py
│   ├── services.py
│   └── modelos/
│       ├── __init__.py
│       ├── usuario.py
│       ├── cliente.py
│       ├── administrador.py
│       └── reserva.py
│
└── presentacion/
    ├── controllers/
    │   ├── common.py
    │   ├── main_controller.py
    │   ├── auth_controller.py
    │   ├── cliente_controller.py
    │   └── admin_controller.py
    │
    ├── templates/
    │   ├── base.html
    │   ├── login.html
    │   ├── register.html
    │   ├── cliente_reservas.html
    │   └── admin_panel.html
    │
    └── static/
        ├── css/
        │   └── style.css
        └── js/
            └── app.js
```


Controllers: manejan la conversación web con el navegador.

Services: manejan las reglas del negocio.


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


## Base de datos

- Archivo SQLite: `reservas.db` (se crea automaticamente en la raiz del proyecto).
- Si quieres reiniciar datos de prueba:
  1. Cierra la app.
  2. Borra `reservas.db`.
  3. Ejecuta de nuevo `python app.py`.

## Notas de diseño

- Se priorizo simplicidad para fines academicos.
- Los controladores Flask se separaron en Blueprints dentro de `presentacion/controllers/`.
- La capa `negocio/services.py` contiene la logica de aplicacion.
- Los DAOs centralizan operaciones SQL por entidad.


## Casos de uso iniciales 

### Administradores

| Nombre          | Email                                       | Password | Cargo                 | Teléfono   | Salario |
| --------------- | ------------------------------------------- | -------- | --------------------- | ---------- | ------- |
| Administrador   | [admin@local.com](mailto:admin@local.com)   | admin123 | Administrador General | 3001000001 | 3500    |
| Marta Jaramillo | [admin2@local.com](mailto:admin2@local.com) | admin234 | Gerente Operaciones   | 3001000002 | 3200    |
| Diego Ruiz      | [admin3@local.com](mailto:admin3@local.com) | admin345 | Supervisor            | 3001000003 | 2800    |


### Clientes

| Nombre       | Email                                           | Password   | Teléfono   | Preferencias          |
| ------------ | ----------------------------------------------- | ---------- | ---------- | --------------------- |
| Sofia Lopez  | [cliente1@local.com](mailto:cliente1@local.com) | cliente123 | 3010000001 | Mesa cerca de ventana |
| Carlos Perez | [cliente2@local.com](mailto:cliente2@local.com) | cliente234 | 3010000002 | Sin gluten            |
| Laura Medina | [cliente3@local.com](mailto:cliente3@local.com) | cliente345 | 3010000003 | Zona tranquila        |

### Restaurantes 

| Nombre      | Dirección         | Teléfono   | Descripción                   |
| ----------- | ----------------- | ---------- | ----------------------------- |
| La Terraza  | Calle 10 #12-34   | 6041111111 | Comida tradicional y parrilla |
| Sushi Norte | Carrera 45 #8-21  | 6042222222 | Sushi y cocina asiatica       |
| Pasta Viva  | Avenida 33 #55-78 | 6043333333 | Pasta artesanal y vinos       |

### Horarios - La terraza

| Día       | Apertura | Cierre |
| --------- | -------- | ------ |
| Sabado    | 12:00    | 23:00  |
| Domingo   | 12:00    | 20:00  |

### Horarios - Sushi Norte 

| Día       | Apertura | Cierre |
| --------- | -------- | ------ |
| Lunes     | 11:30    | 21:30  |
| Martes    | 11:30    | 21:30  |
| Miercoles | 11:30    | 21:30  |
| Jueves    | 11:30    | 21:30  |
| Viernes   | 11:30    | 22:30  |
| Sabado    | 12:00    | 22:30  |

### Horarios Pasta Viva 
| Día       | Apertura | Cierre |
| --------- | -------- | ------ |
| Martes    | 12:00    | 21:00  |
| Miercoles | 12:00    | 21:00  |
| Jueves    | 12:00    | 21:00  |
| Viernes   | 12:00    | 22:00  |
| Sabado    | 12:00    | 22:00  |
| Domingo   | 12:00    | 20:00  |


