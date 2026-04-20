from datos.dao.base_dao import GenericDAO


class ClienteDAO(GenericDAO):
    def __init__(self, db):
        self.db = db

    def crear(self, cliente):
        cur = self.db.execute(
            """
            INSERT INTO cliente(id_usuario, telefono, estado, fecha_registro, preferencias)
            VALUES (?, ?, ?, DATE('now'), ?)
            """,
            (
                cliente["id_usuario"],
                cliente.get("telefono", ""),
                cliente.get("estado", "activo"),
                cliente.get("preferencias", ""),
            ),
        )
        self.db.commit()
        return cur.lastrowid

    def buscar_por_id(self, obj_id):
        return self.db.execute(
            "SELECT * FROM cliente WHERE id_cliente = ?", (obj_id,)
        ).fetchone()

    def buscar_por_usuario(self, id_usuario):
        return self.db.execute(
            "SELECT * FROM cliente WHERE id_usuario = ?", (id_usuario,)
        ).fetchone()

    def actualizar(self, cliente):
        self.db.execute(
            """
            UPDATE cliente
            SET telefono = ?, estado = ?, preferencias = ?
            WHERE id_cliente = ?
            """,
            (
                cliente["telefono"],
                cliente["estado"],
                cliente["preferencias"],
                cliente["id_cliente"],
            ),
        )
        self.db.commit()

    def eliminar(self, obj_id):
        self.db.execute("DELETE FROM cliente WHERE id_cliente = ?", (obj_id,))
        self.db.commit()

    def listar_todos(self):
        return self.db.execute("SELECT * FROM cliente").fetchall()
