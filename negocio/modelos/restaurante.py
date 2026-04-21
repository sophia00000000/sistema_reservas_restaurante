from dataclasses import dataclass


@dataclass
class Restaurante:
    id_restaurante: int | None
    nombre: str
    direccion: str
    telefono: str = ""
    descripcion: str = ""
