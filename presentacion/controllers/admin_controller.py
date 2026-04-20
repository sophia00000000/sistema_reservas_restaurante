from flask import Blueprint, flash, redirect, render_template, request, url_for

from presentacion.controllers.common import get_services, login_required, role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/panel", methods=["GET", "POST"])
@login_required
@role_required("admin")
def panel():
    _, _, admin_service = get_services()
    selected_restaurante = request.args.get("restaurante")

    if request.method == "POST":
        accion = request.form.get("accion")
        selected_restaurante = request.form.get("id_restaurante_selected")
        try:
            if accion == "crear_restaurante":
                admin_service.crear_restaurante(
                    nombre=request.form["nombre"].strip(),
                    direccion=request.form["direccion"].strip(),
                    telefono=request.form.get("telefono", "").strip(),
                    descripcion=request.form.get("descripcion", "").strip(),
                )
                flash("Restaurante creado", "ok")
            elif accion == "actualizar_restaurante":
                admin_service.actualizar_restaurante(
                    id_restaurante=int(request.form["id_restaurante"]),
                    nombre=request.form["nombre"].strip(),
                    direccion=request.form["direccion"].strip(),
                    telefono=request.form.get("telefono", "").strip(),
                    descripcion=request.form.get("descripcion", "").strip(),
                )
                flash("Restaurante actualizado", "ok")
            elif accion == "eliminar_restaurante":
                admin_service.eliminar_restaurante(
                    id_restaurante=int(request.form["id_restaurante"])
                )
                flash("Restaurante eliminado", "ok")
            elif accion == "crear_mesa":
                admin_service.crear_mesa(
                    id_restaurante=int(request.form["id_restaurante"]),
                    numero=int(request.form["numero"]),
                    capacidad=int(request.form["capacidad"]),
                )
                flash("Mesa creada", "ok")
            elif accion == "crear_horario":
                admin_service.crear_horario(
                    id_restaurante=int(request.form["id_restaurante"]),
                    dia_semana=request.form["dia_semana"],
                    hora_inicio=request.form["hora_inicio"],
                    hora_fin=request.form["hora_fin"],
                )
                flash("Horario creado", "ok")
            elif accion == "actualizar_horario":
                admin_service.actualizar_horario(
                    id_horario=int(request.form["id_horario"]),
                    dia_semana=request.form["dia_semana"],
                    hora_inicio=request.form["hora_inicio"],
                    hora_fin=request.form["hora_fin"],
                )
                flash("Horario actualizado", "ok")
            elif accion == "eliminar_horario":
                admin_service.eliminar_horario(
                    id_horario=int(request.form["id_horario"])
                )
                flash("Horario eliminado", "ok")

            if selected_restaurante:
                return redirect(
                    url_for("admin.panel", restaurante=selected_restaurante)
                )
            return redirect(url_for("admin.panel"))
        except ValueError as exc:
            flash(str(exc), "error")

    restaurantes = admin_service.listar_restaurantes()
    reservas = admin_service.listar_reservas()
    horarios = admin_service.listar_horarios_por_restaurante(selected_restaurante)

    return render_template(
        "admin_panel.html",
        restaurantes=restaurantes,
        reservas=reservas,
        horarios=horarios,
        selected_restaurante=selected_restaurante,
    )
