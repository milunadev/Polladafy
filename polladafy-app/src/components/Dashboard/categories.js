import React, { useContext } from 'react';
import {AppContext} from '../../context/AppContext';

const FiltroCategorias = () => {
    const { categoriaFiltro, setCategoriaFiltro } = useContext(AppContext);
    
    //Funciones para manejar los botones de Categoria
    const handleCategoria = (categoria) => {
        return () => setCategoriaFiltro(categoria);
    };

    return(
        <>
            <h4>CATEGORIAS</h4>
            <div className='ButtonContainer'>
                <button className='botonFiltro' onClick={handleCategoria('artist')}>Artista</button>
                <button className='botonFiltro' onClick={handleCategoria('canciones')}>Canciones</button>
                <button className='botonFiltro' onClick={handleCategoria('genero')}>Genero</button>
            </div>
        </>   
    );
}

export {FiltroCategorias}