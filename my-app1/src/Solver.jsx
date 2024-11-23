import React, { useState } from 'react';

function Solver({ timeout, algo, solver }) {
  const [result, setResult] = useState('RESULT');
  const [isLoading, setIsLoading] = useState(false); // Nouvelle variable d'état pour le loader

  const solve = async () => {
    setIsLoading(true); // Afficher le loader avant de faire la requête
    setResult(''); // Réinitialiser le résultat

    try {
      const newResponse = await fetch('http://127.0.0.1:5000/synth');

      if (newResponse.ok) {
        const newData = await newResponse.json();
        setResult(newData);
        console.log("synth_success");
         await new Promise(resolve => setTimeout(resolve, 1000));
      } else {
        console.log("SYNTH FAILED");
      }
    } catch (error) {
      console.error('Error:', error);
    }

    setIsLoading(false); // Cacher le loader après avoir reçu la réponse
  };

  return (
    <section className='solver'>
      <button onClick={solve} className="main-btn">Solve</button>
      {isLoading ? ( // Afficher le loader si isLoading est vrai
        <div className="loader"></div>
      ) : (
        <input type="text" id="result" placeholder={result} value={result} readOnly />
      )}
    </section>
  );
}

export default Solver;
