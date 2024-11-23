import React, { useState } from 'react';

function Dsl() {
  const items = [
    'deepcoder', 'raw', 'dreamcoder', 'regexp',
    'transduction', 'calculator', 'karel'
  ];

  const [selectedItem, setSelectedItem] = useState(null);

  const handleSelectItem = (item) => {
    setSelectedItem(item);
  };

  return (
    <section className="main">
      <div className='main-text'>
      <h1>Choose your DSL</h1>
      <div className="grid">
        {items.map(item => (
          <div 
            
          key={item}
          className={`main-dsl ${selectedItem === item ? 'selected' : ''}`}
          onClick={() => handleSelectItem(item)}
          >
            {item}
          </div>
        ))}
      </div>
      {selectedItem && <p>You selected: {selectedItem}</p>}
      </div>
    </section>
  );
}


export default Dsl;