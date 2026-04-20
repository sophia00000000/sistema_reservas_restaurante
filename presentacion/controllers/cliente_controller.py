from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from presentacion.controllers.common import get_services, login_required, role_required

cliente_bp = Blueprint("cliente", __name__, url_prefix="/cliente")


@cliente_bp.route("/reservas", methods=["GET", "POST"])
@login_required
@role_required("cliente")
def reservas():
    _, reserva_service, _ = get_services()
    restaurantes = reserva_service.listar_restaurantes()
    reservas_cliente = reserva_service.listar_reservas_cliente(
        session["usuario"]["id_cliente"]
    )
    mesas = []
    horarios = []

    selected_restaurante = request.args.get("restaurante")
    if request.method == "POST":
        selected_restaurante = request.form.get("id_restaurante") or request.form.get(
            "id_restaurante_selected"
        )

    if selected_restaurante:
        mesas = reserva_service.listar_mesas_por_restaurante(selected_restaurante)
        horarios = reserva_service.listar_horarios_por_restaurante(selected_restaurante)

    if request.method == "POST":
        accion = request.form.get("accion", "crear")
        try:
            if accion == "crear":
                reserva_service.crear_reserva(
                    id_cliente=session["usuario"]["id_cliente"],
                    id_restaurante=int(request.form["id_restaurante"]),
                    id_mesa=int(request.form["id_mesa"]),
                    fecha=request.form["fecha"],
                    hora_inicio=request.form["hora_inicio"],
                    hora_fin=request.form["hora_fin"],
                    num_personas=int(request.form["num_personas"]),
                )
                flash("Reserva creada con exito", "ok")
            elif accion == "actualizar":
                reserva_service.actualizar_reserva(
                    id_cliente=session["usuario"]["id_cliente"],
                    id_reserva=int(request.form["id_reserva"]),
                    id_restaurante=int(request.form["id_restaurante"]),
                    id_mesa=int(request.form["id_mesa"]),
                    fecha=request.form["fecha"],
                    hora_inicio=request.form["hora_inicio"],
                    hora_fin=request.form["hora_fin"],
                    num_personas=int(request.form["num_personas"]),
                )
                flash("Reserva actualizada", "ok")
            elif accion == "eliminar":
                reserva_service.eliminar_reserva(
                    id_cliente=session["usuario"]["id_cliente"],
                    id_reserva=int(request.form["id_reserva"]),
                )
                flash("Reserva eliminada", "ok")

            if selected_restaurante:
                return redirect(
                    url_for("cliente.reservas", restaurante=selected_restaurante)
                )
            return redirect(url_for("cliente.reservas"))
        except ValueError as exc:
            flash(str(exc), "error")

    return render_template(
        "cliente_reservas.html",
        restaurantes=restaurantes,
        mesas=mesas,
        horarios=horarios,
        selected_restaurante=selected_restaurante,
        reservas=reservas_cliente,
    )
