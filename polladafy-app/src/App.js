// src/App.js

import React from 'react';
import { AppUI } from './AppUI';
import { AppProvider } from './context/AppContext';



function App(){
  return(
    
      <AppProvider>
          <AppUI>

          </AppUI>
      </AppProvider>
  )
}

export default App;
