from datos.dao.base_dao import GenericDAO


class ReservaDAO(GenericDAO):
    def __init__(self, db):
        self.db = db

    def crear(self, reserva):
        cur = self.db.execute(
            """
            INSERT INTO reserva(id_cliente, id_disponibilidad, estado, num_personas)
            VALUES (?, ?, ?, ?)
            """,
            (
                reserva["id_cliente"],
                reserva["id_disponibilidad"],
                reserva.get("estado", "pendiente"),
                reserva["num_personas"],
            ),
        )
        self.db.commit()
        return cur.lastrowid

    def buscar_por_id(self, obj_id):
        return self.db.execute(
            "SELECT * FROM reserva WHERE id_reserva = ?", (obj_id,)
        ).fetchone()

    def actualizar(self, reserva):
        self.db.execute(
            """
            UPDATE reserva
            SET id_disponibilidad = ?, estado = ?, num_personas = ?
            WHERE id_reserva = ?
            """,
            (
                reserva["id_disponibilidad"],
                reserva["estado"],
                reserva["num_personas"],
                reserva["id_reserva"],
            ),
        )
        self.db.commit()

    def eliminar(self, obj_id):
        self.db.execute("DELETE FROM reserva WHERE id_reserva = ?", (obj_id,))
        self.db.commit()

    def listar_todos(self):
        return self.db.execute("SELECT * FROM reserva").fetchall()

    def buscar_por_cliente(self, id_cliente):
        return self.db.execute(
            "SELECT * FROM reserva WHERE id_cliente = ? ORDER BY id_reserva DESC", (id_cliente,)
        ).fetchall()

    def buscar_detalladas_por_cliente(self, id_cliente):
        return self.db.execute(
            """
            SELECT r.id_reserva,
                   r.id_disponibilidad,
                   r.estado,
                   r.num_personas,
                   d.id_mesa,
                   d.fecha,
                   d.hora_inicio,
                   d.hora_fin,
                   m.numero AS mesa_numero,
                   m.capacidad AS mesa_capacidad,
                   re.id_restaurante,
                   re.nombre AS restaurante_nombre
            FROM reserva r
            JOIN disponibilidad d ON d.id_disponibilidad = r.id_disponibilidad
            JOIN mesa m ON m.id_mesa = d.id_mesa
            JOIN restaurante re ON re.id_restaurante = m.id_restaurante
            WHERE r.id_cliente = ?
            ORDER BY d.fecha DESC, d.hora_inicio DESC
            """,
            (id_cliente,),
        ).fetchall()

    def buscar_detallada_cliente_por_id(self, id_reserva, id_cliente):
        return self.db.execute(
            """
            SELECT r.id_reserva,
                   r.id_disponibilidad,
                   r.estado,
                   r.num_personas,
                   d.id_mesa,
                   d.fecha,
                   d.hora_inicio,
                   d.hora_fin,
                   re.id_restaurante
            FROM reserva r
            JOIN disponibilidad d ON d.id_disponibilidad = r.id_disponibilidad
            JOIN mesa m ON m.id_mesa = d.id_mesa
            JOIN restaurante re ON re.id_restaurante = m.id_restaurante
            WHERE r.id_reserva = ? AND r.id_cliente = ?
            """,
            (id_reserva, id_cliente),
        ).fetchone()

    def contar_por_disponibilidad(self, id_disponibilidad):
        row = self.db.execute(
            "SELECT COUNT(*) AS total FROM reserva WHERE id_disponibilidad = ?",
            (id_disponibilidad,),
        ).fetchone()
        return int(row["total"]) if row else 0

    def listar_detalladas(self):
        return self.db.execute(
            """
            SELECT r.id_reserva,
                   r.estado,
                   r.num_personas,
                   d.fecha,
                   d.hora_inicio,
                   d.hora_fin,
                   m.numero AS mesa_numero,
                   re.nombre AS restaurante_nombre,
                   u.nombre AS cliente_nombre
            FROM reserva r
            JOIN cliente c ON c.id_cliente = r.id_cliente
            JOIN usuario u ON u.id_usuario = c.id_usuario
            JOIN disponibilidad d ON d.id_disponibilidad = r.id_disponibilidad
            JOIN mesa m ON m.id_mesa = d.id_mesa
            JOIN restaurante re ON re.id_restaurante = m.id_restaurante
            ORDER BY d.fecha DESC, d.hora_inicio DESC
            """
        ).fetchall()
