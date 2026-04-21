from flask import Flask
from presentacion.controllers.admin_controller import admin_bp
from presentacion.controllers.auth_controller import auth_bp
from presentacion.controllers.cliente_controller import cliente_bp
from presentacion.controllers.main_controller import main_bp

app = Flask(
    __name__,
    template_folder="presentacion/templates",
    static_folder="presentacion/static",
)
# donde está la DB
app.config["SECRET_KEY"] = "dev-key-reservas"

app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(cliente_bp)
app.register_blueprint(admin_bp)


if __name__ == "__main__":
    app.run(debug=True)
