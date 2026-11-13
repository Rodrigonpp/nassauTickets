from flask import Flask
from flask_smorest import Api
from flask_cors import CORS

from app.core.config import Config
from app.extensions import db, migrate


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

    from app import models  # noqa: F401

    api = Api(app)

    from app.routers.health import blp as health_blp
    from app.routers.senhas import blp as senhas_blp

    api.register_blueprint(health_blp)
    api.register_blueprint(senhas_blp)

    from app.core.exceptions import RegraNegocioError

    @app.errorhandler(RegraNegocioError)
    def tratar_regra_negocio(erro):
        return {"codigo": erro.status_code, "mensagem": erro.mensagem}, erro.status_code

    return app