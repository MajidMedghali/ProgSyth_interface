import React, { useState, useEffect } from 'react';
import './Examples.css';


const InputBox = ({ numberOfParameters, invalidExpression, setValidated, boxStyle }) => {
  const [inputs, setInputs] = useState([Array.from({ length: numberOfParameters }, () => '')]);
  const [currentRoute, setRoute] = useState('get_inputs');
  const [validationMessage, setValidationMessage] = useState('');

  useEffect(() => {
    setInputs([Array.from({ length: numberOfParameters + 1 }, () => '')]);
  }, [numberOfParameters]);

  const handleInputChange = (inputIndex, parameterIndex, value) => {
    const newInputs = [...inputs];
    newInputs[inputIndex][parameterIndex] = value;
    setInputs(newInputs);
  };

  const handleAddInput = () => {
    setInputs([...inputs, Array.from({ length: numberOfParameters + 1 }, () => '')]);
  };

  const handleRemoveInput = (inputIndex) => {
    const newInputs = [...inputs];
    newInputs.splice(inputIndex, 1);
    setInputs(newInputs);
  };

  const handleValidate = async () => {
    try {
      let path = "";
      if (boxStyle === 1) {
        path = "http://127.0.0.1:5000/eval";
      } else {
        path = "http://127.0.0.1:5000/get_inputs";
      }
      const response = await fetch(path, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ expression: inputs })
      });

      if (response.ok) {
        const data = await response.json();
        if (boxStyle === 1) {
          try {
            const response = await fetch('http://127.0.0.1:5000/evaluate_solution');
            if (response.ok) {
              const data_new = await response.json();
              console.log(data_new.evaluations);
              // Update the state with the fetched value
              const newInputs = [...inputs];
              newInputs.forEach((input, index) => {
                if (index < data_new.evaluations.length) {
                  newInputs[index][numberOfParameters] = data_new.evaluations[index];
                }
              });
              setInputs(newInputs);
            } else {
              console.error('Failed to fetch number of parameters');
            }
          } catch (error) {
            console.error('Error:', error);
          }
        }
        setValidated(true); // Set validated to true after successful validation
        setValidationMessage('Inputs were taken into consideration'); // Set the validation message
        setTimeout(() => setValidationMessage(''), 2000); // Clear the message after 2 seconds
      } else {
        console.error('Failed to validate inputs');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <div className="input-box">
      {inputs.map((input, inputIndex) => (
        <div className="input-container" key={inputIndex}>
          <div className="input">
            {input.map((parameter, parameterIndex) => (
              <div className="input-parameter-container" key={`${inputIndex}-${parameterIndex}`}>
                <input
                  type="text"
                  placeholder={parameterIndex + 1 === numberOfParameters + 1 ? (boxStyle === 1 ? "Output" : `Parameter ${parameterIndex + 1}`) : `Parameter ${parameterIndex + 1}`}
                  value={parameter}
                  onChange={(e) => handleInputChange(inputIndex, parameterIndex, e.target.value)}
                  readOnly={parameterIndex + 1 === numberOfParameters + 1 && boxStyle === 1}
                />
              </div>
            ))}
            {inputs.length > 1 && (
              <button onClick={() => handleRemoveInput(inputIndex)}>Remove</button>
            )}
          </div>
        </div>
      ))}
      <div className="container">
        {typeof numberOfParameters === 'number' && numberOfParameters > 0 && (
          <button onClick={handleAddInput}>Add Input</button>
        )}
        {numberOfParameters > 0 && (
          <div className="container" style={{ margin: '10px 0' }}>
            {!invalidExpression && (
              <button onClick={handleValidate}>Validate</button>
            )}
          </div>
        )}
        {validationMessage && <p className='validate'>{validationMessage}</p>} {/* Display validation message */}
      </div>
      <div>
     
      </div>
    </div>
  );
};

export default InputBox;
