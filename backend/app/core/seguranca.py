from functools import wraps

from flask_jwt_extended import get_jwt, get_jwt_identity, verify_jwt_in_request

from app.core.exceptions import AcessoNegadoError


def usuario_atual_id() -> int:
    return int(get_jwt_identity())


def perfil_requerido(*perfis):
    """Exige token válido e um dos perfis informados."""
    def decorador(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            if get_jwt().get("perfil") not in perfis:
                raise AcessoNegadoError("Perfil sem permissão para esta ação.")
            return fn(*args, **kwargs)
        return wrapper
    return decorador