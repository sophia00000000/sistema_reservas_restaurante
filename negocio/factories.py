from abc import ABC, abstractmethod

from negocio.modelos import Administrador, Cliente


class UsuarioFactory(ABC):
    @abstractmethod
    def crear_usuario(self, data):
        raise NotImplementedError


class ClienteFactory(UsuarioFactory):
    def crear_usuario(self, data):
        return Cliente(
            id_usuario=data.get("id_usuario"),
            nombre=data["nombre"],
            email=data["email"],
            password=data["password"],
            rol="cliente",
            telefono=data.get("telefono", ""),
            estado=data.get("estado", "activo"),
            fecha_registro=data.get("fecha_registro"),
            preferencias=data.get("preferencias", ""),
        )


class AdminFactory(UsuarioFactory):
    def crear_usuario(self, data):
        return Administrador(
            id_usuario=data.get("id_usuario"),
            nombre=data["nombre"],
            email=data["email"],
            password=data["password"],
            rol="admin",
            cargo=data.get("cargo", "Administrador"),
            telefono=data.get("telefono", ""),
            fecha_contratacion=data.get("fecha_contratacion"),
            estado=data.get("estado", "activo"),
            salario=float(data.get("salario", 0)),
        )
