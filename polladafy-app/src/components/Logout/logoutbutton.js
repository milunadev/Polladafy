// src/components/Login/LoginButton.js
import { useNavigate } from 'react-router-dom';
import React from 'react';
import '../../css/logout.css'

const LogoutButton = () => {
    const navigate = useNavigate();
    const handleLogout = () => {
        // Borrar el token de sesión del almacenamiento local
        localStorage.removeItem('sessionToken');
      
        // Redirigir al usuario a la página de inicio de sesión
        console.log(localStorage.getItem('sessionToken'));
        navigate('/')
      };

  return (
    <div className='logoutContainer'>
      <button className='LogoutButton' onClick={handleLogout}>
      CERRAR SESION
    </button>
    </div>
    
  );
};

export {LogoutButton};