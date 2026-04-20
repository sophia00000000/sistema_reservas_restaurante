from datos.dao.base_dao import GenericDAO


class HorarioDAO(GenericDAO):
    def __init__(self, db):
        self.db = db

    def crear(self, horario):
        cur = self.db.execute(
            """
            INSERT INTO horario(id_restaurante, dia_semana, hora_inicio, hora_fin)
            VALUES (?, ?, ?, ?)
            """,
            (
                horario["id_restaurante"],
                horario["dia_semana"],
                horario["hora_inicio"],
                horario["hora_fin"],
            ),
        )
        self.db.commit()
        return cur.lastrowid

    def buscar_por_id(self, obj_id):
        return self.db.execute(
            "SELECT * FROM horario WHERE id_horario = ?", (obj_id,)
        ).fetchone()

    def actualizar(self, horario):
        self.db.execute(
            """
            UPDATE horario
            SET dia_semana = ?, hora_inicio = ?, hora_fin = ?
            WHERE id_horario = ?
            """,
            (
                horario["dia_semana"],
                horario["hora_inicio"],
                horario["hora_fin"],
                horario["id_horario"],
            ),
        )
        self.db.commit()

    def eliminar(self, obj_id):
        self.db.execute("DELETE FROM horario WHERE id_horario = ?", (obj_id,))
        self.db.commit()

    def listar_todos(self):
        return self.db.execute("SELECT * FROM horario").fetchall()

    def buscar_por_restaurante(self, id_restaurante):
        return self.db.execute(
            """
            SELECT * FROM horario
            WHERE id_restaurante = ?
            ORDER BY dia_semana, hora_inicio
            """,
            (id_restaurante,),
        ).fetchall()

    def buscar_por_restaurante_dia(self, id_restaurante, dia_semana):
        return self.db.execute(
            """
            SELECT * FROM horario
            WHERE id_restaurante = ? AND dia_semana = ?
            ORDER BY hora_inicio
            """,
            (id_restaurante, dia_semana),
        ).fetchall()
