// src/views/LoginView.js

import React from 'react';
import {LoginButton} from '../components/Login/LoginButton';
import '../css/login.css'

const LoginView = () => {
  return (
    <div className='LoginMainContainer h-full w-full flex items-center'>
      <span className='spanLogin'>
        <p>Genera la invitacion a tu pollada bailable! 🍺🍺🍺 </p>
        <ul>
          <li>- Imprime tu tracklist</li>
          <li>- Imprime a tus artistas invitados.</li>

        </ul>
      </span>
      
      <section className='LoginMainImageContainer'>
        <img id='LoginMainImage' src='https://portal.andina.pe/EDPfotografia/Thumbnail/2015/01/30/000279770W.jpg'></img>
      </section>
      <section className='LoginMainImageContainer'>
        <LoginButton />
      </section>
      
    </div>
  );
};

export {LoginView};
