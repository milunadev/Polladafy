import React from 'react';
import '../../css/comunes.css'

const Header = () => {
    return (
      <div className='HeaderContainer'>
        <h1 className='HeaderTitle'>POLLADAFY </h1>
        <img className='HeaderLogo' src='https://mir-s3-cdn-cf.behance.net/project_modules/max_1200/97f10f18458481.562c9cd31da7d.png'></img>
        <p className='HeaderSubtitle'> Peruanizando Spotify!</p>
      </div>
    );
  };
  
  export {Header};