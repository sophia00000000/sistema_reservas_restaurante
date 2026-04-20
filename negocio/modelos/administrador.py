from dataclasses import dataclass

from negocio.modelos.usuario import Usuario


@dataclass
class Administrador(Usuario):
    cargo: str = "Administrador"
    telefono: str = ""
    fecha_contratacion: str | None = None
    estado: str = "activo"
    salario: float = 0
