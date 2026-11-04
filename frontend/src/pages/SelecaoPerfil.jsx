import React from 'react'

const SelecaoPerfil = () => {
  return (
    <div>
      <h1 className='painel-title'>Selecione o perfil que deseja acessar:</h1>
      <div className="selecao-perfil">
        <a href="/atendente/login">Atendente</a>
        <a href="/painel">Painel</a>
        <a href="/totem">Totem</a>
      </div>
    </div>
  )
}

export default SelecaoPerfil