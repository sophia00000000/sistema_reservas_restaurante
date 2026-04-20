from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from presentacion.controllers.common import get_services

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    auth_service, _, _ = get_services()
    if request.method == "POST":
        try:
            auth_service.registrar_cliente(
                nombre=request.form["nombre"].strip(),
                email=request.form["email"].strip().lower(),
                password=request.form["password"],
                telefono=request.form.get("telefono", "").strip(),
                preferencias=request.form.get("preferencias", "").strip(),
            )
            flash("Registro exitoso. Inicia sesion", "ok")
            return redirect(url_for("auth.login"))
        except ValueError as exc:
            flash(str(exc), "error")
    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    auth_service, _, _ = get_services()
    if request.method == "POST":
        usuario = auth_service.login(
            email=request.form["email"].strip().lower(),
            password=request.form["password"],
        )
        if not usuario:
            flash("Credenciales invalidas", "error")
            return render_template("login.html")

        session["usuario"] = dict(usuario)
        flash("Bienvenido", "ok")
        return redirect(url_for("main.index"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("Sesion cerrada", "ok")
    return redirect(url_for("auth.login"))
