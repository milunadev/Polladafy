// src/components/Login/LoginButton.js

import React from 'react';
import '../../css/login.css'

const LoginButton = () => {
  const handleLogin = () => {
    fetch('https://fh8qwcz15a.execute-api.us-east-2.amazonaws.com/auth/spotify')
      .then(response => response.json())
      .then(data => {
        window.location.href = data.authUrl; // Suponiendo que 'authUrl' es la URL de autenticación de Spotify
      })
      .catch(error => console.error('Error:', error));
  };

  return (
    <button className='LoginButton' onClick={handleLogin}>
      Iniciar Sesión con Spotify
    </button>
  );
};

export {LoginButton};