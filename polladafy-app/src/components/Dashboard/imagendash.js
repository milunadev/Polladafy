import React, { useContext } from 'react';
import { AppContext } from '../../context/AppContext';
import '../../css/dashboard.css';

const ImageDash = () => {
    const { urlImage } = useContext(AppContext);

    return (
        <div className='ImageDashboardContainer'>
            {!urlImage ? (
                <img 
                    id='ImageLoading' 
                    alt='Cargando...' 
                    src='https://polladafybucket.s3.us-east-2.amazonaws.com/pilsen.png'
                    className="loading-image"
                />
            ) : (
                <img id='ImageDash' src={urlImage} alt="Imagen Final" />
            )}
        </div>
    );
};

export { ImageDash };
