import React, { useContext } from 'react';
import { AppContext } from '../../context/AppContext';
import '../../css/dashboard.css'

const DownloadButton = () => {
    const {urlImage } = useContext(AppContext);
    return (
        <a className='downloadboton' href={urlImage} download>
            <button>🍺 Descargarme aquí 🍺</button>
        </a>
    );
};

export {DownloadButton};