from datetime import datetime

from datos.dao.administrador_dao import AdministradorDAO
from datos.dao.cliente_dao import ClienteDAO
from datos.dao.disponibilidad_dao import DisponibilidadDAO
from datos.dao.horario_dao import HorarioDAO
from datos.dao.mesa_dao import MesaDAO
from datos.dao.reserva_dao import ReservaDAO
from datos.dao.restaurante_dao import RestauranteDAO
from datos.dao.usuario_dao import UsuarioDAO
from negocio.builders import ReservaBuilder, ReservaDirector
from negocio.factories import AdminFactory, ClienteFactory


class AuthService:
    def __init__(self, db):
        self.usuario_dao = UsuarioDAO(db)
        self.cliente_dao = ClienteDAO(db)
        self.admin_dao = AdministradorDAO(db)
        self.cliente_factory = ClienteFactory()
        self.admin_factory = AdminFactory()

    def registrar_cliente(self, nombre, email, password, telefono, preferencias):
        if self.usuario_dao.buscar_por_email(email):
            raise ValueError("El email ya esta registrado")

        cliente_obj = self.cliente_factory.crear_usuario(
            {
                "nombre": nombre,
                "email": email,
                "password_hash": password,
                "telefono": telefono,
                "preferencias": preferencias,
            }
        )

        id_usuario = self.usuario_dao.crear(
            {
                "nombre": cliente_obj.nombre,
                "email": cliente_obj.email,
                "password_hash": cliente_obj.password_hash,
                "rol": "cliente",
            }
        )

        id_cliente = self.cliente_dao.crear(
            {
                "id_usuario": id_usuario,
                "telefono": cliente_obj.telefono,
                "estado": cliente_obj.estado,
                "preferencias": cliente_obj.preferencias,
            }
        )
        return {"id_usuario": id_usuario, "id_cliente": id_cliente}

    def login(self, email, password):
        usuario = self.usuario_dao.buscar_por_email(email)
        if not usuario:
            return None

        if usuario["password_hash"] != password:
            return None

        result = {
            "id_usuario": usuario["id_usuario"],
            "nombre": usuario["nombre"],
            "email": usuario["email"],
            "rol": usuario["rol"],
        }

        if usuario["rol"] == "cliente":
            cliente = self.cliente_dao.buscar_por_usuario(usuario["id_usuario"])
            if cliente:
                result["id_cliente"] = cliente["id_cliente"]
        else:
            admin = self.admin_dao.buscar_por_usuario(usuario["id_usuario"])
            if admin:
                result["id_admin"] = admin["id_admin"]

        return result


