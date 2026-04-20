from dataclasses import dataclass


@dataclass
class Reserva:
    id_reserva: int | None
    id_cliente: int
    id_disponibilidad: int
    estado: str
    num_personas: int
