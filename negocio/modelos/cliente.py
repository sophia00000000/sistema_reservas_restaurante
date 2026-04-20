from dataclasses import dataclass

from negocio.modelos.usuario import Usuario


@dataclass
class Cliente(Usuario):
    telefono: str = ""
    estado: str = "activo"
    fecha_registro: str | None = None
    preferencias: str = ""
