from datos.dao.base_dao import GenericDAO


class MesaDAO(GenericDAO):
    def __init__(self, db):
        self.db = db

    def crear(self, mesa):
        cur = self.db.execute(
            """
            INSERT INTO mesa(id_restaurante, numero, capacidad, estado)
            VALUES (?, ?, ?, ?)
            """,
            (
                mesa["id_restaurante"],
                mesa["numero"],
                mesa["capacidad"],
                mesa.get("estado", "activa"),
            ),
        )
        self.db.commit()
        return cur.lastrowid

    def buscar_por_id(self, obj_id):
        return self.db.execute("SELECT * FROM mesa WHERE id_mesa = ?", (obj_id,)).fetchone()

    def actualizar(self, mesa):
        self.db.execute(
            """
            UPDATE mesa
            SET numero = ?, capacidad = ?, estado = ?
            WHERE id_mesa = ?
            """,
            (mesa["numero"], mesa["capacidad"], mesa["estado"], mesa["id_mesa"]),
        )
        self.db.commit()

    def eliminar(self, obj_id):
        self.db.execute("DELETE FROM mesa WHERE id_mesa = ?", (obj_id,))
        self.db.commit()

    def listar_todos(self):
        return self.db.execute("SELECT * FROM mesa").fetchall()

    def buscar_por_restaurante(self, id_restaurante):
        return self.db.execute(
            "SELECT * FROM mesa WHERE id_restaurante = ? ORDER BY numero", (id_restaurante,)
        ).fetchall()
