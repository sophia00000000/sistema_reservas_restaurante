from dataclasses import dataclass


@dataclass
class Disponibilidad:
    id_disponibilidad: int | None
    id_mesa: int
    fecha: str
    hora_inicio: str
    hora_fin: str
    estado: str = "disponible"
