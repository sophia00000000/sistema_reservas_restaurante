from functools import wraps

from flask import flash, redirect, session, url_for

from datos.ConexionDB import ConexionDB
from negocio.services import AdminService, AuthService, ReservaService


def get_services():
    conexion = ConexionDB.get_instance()
    db = conexion.conectar()
    return AuthService(db), ReservaService(db), AdminService(db)


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "usuario" not in session:
            flash("Debes iniciar sesion", "error")
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)

    return wrapper


def role_required(role):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            usuario = session.get("usuario")
            if not usuario or usuario.get("rol") != role:
                flash("No tienes permisos para esta seccion", "error")
                return redirect(url_for("main.index"))
            return func(*args, **kwargs)

        return wrapper

    return decorator
