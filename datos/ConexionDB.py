import sqlite3
from pathlib import Path


class ConexionDB:
	_instancia = None

	def __new__(cls, db_path=None):
		if cls._instancia is None:
			cls._instancia = super().__new__(cls)
			cls._instancia._inicializada = False
		return cls._instancia

	def __init__(self, db_path=None):
		if self._inicializada:
			return

		base_dir = Path(__file__).resolve().parents[1]
		self.db_path = Path(db_path) if db_path else base_dir / "reservas.db"
		self._conexion = sqlite3.connect(self.db_path, check_same_thread=False)
		self._conexion.row_factory = sqlite3.Row
		self._conexion.execute("PRAGMA foreign_keys = ON")
		self._crear_tablas()
		self._migrar_columna_password()
		self._crear_datos_iniciales()
		self._inicializada = True

	@classmethod
	def get_instance(cls, db_path=None):
		return cls(db_path)

	def conectar(self):
		return self._conexion

	def _crear_tablas(self):
		self._conexion.executescript(
			"""
			CREATE TABLE IF NOT EXISTS usuario (
				id_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
				nombre TEXT NOT NULL,
				email TEXT NOT NULL UNIQUE,
				password TEXT NOT NULL,
				rol TEXT NOT NULL CHECK (rol IN ('cliente', 'admin'))
			);

			CREATE TABLE IF NOT EXISTS cliente (
				id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
				id_usuario INTEGER NOT NULL UNIQUE,
				telefono TEXT,
				estado TEXT NOT NULL DEFAULT 'activo',
				fecha_registro TEXT NOT NULL,
				preferencias TEXT,
				FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
			);

			CREATE TABLE IF NOT EXISTS administrador (
				id_admin INTEGER PRIMARY KEY AUTOINCREMENT,
				id_usuario INTEGER NOT NULL UNIQUE,
				cargo TEXT,
				telefono TEXT,
				fecha_contratacion TEXT NOT NULL,
				estado TEXT NOT NULL DEFAULT 'activo',
				salario REAL DEFAULT 0,
				FOREIGN KEY (id_usuario) REFERENCES usuario(id_usuario) ON DELETE CASCADE
			);

			CREATE TABLE IF NOT EXISTS restaurante (
				id_restaurante INTEGER PRIMARY KEY AUTOINCREMENT,
				nombre TEXT NOT NULL,
				direccion TEXT NOT NULL,
				telefono TEXT,
				descripcion TEXT
			);

			CREATE TABLE IF NOT EXISTS mesa (
				id_mesa INTEGER PRIMARY KEY AUTOINCREMENT,
				id_restaurante INTEGER NOT NULL,
				numero INTEGER NOT NULL,
				capacidad INTEGER NOT NULL,
				estado TEXT NOT NULL DEFAULT 'activa',
				FOREIGN KEY (id_restaurante) REFERENCES restaurante(id_restaurante) ON DELETE CASCADE
			);

			CREATE TABLE IF NOT EXISTS horario (
				id_horario INTEGER PRIMARY KEY AUTOINCREMENT,
				id_restaurante INTEGER NOT NULL,
				dia_semana TEXT NOT NULL,
				hora_inicio TEXT NOT NULL,
				hora_fin TEXT NOT NULL,
				FOREIGN KEY (id_restaurante) REFERENCES restaurante(id_restaurante) ON DELETE CASCADE
			);

			CREATE TABLE IF NOT EXISTS disponibilidad (
				id_disponibilidad INTEGER PRIMARY KEY AUTOINCREMENT,
				id_mesa INTEGER NOT NULL,
				fecha TEXT NOT NULL,
				hora_inicio TEXT NOT NULL,
				hora_fin TEXT NOT NULL,
				estado TEXT NOT NULL DEFAULT 'disponible',
				FOREIGN KEY (id_mesa) REFERENCES mesa(id_mesa) ON DELETE CASCADE,
				UNIQUE (id_mesa, fecha, hora_inicio, hora_fin)
			);

			CREATE TABLE IF NOT EXISTS reserva (
				id_reserva INTEGER PRIMARY KEY AUTOINCREMENT,
				id_cliente INTEGER NOT NULL,
				id_disponibilidad INTEGER NOT NULL,
				estado TEXT NOT NULL DEFAULT 'pendiente',
				num_personas INTEGER NOT NULL,
				FOREIGN KEY (id_cliente) REFERENCES cliente(id_cliente) ON DELETE CASCADE,
				FOREIGN KEY (id_disponibilidad) REFERENCES disponibilidad(id_disponibilidad) ON DELETE CASCADE
			);
			"""
		)
		self._conexion.commit()

	def _migrar_columna_password(self):
		columnas = [
			row["name"]
			for row in self._conexion.execute("PRAGMA table_info(usuario)").fetchall()
		]

		if "password" in columnas:
			return

		if "password_hash" in columnas:
			try:
				self._conexion.execute(
					"ALTER TABLE usuario RENAME COLUMN password_hash TO password"
				)
			except sqlite3.OperationalError:
				self._conexion.execute("ALTER TABLE usuario ADD COLUMN password TEXT")
				self._conexion.execute(
					"UPDATE usuario SET password = password_hash WHERE password IS NULL OR password = ''"
				)

		self._conexion.commit()

	def _crear_datos_iniciales(self):
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
		]

		for admin in admins:
			id_usuario = self._upsert_usuario(
				nombre=admin["nombre"],
				email=admin["email"],
				password=admin["password"],
				rol="admin",
			)
			self._upsert_administrador(
				id_usuario=id_usuario,
				cargo=admin["cargo"],
				telefono=admin["telefono"],
				salario=admin["salario"],
			)

		for cliente in clientes:
			id_usuario = self._upsert_usuario(
				nombre=cliente["nombre"],
				email=cliente["email"],
				password=cliente["password"],
				rol="cliente",
			)
			self._upsert_cliente(
				id_usuario=id_usuario,
				telefono=cliente["telefono"],
				preferencias=cliente["preferencias"],
			)

		for restaurante in restaurantes:
			id_restaurante = self._upsert_restaurante(
				nombre=restaurante["nombre"],
				direccion=restaurante["direccion"],
				telefono=restaurante["telefono"],
				descripcion=restaurante["descripcion"],
			)
			self._upsert_horarios(id_restaurante, restaurante["horarios"])
			self._upsert_mesas_base(id_restaurante)

		self._conexion.commit()


