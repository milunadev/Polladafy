import React, { useContext } from 'react';
import {AppContext} from '../../context/AppContext';

const FiltroCategorias = () => {
    const { categoriaFiltro, setCategoriaFiltro, setUrlImage } = useContext(AppContext);

    const handleCategoria = (categoria) => {
        return () => {
            if (categoriaFiltro !== categoria) {
                setUrlImage(null);
            }
            setCategoriaFiltro(categoria);
        };
    };

    return (
        <>
            <h4>CATEGORÍAS</h4>
            <div className='ButtonContainer'>
                <button 
                    className={`botonFiltro ${categoriaFiltro === 'artists' ? 'botonFiltroSeleccionado' : ''}`} 
                    onClick={handleCategoria('artists')}
                >
                    Artista
                </button>
                <button 
                    className={`botonFiltro ${categoriaFiltro === 'tracks' ? 'botonFiltroSeleccionado' : ''}`} 
                    onClick={handleCategoria('tracks')}
                >
                    Canciones
                </button>
                {/* Puedes agregar más botones aquí si es necesario */}
            </div>
        </>
    );
}

export {FiltroCategorias}