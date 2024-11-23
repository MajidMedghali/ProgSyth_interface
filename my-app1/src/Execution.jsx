import React, { useState } from 'react';

function ExecutionForm() {
  const [argumentsList, setArgumentsList] = useState([""]);

  const handleInputChange = (index, value) => {
    const newList = [...argumentsList];
    newList[index] = value;
    setArgumentsList(newList);
  };

  const handleAddInput = () => {
    setArgumentsList([...argumentsList, ""]);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const messageDiv = document.getElementById("message");
    messageDiv.innerHTML = "Button clicked!";
  };

  return (
    <section className='execution'>
      <form onSubmit={handleSubmit}>
        <div className='arguments'>
          <label className='titles'>Enter your arguments:</label>
          {argumentsList.map((arg, index) => (
            <input
              key={index}
              type="text"
              placeholder={`Argument ${index + 1}`}
              value={arg}
              onChange={(e) => handleInputChange(index, e.target.value)}
            />
          ))}
          <button type="button" onClick={handleAddInput}>+</button> {/* Button to add more input fields */}
        </div>
        <button type="submit" className="main-btn" id="execute-btn">Execute</button> 
      </form>
      <div id="result_execution"></div>
    </section>
  );
}

export default ExecutionForm;
