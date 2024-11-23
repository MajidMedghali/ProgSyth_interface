import React, { useState, useEffect } from 'react';
import Solver from './Solver';
import ExecutionForm from './Execution';
import InputBox from './inputBox';
import './Examples.css';


const Home = () => {
  const [timeout, setTimout] = useState('');
  const [algo, setAlgo] = useState('');
  const [solver, setSolver] = useState('');
  const [showInputBox, setShowInputBox] = useState(false);
  const [numParam, setNumParam] = useState(-1);
  

  const handleChange = async(index, expression) =>{
    try {
      const response = await fetch(`http://127.0.0.1:5000/get_addons/${index}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ expression })
      });
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const toggleInputBox = () => {
    setShowInputBox(!showInputBox);
  };
 const getParam = async () => {
  try {
    const response = await fetch('http://127.0.0.1:5000/get_number_of_parameters');
    if (response.ok) {
      const data = await response.json();
      setNumParam(data.num_param);
      console.log(data.numParam); // Update the state with the fetched value
    } else {
      console.error('Failed to fetch number of parameters');
    }
  } catch (error) {
    console.error('Error:', error);
  }
}
  useEffect(() => {
    getParam(); // Fetch parameters when component mounts or whenever there's a change
  }, []);
 
  return (
    <section className='main'>
      <div className='parameters'>
        <label className='titles'>Choose your parameters:</label><br />
        <select id="TIMEOUT" className='parameter' onChange={(e) => handleChange(3,e.target.value)}>
          <option value="" disabled selected>TIMEOUT</option>
          <option value="1">1 min</option>
          <option value="2">2 min</option>
          <option value="3">3 min</option>
          <option value="4">4 min</option>
          <option value="5">5 min</option>
        </select>

        <select id="ALGO" className='parameter' onChange={(e) => handleChange(4,e.target.value)}>
          <option value="" disabled selected>Search Algorithm</option>
          <option value="heap_search">heap_search</option>
          <option value="beap_search">beap_search</option>
          <option value="bucket_search">bucket_search</option>
          <option value="bee_search">bee_search</option>
        </select>

        <select id="SOLVER" className='parameter' onChange={(e) => handleChange(5,e.target.value)}>
          <option value="" disabled selected>Solver</option>
          <option value="naive">naive</option>
          <option value="cutoff">cutoff</option>
          <option value="restart">restart</option>
          <option value="PBEsolver">PBEsolver</option>
        </select>
      </div>
      
      <Solver timeout={timeout} algo={algo} solver={solver} />
      <div className="input-box">
      {!showInputBox && (
        <button className="button-evaluate"  onClick={toggleInputBox} >Evaluate</button>
      )}

      {showInputBox && (
        <div>
          <button onClick={toggleInputBox}>Remove Evaluation</button>
          {/* <div>
          ${numParam}
          </div> */}
          <InputBox numberOfParameters={numParam} boxStyle={1}  />
        </div>

      )}
      </div>
    </section>
  );
};

export default Home;
