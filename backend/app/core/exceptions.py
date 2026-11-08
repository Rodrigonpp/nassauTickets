class RegraNegocioError(Exception):
    """Erro de regra de negócio. Vira resposta HTTP padronizada na API."""

    status_code = 400

    def __init__(self, mensagem: str):
        super().__init__(mensagem)
        self.mensagem = mensagem


class TransicaoInvalidaError(RegraNegocioError):
    status_code = 409

class ForaDoExpedienteError(RegraNegocioError):
    status_code = 403