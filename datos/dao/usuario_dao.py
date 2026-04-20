from datos.dao.base_dao import GenericDAO


class UsuarioDAO(GenericDAO):
    def __init__(self, db):
        self.db = db

    def crear(self, usuario):
        cur = self.db.execute(
            """
            INSERT INTO usuario(nombre, email, password, rol)
            VALUES (?, ?, ?, ?)
            """,
            (usuario["nombre"], usuario["email"], usuario["password"], usuario["rol"]),
        )
        self.db.commit()
        return cur.lastrowid

    def buscar_por_id(self, obj_id):
        return self.db.execute(
            "SELECT * FROM usuario WHERE id_usuario = ?", (obj_id,)
        ).fetchone()

    def buscar_por_email(self, email):
        return self.db.execute(
            "SELECT * FROM usuario WHERE email = ?", (email,)
        ).fetchone()

    def actualizar(self, usuario):
        self.db.execute(
            """
            UPDATE usuario
            SET nombre = ?, email = ?, password = ?
            WHERE id_usuario = ?
            """,
            (
                usuario["nombre"],
                usuario["email"],
                usuario["password"],
                usuario["id_usuario"],
            ),
        )
        self.db.commit()

    def eliminar(self, obj_id):
        self.db.execute("DELETE FROM usuario WHERE id_usuario = ?", (obj_id,))
        self.db.commit()

    def listar_todos(self):
        return self.db.execute("SELECT * FROM usuario").fetchall()
