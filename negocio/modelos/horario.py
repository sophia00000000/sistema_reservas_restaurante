from dataclasses import dataclass


@dataclass
class Horario:
    id_horario: int | None
    id_restaurante: int
    dia_semana: str
    hora_inicio: str
    hora_fin: str
