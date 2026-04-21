from dataclasses import dataclass


@dataclass
class Mesa:
    id_mesa: int | None
    id_restaurante: int
    numero: int
    capacidad: int
    estado: str = "activa"