# métodos para inicialización, no para las peticiones normales del navegador.
	def _upsert_usuario(self, nombre, email, password, rol):
		usuario = self._conexion.execute(
			"SELECT id_usuario FROM usuario WHERE email = ?",
			(email,),
		).fetchone()
		if usuario:
			self._conexion.execute(
				"""
				UPDATE usuario
				SET nombre = ?, password = ?, rol = ?
				WHERE id_usuario = ?
				""",
				(nombre, password, rol, usuario["id_usuario"]),
			)
			return usuario["id_usuario"]

		cur = self._conexion.execute(
			"""
			INSERT INTO usuario(nombre, email, password, rol)
			VALUES (?, ?, ?, ?)
			""",
			(nombre, email, password, rol),
		)
		return cur.lastrowid

	def _upsert_administrador(self, id_usuario, cargo, telefono, salario):
		existente = self._conexion.execute(
			"SELECT id_admin FROM administrador WHERE id_usuario = ?",
			(id_usuario,),
		).fetchone()
		if existente:
			self._conexion.execute(
				"""
				UPDATE administrador
				SET cargo = ?, telefono = ?, estado = 'activo', salario = ?
				WHERE id_usuario = ?
				""",
				(cargo, telefono, salario, id_usuario),
			)
			return

		self._conexion.execute(
			"""
			INSERT INTO administrador(id_usuario, cargo, telefono, fecha_contratacion, estado, salario)
			VALUES (?, ?, ?, DATE('now'), 'activo', ?)
			""",
			(id_usuario, cargo, telefono, salario),
		)

	def _upsert_cliente(self, id_usuario, telefono, preferencias):
		existente = self._conexion.execute(
			"SELECT id_cliente FROM cliente WHERE id_usuario = ?",
			(id_usuario,),
		).fetchone()
		if existente:
			self._conexion.execute(
				"""
				UPDATE cliente
				SET telefono = ?, estado = 'activo', preferencias = ?
				WHERE id_usuario = ?
				""",
				(telefono, preferencias, id_usuario),
			)
			return

		self._conexion.execute(
			"""
			INSERT INTO cliente(id_usuario, telefono, estado, fecha_registro, preferencias)
			VALUES (?, ?, 'activo', DATE('now'), ?)
			""",
			(id_usuario, telefono, preferencias),
		)

	def _upsert_restaurante(self, nombre, direccion, telefono, descripcion):
		existente = self._conexion.execute(
			"SELECT id_restaurante FROM restaurante WHERE nombre = ?",
			(nombre,),
		).fetchone()
		if existente:
			self._conexion.execute(
				"""
				UPDATE restaurante
				SET direccion = ?, telefono = ?, descripcion = ?
				WHERE id_restaurante = ?
				""",
				(direccion, telefono, descripcion, existente["id_restaurante"]),
			)
			return existente["id_restaurante"]

		cur = self._conexion.execute(
			"""
			INSERT INTO restaurante(nombre, direccion, telefono, descripcion)
			VALUES (?, ?, ?, ?)
			""",
			(nombre, direccion, telefono, descripcion),
		)
		return cur.lastrowid

	def _upsert_horarios(self, id_restaurante, horarios):
		for dia_semana, hora_inicio, hora_fin in horarios:
			existente = self._conexion.execute(
				"""
				SELECT id_horario FROM horario
				WHERE id_restaurante = ? AND dia_semana = ? AND hora_inicio = ? AND hora_fin = ?
				""",
				(id_restaurante, dia_semana, hora_inicio, hora_fin),
			).fetchone()
			if existente:
				continue

			self._conexion.execute(
				"""
				INSERT INTO horario(id_restaurante, dia_semana, hora_inicio, hora_fin)
				VALUES (?, ?, ?, ?)
				""",
				(id_restaurante, dia_semana, hora_inicio, hora_fin),
			)

	def _upsert_mesas_base(self, id_restaurante):
		mesas_base = [
			(1, 2),
			(2, 4),
			(3, 4),
			(4, 6),
		]
		for numero, capacidad in mesas_base:
			existente = self._conexion.execute(
				"""
				SELECT id_mesa FROM mesa
				WHERE id_restaurante = ? AND numero = ?
				""",
				(id_restaurante, numero),
			).fetchone()
			if existente:
				self._conexion.execute(
					"""
					UPDATE mesa
					SET capacidad = ?, estado = 'activa'
					WHERE id_mesa = ?
					""",
					(capacidad, existente["id_mesa"]),
				)
				continue

			self._conexion.execute(
				"""
				INSERT INTO mesa(id_restaurante, numero, capacidad, estado)
				VALUES (?, ?, ?, 'activa')
				""",
				(id_restaurante, numero, capacidad),
			)
