import retirada_exames from "../../assets/retirada_exames.svg";
import atendimento_geral from "../../assets/user.svg";
import atendimento_prioritario from "../../assets/atendimento_prioritario.svg";
import seta_azul from "../../assets/seta_azul.svg";
import seta_laranja from "../../assets/seta_laranja.svg";
import seta_roxa from "../../assets/seta_roxa.svg";

const servicos = [
  {
    id: "prioritario",
    img: atendimento_prioritario,
    title: "Atendimento prioritário",
    description: "Pessoas com prioridade prevista em lei",
    type: "SP",
    seta: seta_laranja,
  },
  {
    id: "geral",
    img: atendimento_geral,
    title: "Atendimento geral",
    description: "Atendimento clínico e coleta, sem prioridade",
    type: "SG",
    seta: seta_azul,
  },
  {
    id: "exames",
    img: retirada_exames,
    title: "Retirada de exames",
    description: "Entrega de resultados e documentos",
    type: "SE",
    seta: seta_roxa,
  },
];

export default servicos;