class ReservaService:
    def __init__(self, db):
        self.restaurante_dao = RestauranteDAO(db)
        self.mesa_dao = MesaDAO(db)
        self.horario_dao = HorarioDAO(db)
        self.disponibilidad_dao = DisponibilidadDAO(db)
        self.reserva_dao = ReservaDAO(db)
        self.builder = ReservaBuilder()
        self.director = ReservaDirector()

    def listar_restaurantes(self):
        return self.restaurante_dao.listar_todos()

    def listar_mesas_por_restaurante(self, id_restaurante):
        return self.mesa_dao.buscar_por_restaurante(id_restaurante)

    def listar_horarios_por_restaurante(self, id_restaurante):
        if not id_restaurante:
            return []
        return self.horario_dao.buscar_por_restaurante(id_restaurante)

    def _validar_datos_reserva(self, fecha, hora_inicio, hora_fin):
        if not fecha or not hora_inicio or not hora_fin:
            raise ValueError("Fecha y horas son obligatorias")

        try:
            inicio_dt = datetime.strptime(hora_inicio, "%H:%M")
            fin_dt = datetime.strptime(hora_fin, "%H:%M")
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError("Formato de fecha/hora invalido") from exc

        if inicio_dt >= fin_dt:
            raise ValueError("La hora de inicio debe ser menor que la hora de fin")

        return fecha_dt

    def _validar_reglas_reserva(
        self,
        id_restaurante,
        id_mesa,
        fecha,
        hora_inicio,
        hora_fin,
        num_personas,
        excluir_id_disponibilidad=None,
    ):
        mesa = self.mesa_dao.buscar_por_id(id_mesa)
        if not mesa:
            raise ValueError("La mesa no existe")

        if int(mesa["id_restaurante"]) != int(id_restaurante):
            raise ValueError("La mesa seleccionada no pertenece al restaurante")

        if mesa["estado"] != "activa":
            raise ValueError("La mesa no esta activa para reservas")

        fecha_dt = self._validar_datos_reserva(fecha, hora_inicio, hora_fin)
        dia_semana = [
            "Lunes",
            "Martes",
            "Miercoles",
            "Jueves",
            "Viernes",
            "Sabado",
            "Domingo",
        ][fecha_dt.weekday()]

        horarios_dia = self.horario_dao.buscar_por_restaurante_dia(
            int(id_restaurante), dia_semana
        )
        if not horarios_dia:
            raise ValueError("El restaurante no tiene horario habilitado para ese dia")

        dentro_de_horario = any(
            h["hora_inicio"] <= hora_inicio and hora_fin <= h["hora_fin"]
            for h in horarios_dia
        )
        if not dentro_de_horario:
            raise ValueError("La reserva esta fuera del horario del restaurante")

        if self.disponibilidad_dao.tiene_conflicto_horario(
            id_mesa=int(id_mesa),
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            excluir_id_disponibilidad=excluir_id_disponibilidad,
        ):
            raise ValueError("La mesa ya esta reservada en ese horario")

        if int(num_personas) > int(mesa["capacidad"]):
            raise ValueError("La cantidad de personas supera la capacidad de la mesa")

    def crear_reserva(
        self,
        id_cliente,
        id_restaurante,
        id_mesa,
        fecha,
        hora_inicio,
        hora_fin,
        num_personas,
    ):
        self._validar_reglas_reserva(
            id_restaurante=id_restaurante,
            id_mesa=id_mesa,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            num_personas=num_personas,
        )

        id_disponibilidad = self.disponibilidad_dao.crear_si_no_existe(
            {
                "id_mesa": id_mesa,
                "fecha": fecha,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "estado": "disponible",
            }
        )

        bloque = self.disponibilidad_dao.buscar_por_id(id_disponibilidad)
        if bloque["estado"] != "disponible":
            raise ValueError("Ese horario ya esta reservado")

        reserva = self.director.construir_reserva_estandar(
            self.builder,
            id_cliente=id_cliente,
            id_disponibilidad=id_disponibilidad,
            num_personas=num_personas,
        )

        id_reserva = self.reserva_dao.crear(
            {
                "id_cliente": reserva.id_cliente,
                "id_disponibilidad": reserva.id_disponibilidad,
                "estado": reserva.estado,
                "num_personas": reserva.num_personas,
            }
        )
        self.disponibilidad_dao.marcar_reservada(id_disponibilidad)
        return id_reserva

    def listar_reservas_cliente(self, id_cliente):
        return self.reserva_dao.buscar_detalladas_por_cliente(id_cliente)

    def actualizar_reserva(
        self,
        id_cliente,
        id_reserva,
        id_restaurante,
        id_mesa,
        fecha,
        hora_inicio,
        hora_fin,
        num_personas,
    ):
        reserva_actual = self.reserva_dao.buscar_detallada_cliente_por_id(
            id_reserva=id_reserva,
            id_cliente=id_cliente,
        )
        if not reserva_actual:
            raise ValueError("Reserva no encontrada")

        self._validar_reglas_reserva(
            id_restaurante=id_restaurante,
            id_mesa=id_mesa,
            fecha=fecha,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            num_personas=num_personas,
            excluir_id_disponibilidad=reserva_actual["id_disponibilidad"],
        )

        id_disponibilidad_nueva = self.disponibilidad_dao.crear_si_no_existe(
            {
                "id_mesa": id_mesa,
                "fecha": fecha,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
                "estado": "disponible",
            }
        )
        disponibilidad_nueva = self.disponibilidad_dao.buscar_por_id(id_disponibilidad_nueva)

        misma_disponibilidad = (
            int(id_disponibilidad_nueva) == int(reserva_actual["id_disponibilidad"])
        )
        if not misma_disponibilidad and disponibilidad_nueva["estado"] != "disponible":
            raise ValueError("Ese horario ya esta reservado")

        self.reserva_dao.actualizar(
            {
                "id_reserva": id_reserva,
                "id_disponibilidad": id_disponibilidad_nueva,
                "estado": reserva_actual["estado"],
                "num_personas": int(num_personas),
            }
        )

        self.disponibilidad_dao.marcar_reservada(id_disponibilidad_nueva)

        id_disponibilidad_anterior = int(reserva_actual["id_disponibilidad"])
        if id_disponibilidad_anterior != int(id_disponibilidad_nueva):
            if self.reserva_dao.contar_por_disponibilidad(id_disponibilidad_anterior) == 0:
                self.disponibilidad_dao.marcar_disponible(id_disponibilidad_anterior)

    def eliminar_reserva(self, id_cliente, id_reserva):
        reserva = self.reserva_dao.buscar_detallada_cliente_por_id(id_reserva, id_cliente)
        if not reserva:
            raise ValueError("Reserva no encontrada")

        id_disponibilidad = int(reserva["id_disponibilidad"])
        self.reserva_dao.eliminar(id_reserva)

        if self.reserva_dao.contar_por_disponibilidad(id_disponibilidad) == 0:
            self.disponibilidad_dao.marcar_disponible(id_disponibilidad)


