from dataclasses import dataclass


@dataclass
class Usuario:
    id_usuario: int | None
    nombre: str
    email: str
    password: str
    rol: str
