from abc import ABC, abstractmethod


class GenericDAO(ABC):
    @abstractmethod
    def crear(self, obj):
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, obj_id):
        raise NotImplementedError

    @abstractmethod
    def actualizar(self, obj):
        raise NotImplementedError

    @abstractmethod
    def eliminar(self, obj_id):
        raise NotImplementedError

    @abstractmethod
    def listar_todos(self):
        raise NotImplementedError
