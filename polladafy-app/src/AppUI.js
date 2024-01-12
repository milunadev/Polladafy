import React from "react";
import { BrowserRouter} from 'react-router-dom'
import {useRoutes} from 'react-router-dom'
import {LoginView} from './views/LoginView'
import { DashboardView } from "./views/DashboardView";
import { Header } from "./components/comunes/header";

const AppRoutes = ()=>{
    const routes = useRoutes([
        {path: "/", element: <LoginView/>},
        {path: "/dashboard", element: <DashboardView/>},
  
    ])
    return routes
}

function AppUI(){   
    return(
        <>
            <Header/>
            <AppRoutes/>
        </>
        
 
    )
}

export {AppUI};