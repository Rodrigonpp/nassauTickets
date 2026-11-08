import enum


class Perfil(str, enum.Enum):
    ATENDENTE = "ATENDENTE"
    GESTOR = "GESTOR"


class StatusGuiche(str, enum.Enum):
    DISPONIVEL = "DISPONIVEL"
    OCUPADO = "OCUPADO"
    INATIVO = "INATIVO"


class TipoSenha(str, enum.Enum):
    SP = "SP"  # Prioritária
    SG = "SG"  # Geral
    SE = "SE"  # Retirada de exames


class StatusSenha(str, enum.Enum):
    EMITIDA = "EMITIDA"
    AGUARDANDO = "AGUARDANDO"
    CHAMADA = "CHAMADA"
    CHAMADA_NOVAMENTE = "CHAMADA_NOVAMENTE"
    EM_ATENDIMENTO = "EM_ATENDIMENTO"
    ATENDIDA = "ATENDIDA"
    NAO_COMPARECEU = "NAO_COMPARECEU"