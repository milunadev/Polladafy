// src/context/AppContext.js
import React from "react";
import { createContext, useState } from "react";

const AppContext = createContext();

//long_term (calculated from several years of data and including 
//all new data as it becomes available), medium_term (approximately last 6 months), 
//short_term (approximately last 4 weeks). Default: medium_term

function AppProvider({ children }){
    const [categoriaFiltro,setCategoriaFiltro] = useState('artista');
    const [periodoFiltro,setperiodoFiltro] = useState('medium_term');
  // Aquí puedes agregar funciones para manejar los datos, como actualizar el estado, hacer llamadas a la API, etc.

  return (
    <AppContext.Provider value={{ categoriaFiltro,setCategoriaFiltro,periodoFiltro,setperiodoFiltro }}>
      {children}
    </AppContext.Provider>
  );
};
export { AppProvider, AppContext}