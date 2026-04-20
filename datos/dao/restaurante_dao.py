from datos.dao.base_dao import GenericDAO


class RestauranteDAO(GenericDAO):
    def __init__(self, db):
        self.db = db

    def crear(self, restaurante):
        cur = self.db.execute(
            """
            INSERT INTO restaurante(nombre, direccion, telefono, descripcion)
            VALUES (?, ?, ?, ?)
            """,
            (
                restaurante["nombre"],
                restaurante["direccion"],
                restaurante.get("telefono", ""),
                restaurante.get("descripcion", ""),
            ),
        )
        self.db.commit()
        return cur.lastrowid

    def buscar_por_id(self, obj_id):
        return self.db.execute(
            "SELECT * FROM restaurante WHERE id_restaurante = ?", (obj_id,)
        ).fetchone()

    def actualizar(self, restaurante):
        self.db.execute(
            """
            UPDATE restaurante
            SET nombre = ?, direccion = ?, telefono = ?, descripcion = ?
            WHERE id_restaurante = ?
            """,
            (
                restaurante["nombre"],
                restaurante["direccion"],
                restaurante["telefono"],
                restaurante["descripcion"],
                restaurante["id_restaurante"],
            ),
        )
        self.db.commit()

    def eliminar(self, obj_id):
        self.db.execute("DELETE FROM restaurante WHERE id_restaurante = ?", (obj_id,))
        self.db.commit()

    def listar_todos(self):
        return self.db.execute("SELECT * FROM restaurante ORDER BY nombre").fetchall()
