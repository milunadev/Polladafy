import React, { useContext } from 'react';
import {FiltroCategorias} from '../components/Dashboard/categories'
import { FiltroTiempo } from '../components/Dashboard/times';
import '../css/dashboard.css'
import { useEffect } from 'react';
import { AppContext } from '../context/AppContext';
import { ImageDash } from '../components/Dashboard/imagendash';
import { LogoutButton } from '../components/Logout/logoutbutton';
import { DownloadButton } from '../components/Dashboard/downloadbutton';

const DashboardView = () => {
    //CONTEXTO
    const {urlImage, setUrlImage, categoriaFiltro, periodoFiltro, dataSpotify, setDataSpotify } = useContext(AppContext);
    const urlS3base = 'https://polladafybucket.s3.us-east-2.amazonaws.com/'

    //API ENDPOINTS
    const api_consulta_top = 'https://fh8qwcz15a.execute-api.us-east-2.amazonaws.com/request/trackandartist'

    
    //Usamos useEffect para recuperar el token de sesion de la URL y la
    //almacenamos en el local storage. Posible mejora: uso de cookies.
    useEffect(() => {
        const queryParams = new URLSearchParams(window.location.search);
        const sessionToken = queryParams.get('session_token');
        const username = queryParams.get('username');
        console.log('USER',username)
        const fetchData = async () => {
            try {
                console.log('CONSULTANDO API')
                const response = await fetch(`${api_consulta_top}?categoria=${categoriaFiltro}&periodo=${periodoFiltro}`, {
                    method: 'GET',
                    headers: {
                        'Session-Token': sessionToken,
                        'Username':username,
                        'Content-Type': 'application/json'
                    }
                });
                
                if (!response.ok) {
                    console.log(response)
                    throw new Error('Error al realizar la solicitud');
                }

                const data = await response.json();
                console.log(data)
                return data
                
            } catch (error) {
                console.error('Error:', error);
            }
        };

        if (sessionToken) {
            localStorage.setItem('sessionToken', sessionToken);
            //window.history.replaceState(null, null, window.location.pathname);
        
            fetchData()
            .then((data) => {
                setDataSpotify(data);
                console.log('data de spoti', data);

                // Verificar si data contiene s3_key directamente o dentro de body
                const s3Key = data?.s3_key || data?.body?.s3_key;
                if (s3Key) { 
                    setUrlImage(urlS3base + s3Key);
                    console.log('Seteando URLIMAGE');
                }
                return data;  // Devolver 'data' para el siguiente 'then'
            })
            .catch((error) => {
                console.error("Error fetching data: ", error);
            });
        }
      }, [categoriaFiltro, periodoFiltro]);

    

    //logs
    console.log(categoriaFiltro)
    console.log(periodoFiltro)
    console.log(dataSpotify)

    return(
        <>
        
            <div className='MainDashboardContainer'>
                <div className='DashboardElementContainer'>
                    <ImageDash/>
                    <DownloadButton/>
                    {/* <img id='ImageDash' src='https://portal.andina.pe/EDPfotografia/Thumbnail/2015/01/30/000279770W.jpg'></img> */}
                </div>
                <div id='FiltrosContainer'>
                    <h1 id='FiltrosTitle'>PERSONALIZA TU POLLADA</h1>
                    <FiltroCategorias/>
                    <FiltroTiempo/>
                    <p></p>
                </div>
                
            </div>
            <LogoutButton/>
        </>
    );
}

export {DashboardView}