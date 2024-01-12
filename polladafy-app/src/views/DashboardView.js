import React, { useContext } from 'react';
import {FiltroCategorias} from '../components/Dashboard/categories'
import { FiltroTiempo } from '../components/Dashboard/times';
import '../css/dashboard.css'
import { useEffect } from 'react';
import { AppContext } from '../context/AppContext';

const DashboardView = () => {

    const { categoriaFiltro, periodoFiltro } = useContext(AppContext);

    //Usamos useEffect para recuperar el token de sesion de la URL y la
    //almacenamos en el local storage. Posible mejora: uso de cookies.
    useEffect(() => {
        const queryParams = new URLSearchParams(window.location.search);
        const sessionToken = queryParams.get('session_token');
        
        if (sessionToken) {
            console.log(sessionToken)
          // Guardar el token de sesión en una cookie o almacenamiento local
          //document.cookie = `sessionToken=${sessionToken}; HttpOnly; Secure; Path=/;`;
          // O
          localStorage.setItem('sessionToken', sessionToken);
            
          // Opcional: Limpiar la URL quitando el parámetro session_token
          //window.history.replaceState(null, null, window.location.pathname);
        }
      }, []);
    
    const sessionToken = localStorage.getItem('sessionToken')
    

    //logs
    console.log(categoriaFiltro)
    console.log(periodoFiltro)
      
    return(
        <>
        
            <div className='MainDashboardContainer'>
                <div id='FiltrosContainer'>
                    <h1 id='FiltrosTitle'>PERSONALIZA TU POLLADA</h1>
                    <FiltroCategorias/>
                    <FiltroTiempo/>
                </div>
                <div>
                    <img id='ImageDash' src='https://portal.andina.pe/EDPfotografia/Thumbnail/2015/01/30/000279770W.jpg'></img>
                </div>
            </div>
        </>
    );
}

export {DashboardView}