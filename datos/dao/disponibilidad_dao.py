from datos.dao.base_dao import GenericDAO


class DisponibilidadDAO(GenericDAO):
    def __init__(self, db):
        self.db = db

    def crear(self, disponibilidad):
        cur = self.db.execute(
            """
            INSERT INTO disponibilidad(id_mesa, fecha, hora_inicio, hora_fin, estado)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                disponibilidad["id_mesa"],
                disponibilidad["fecha"],
                disponibilidad["hora_inicio"],
                disponibilidad["hora_fin"],
                disponibilidad.get("estado", "disponible"),
            ),
        )
        self.db.commit()
        return cur.lastrowid

    def buscar_por_id(self, obj_id):
        return self.db.execute(
            "SELECT * FROM disponibilidad WHERE id_disponibilidad = ?", (obj_id,)
        ).fetchone()

    def actualizar(self, disponibilidad):
        self.db.execute(
            """
            UPDATE disponibilidad
            SET fecha = ?, hora_inicio = ?, hora_fin = ?, estado = ?
            WHERE id_disponibilidad = ?
            """,
            (
                disponibilidad["fecha"],
                disponibilidad["hora_inicio"],
                disponibilidad["hora_fin"],
                disponibilidad["estado"],
                disponibilidad["id_disponibilidad"],
            ),
        )
        self.db.commit()

    def eliminar(self, obj_id):
        self.db.execute(
            "DELETE FROM disponibilidad WHERE id_disponibilidad = ?", (obj_id,)
        )
        self.db.commit()

    def listar_todos(self):
        return self.db.execute("SELECT * FROM disponibilidad").fetchall()

    def buscar_por_mesa_fecha(self, id_mesa, fecha):
        return self.db.execute(
            """
            SELECT * FROM disponibilidad
            WHERE id_mesa = ? AND fecha = ?
            ORDER BY hora_inicio
            """,
            (id_mesa, fecha),
        ).fetchall()

    def tiene_conflicto_horario(
        self,
        id_mesa,
        fecha,
        hora_inicio,
        hora_fin,
        excluir_id_disponibilidad=None,
    ):
        query = """
            SELECT 1
            FROM disponibilidad
            WHERE id_mesa = ?
              AND fecha = ?
              AND estado = 'reservada'
              AND NOT (? >= hora_fin OR ? <= hora_inicio)
        """
        params = [id_mesa, fecha, hora_inicio, hora_fin]

        if excluir_id_disponibilidad is not None:
            query += " AND id_disponibilidad <> ?"
            params.append(excluir_id_disponibilidad)

        query += " LIMIT 1"
        conflicto = self.db.execute(query, tuple(params)).fetchone()
        return conflicto is not None

    def crear_si_no_existe(self, data):
        existente = self.db.execute(
            """
            SELECT * FROM disponibilidad
            WHERE id_mesa = ? AND fecha = ? AND hora_inicio = ? AND hora_fin = ?
            """,
            (data["id_mesa"], data["fecha"], data["hora_inicio"], data["hora_fin"]),
        ).fetchone()
        if existente:
            return existente["id_disponibilidad"]
        return self.crear(data)

    def marcar_reservada(self, id_disponibilidad):
        self.db.execute(
            "UPDATE disponibilidad SET estado = 'reservada' WHERE id_disponibilidad = ?",
            (id_disponibilidad,),
        )
        self.db.commit()

    def marcar_disponible(self, id_disponibilidad):
        self.db.execute(
            "UPDATE disponibilidad SET estado = 'disponible' WHERE id_disponibilidad = ?",
            (id_disponibilidad,),
        )
        self.db.commit()
