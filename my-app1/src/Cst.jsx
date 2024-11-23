// CST.jsx
import React, { useState } from 'react';

const Cst = () => {
  const [type, setType] = useState('INT'); // Défaut à INT
  const [numValues, setNumValues] = useState(0);

  const renderInputs = () => {
    let inputs = [];
    for (let i = 0; i < numValues; i++) {
      inputs.push(
        <input
          key={i}
          type={type === 'INT' ? 'number' : 'text'}
          step="any"
          placeholder={`Value ${i + 1}`}
          className="value-input"
        />
      );
    }
    return inputs;
  };

  return (
    <div className='main'>
      <div className='main-text cst-section'>
        <div><br></br> 
          <label className='titles'>Select your constant type: </label><br></br>
          <select id='cst-type' onChange={(e) => setType(e.target.value)} defaultValue={type}>
            <option value="INT">INT</option>
            <option value="FLOAT">FLOAT</option> 
          </select>  
        </div><br></br> 
        <div>
        <label className='titles'>
            Number of Values: 
            </label> <br></br>
          <input id='num-cst'
            type="number"
            min="0"
            onChange={(e) => setNumValues(parseInt(e.target.value, 10))}
            placeholder="Enter number of values"
          />
        </div>
        <div>{renderInputs()}</div>
      </div>
    </div>
  );
};

export default Cst;
