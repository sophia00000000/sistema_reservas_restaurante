from flask import Blueprint, redirect, session, url_for

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    usuario = session.get("usuario")
    if not usuario:
        return redirect(url_for("auth.login"))

    if usuario["rol"] == "admin":
        return redirect(url_for("admin.panel"))
    return redirect(url_for("cliente.reservas"))