class AdminService:
    def __init__(self, db):
        self.restaurante_dao = RestauranteDAO(db)
        self.mesa_dao = MesaDAO(db)
        self.horario_dao = HorarioDAO(db)
        self.reserva_dao = ReservaDAO(db)

    def crear_restaurante(self, nombre, direccion, telefono, descripcion):
        return self.restaurante_dao.crear(
            {
                "nombre": nombre,
                "direccion": direccion,
                "telefono": telefono,
                "descripcion": descripcion,
            }
        )

    def actualizar_restaurante(self, id_restaurante, nombre, direccion, telefono, descripcion):
        restaurante = self.restaurante_dao.buscar_por_id(id_restaurante)
        if not restaurante:
            raise ValueError("Restaurante no encontrado")

        self.restaurante_dao.actualizar(
            {
                "id_restaurante": id_restaurante,
                "nombre": nombre,
                "direccion": direccion,
                "telefono": telefono,
                "descripcion": descripcion,
            }
        )

    def eliminar_restaurante(self, id_restaurante):
        restaurante = self.restaurante_dao.buscar_por_id(id_restaurante)
        if not restaurante:
            raise ValueError("Restaurante no encontrado")
        self.restaurante_dao.eliminar(id_restaurante)

    def crear_mesa(self, id_restaurante, numero, capacidad, estado="activa"):
        return self.mesa_dao.crear(
            {
                "id_restaurante": id_restaurante,
                "numero": numero,
                "capacidad": capacidad,
                "estado": estado,
            }
        )

    def crear_horario(self, id_restaurante, dia_semana, hora_inicio, hora_fin):
        if hora_inicio >= hora_fin:
            raise ValueError("La hora de inicio debe ser menor que la hora de fin")

        return self.horario_dao.crear(
            {
                "id_restaurante": id_restaurante,
                "dia_semana": dia_semana,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
            }
        )

    def listar_horarios_por_restaurante(self, id_restaurante):
        if not id_restaurante:
            return []
        return self.horario_dao.buscar_por_restaurante(id_restaurante)

    def actualizar_horario(self, id_horario, dia_semana, hora_inicio, hora_fin):
        horario = self.horario_dao.buscar_por_id(id_horario)
        if not horario:
            raise ValueError("Horario no encontrado")
        if hora_inicio >= hora_fin:
            raise ValueError("La hora de inicio debe ser menor que la hora de fin")

        self.horario_dao.actualizar(
            {
                "id_horario": id_horario,
                "dia_semana": dia_semana,
                "hora_inicio": hora_inicio,
                "hora_fin": hora_fin,
            }
        )

    def eliminar_horario(self, id_horario):
        horario = self.horario_dao.buscar_por_id(id_horario)
        if not horario:
            raise ValueError("Horario no encontrado")
        self.horario_dao.eliminar(id_horario)

    def listar_reservas(self):
        return self.reserva_dao.listar_detalladas()

    def listar_restaurantes(self):
        return self.restaurante_dao.listar_todos()
