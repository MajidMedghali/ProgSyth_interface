// MyContext.js

import React, { createContext, useState } from 'react';

// Créez un contexte
const MyContext = createContext();

// Créez un fournisseur de contexte pour fournir le contexte aux composants enfants
const MyContextProvider = ({ children }) => {
  const [data, setData] = useState(/* Votre valeur initiale ici */);

  return (
    <MyContext.Provider value={{ data, setData }}>
      {children}
    </MyContext.Provider>
  );
};

export { MyContext, MyContextProvider };
