from datos.dao.base_dao import GenericDAO


class AdministradorDAO(GenericDAO):
    def __init__(self, db):
        self.db = db

    def crear(self, admin):
        cur = self.db.execute(
            """
            INSERT INTO administrador(id_usuario, cargo, telefono, fecha_contratacion, estado, salario)
            VALUES (?, ?, ?, DATE('now'), ?, ?)
            """,
            (
                admin["id_usuario"],
                admin.get("cargo", "Admin"),
                admin.get("telefono", ""),
                admin.get("estado", "activo"),
                admin.get("salario", 0),
            ),
        )
        self.db.commit()
        return cur.lastrowid

    def buscar_por_id(self, obj_id):
        return self.db.execute(
            "SELECT * FROM administrador WHERE id_admin = ?", (obj_id,)
        ).fetchone()

    def buscar_por_usuario(self, id_usuario):
        return self.db.execute(
            "SELECT * FROM administrador WHERE id_usuario = ?", (id_usuario,)
        ).fetchone()

    def actualizar(self, admin):
        self.db.execute(
            """
            UPDATE administrador
            SET cargo = ?, telefono = ?, estado = ?, salario = ?
            WHERE id_admin = ?
            """,
            (
                admin["cargo"],
                admin["telefono"],
                admin["estado"],
                admin["salario"],
                admin["id_admin"],
            ),
        )
        self.db.commit()

    def eliminar(self, obj_id):
        self.db.execute("DELETE FROM administrador WHERE id_admin = ?", (obj_id,))
        self.db.commit()

    def listar_todos(self):
        return self.db.execute("SELECT * FROM administrador").fetchall()
