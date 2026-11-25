from flask import Flask
from flask_cors import CORS
from flask_smorest import Api

from app.core.config import Config
from app.extensions import db, jwt, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app, resources={r"/api/*": {"origins": [
        "http://localhost:5173",
        "http://localhost:4200",
        "http://localhost:3000",
    ]}})

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    from app import models  # noqa: F401

    api = Api(app)

    from app.routers.admin import blp as admin_blp
    from app.routers.atendimentos import blp as atendimentos_blp
    from app.routers.auth import blp as auth_blp
    from app.routers.health import blp as health_blp
    from app.routers.painel import blp as painel_blp
    from app.routers.relatorios import blp as relatorios_blp
    from app.routers.senhas import blp as senhas_blp

    api.register_blueprint(health_blp)
    api.register_blueprint(auth_blp)
    api.register_blueprint(senhas_blp)
    api.register_blueprint(atendimentos_blp)
    api.register_blueprint(painel_blp)
    api.register_blueprint(relatorios_blp)
    api.register_blueprint(admin_blp)

    from app.core.exceptions import RegraNegocioError

    @app.errorhandler(RegraNegocioError)
    def tratar_regra_negocio(erro):
        return {"codigo": erro.status_code, "mensagem": erro.mensagem}, erro.status_code

    return app