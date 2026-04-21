from negocio.modelos import Reserva


class ReservaBuilder:
    def __init__(self):
        self.reset()

    def reset(self):
        # Estado interno temporal del builder.
        self._data = {
            "id_reserva": None,
            "id_cliente": None,
            "id_disponibilidad": None,
            "estado": "pendiente",
            "num_personas": 1,
        }
        return self

    def set_cliente(self, id_cliente):
        self._data["id_cliente"] = id_cliente
        return self

    def set_disponibilidad(self, id_disponibilidad):
        self._data["id_disponibilidad"] = id_disponibilidad
        return self

    def set_estado(self, estado):
        self._data["estado"] = estado
        return self

    def set_num_personas(self, cantidad):
        self._data["num_personas"] = int(cantidad)
        return self

    def build(self):
        # Validaciones minimas antes de materializar la reserva.
        if not self._data["id_cliente"]:
            raise ValueError("La reserva requiere id_cliente")
        if not self._data["id_disponibilidad"]:
            raise ValueError("La reserva requiere id_disponibilidad")
        if self._data["num_personas"] <= 0:
            raise ValueError("num_personas debe ser mayor que 0")

        reserva = Reserva(**self._data)
        self.reset()
        return reserva


class ReservaDirector:
    def construir_reserva_estandar(
        self, builder, id_cliente, id_disponibilidad, num_personas
    ):
        # Receta estandar de construccion para nuevas reservas.
        return (
            builder.reset()
            .set_cliente(id_cliente)
            .set_disponibilidad(id_disponibilidad)
            .set_num_personas(num_personas)
            .set_estado("pendiente")
            .build()
        )
