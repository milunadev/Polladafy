import React, { useContext } from 'react';
import {AppContext} from '../../context/AppContext';

const FiltroTiempo = () => {
    const { categoriaPeriodo, setCategoriaPeriodo } = useContext(AppContext);
    //Funciones para manejar los botones de Periodo
    const handlePeriodo = (categoria) => {
        return () => setCategoriaPeriodo(categoria);
    };

//long_term (calculated from several years of data and including 
//all new data as it becomes available), medium_term (approximately last 6 months), 
//short_term (approximately last 4 weeks). Default: medium_term

    return(
        <>
            <h4>PERIODO DE TIEMPO</h4>
            <div className='ButtonContainer'>
                <button className='botonFiltro' onClick={handlePeriodo('short_term')}>Ultimo Mes</button>
                <button className='botonFiltro' onClick={handlePeriodo('medium_term')}>6 meses</button>
                <button className='botonFiltro' onClick={handlePeriodo('long_term')}>TODO EL TIEMPO</button>
            </div>
        </>  
    );
}

export {FiltroTiempo}