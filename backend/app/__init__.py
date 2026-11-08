from flask import Flask
from flask_smorest import Api

from app.core.config import Config
from app.extensions import db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    
    from app import models  # noqa: F401
    
    api = Api(app)

    from app.routers.health import blp as health_blp
    api.register_blueprint(health_blp)

    from app.core.exceptions import RegraNegocioError

    @app.errorhandler(RegraNegocioError)
    def tratar_regra_negocio(erro):
        return {"codigo": erro.status_code, "mensagem": erro.mensagem}, erro.status_code

    return app