from flask_smorest import Blueprint, abort
from sqlalchemy import text

from app.extensions import db

blp = Blueprint(
    "health", __name__, url_prefix="/api/v1", description="Infraestrutura"
)


@blp.route("/health")
@blp.response(200)
def health():
    """Health check: confirma que a API e o banco estão respondendo."""
    try:
        db.session.execute(text("SELECT 1"))
    except Exception:
        abort(503, message="Banco de dados indisponível")
    return {"status": "ok", "database": "ok"}