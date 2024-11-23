import React, { useState, useEffect } from 'react';
import './Examples.css';
import InputBox from './inputBox';

const ExpressionBox = ({ onExpressionSubmit, numberOfParameters }) => {
  const [expression, setExpression] = useState('');
  const [initialSubmission, setInitialSubmission] = useState(true);
  const [submitted, setSubmitted] = useState(false);
  const [editing, setEditing] = useState(false);
  const [showInputBox, setShowInputBox] = useState(false);
  const [invalidExpression, setInvalidExpression] = useState(false);
  const [validated, setValidated] = useState(false); // New state variable for validation

  const handleButtonClick = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/Dsl', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ expression })
      });

      if (response.ok) {
        onExpressionSubmit();
        setSubmitted(true);
        setEditing(false);
        setInitialSubmission(false);
        setShowInputBox(true); // Show input box after successful submission
        setInvalidExpression(false); // Reset invalid expression flag
        setValidated(false); // Reset validated flag
      } else {
        console.error('Failed to submit expression');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  const handleChangeExpression = () => {
    if (submitted) {
      setSubmitted(false);
    }
    setShowInputBox(false); // Hide input box when changing expression
    setEditing(true); // Set editing to true when changing expression
    setValidated(false); // Reset validated flag
  };

  const handleInputChange = (e) => {
    setExpression(e.target.value);
  };

  const handleSubmitOrChange = () => {
    if (editing) {
      handleButtonClick();
    } else {
      handleChangeExpression();
    }
  };

  useEffect(() => {
    const intervalId = setInterval(() => {
      if (typeof numberOfParameters !== 'number' || isNaN(numberOfParameters)) {
        setInvalidExpression(true);
      } else {
        setInvalidExpression(false);
      }
    }, 1000); // Check every second

    return () => clearInterval(intervalId); // Cleanup interval on unmount
  }, [numberOfParameters]);

  return (
    <div className="expression-box">
      <div className="container">
        <div className="box">
          <input
            type="text"
            placeholder="Enter expression"
            value={expression}
            onChange={handleInputChange}
            disabled={submitted && !editing}
          />
          {(initialSubmission && !editing) ? (
            <button onClick={handleButtonClick}>Submit</button>
          ) : (
            <button onClick={handleSubmitOrChange}>
              {editing ? 'Submit' : 'Change Expression'}
            </button>
          )}
        </div>
      </div>
      {invalidExpression && (
        <div className="container">
          <p className="error-message">Not valid</p>
        </div>
      )}
      {showInputBox && (
        <div className="container">
          <InputBox
            numberOfParameters={numberOfParameters}
            invalidExpression={invalidExpression}
            validated={validated} // Pass validated state to InputBox
            setValidated={setValidated}
            boxStyle={0} // Pass setValidated function to InputBox
          />
        </div>
      )}
    </div>
  );
};



const Examples = () => {
  const [numberOfParameters, setNumberOfParameters] = useState(1);

  const handleExpressionSubmit = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/get_number_of_parameters');
      if (response.ok) {
        const data = await response.json();
        // console.log(data.num_param)
        setNumberOfParameters(data.num_param);
        console.log(data.num_param); // Update the state with the fetched value
      } else {
        console.error('Failed to fetch number of parameters');
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  return (
    <section className="main">
      <div className="container">
        <ExpressionBox onExpressionSubmit={handleExpressionSubmit} numberOfParameters={numberOfParameters}  />
      </div>
    </section>
  );
};

export default Examples;
