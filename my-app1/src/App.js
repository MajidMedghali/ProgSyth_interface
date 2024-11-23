import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Link, useLocation } from 'react-router-dom'; // Import useLocation
import './styles.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import img from "./Progsynth_logo.png";
import Examples from './Examples';
import Dsl from './Dsl';
import Home from './Home';
import Cst from './Cst';
import 'boxicons/css/boxicons.min.css';
import { Application } from '@splinetool/runtime';

const DescriptionContainer = () => {
  return (
    <div className="description-container">
      <h2>ProgSynth</h2>
      <p>
        ProgSynth is a high-level framework that enables leveraging program synthesis for other domains such as reinforcement learning or system design.
      </p>
    </div>
  );
};

const FeaturesContainer = () => {
  return (
    <div className="features-container">
      <h3>Why Progsynth</h3>
      <p>The advantage of "classic" algorithms are their theoretical guarantees. 
        But many new deep learning based methods have emerged, 
        they provide a tremendous efficiency but lose almost all theoretical guarantees. 
        ProgSynth provides already implemented algorithms that combine both approaches to get the best of both worlds: 
        speed and guarantees!</p>
    </div>
  );
};

function App() {
  const [isChecked, setIsChecked] = useState(false);
  const location = useLocation(); // Use useLocation hook

  const handleCheckboxChange = () => {
    setIsChecked(!isChecked);
  };

  useEffect(() => {
    if (location.pathname === '/') {
      const canvas1 = document.getElementById('canvas3d1');
      const app1 = new Application(canvas1);
      app1.load('https://prod.spline.design/fzUd-AFC1Y8I4PR2/scene.splinecode')
        .then(() => {
          console.log('First Spline scene loaded successfully!');
        })
        .catch((error) => {
          console.error('Error loading first Spline scene:', error);
        });

      const canvas2 = document.getElementById('canvas3d2');
      const app2 = new Application(canvas2);
      // Load the second spline scene and adjust its positioning
      app2.load('https://prod.spline.design/dCjWMo0YLmAFpNLq/scene.splinecode')
        .then(() => {
          console.log('Second Spline scene loaded successfully!');
        })
        .catch((error) => {
          console.error('Error loading second Spline scene:', error);
        });
    }
  }, [location.pathname]);

  return (
    <div>
      <header>
        <input type="checkbox" id="check" checked={isChecked} onChange={handleCheckboxChange} />
        <label htmlFor="check" className="icons">
          <i className='bx bx-menu' id="menu-icon"></i>
          <i className='bx bx-x' id="close-icon"></i>
        </label>
        {/* <img className="logo" src={img} alt="Progsynth Logo" /> */}
        <nav className={`navigation ${isChecked ? 'active' : ''}`}>
          <Link to="/Home">Experience</Link>
          <Link to="/Examples">Examples</Link>
          <Link to="/Cst">CST</Link>
          <Link to="/Dsl">DSL</Link>
          <Link to="/Statistics">Statistics</Link>
        </nav>
      </header>
      <main>
      <Routes>
        <Route path="/Home" element={<Home />} />
        <Route path="/Examples" element={<Examples />} />
        <Route path="/Cst" element={<Cst />} />
        <Route path="/Dsl" element={<Dsl />} />
      </Routes>
      {location.pathname === '/' && (
          <div className="container"> {/* Wrap containers in a parent container */}
            <DescriptionContainer /> {/* Import and render DescriptionContainer component */}
            <FeaturesContainer />  {/* Import and render FeaturesContainer component */}
          </div>
        )}
      </main>

      {/* Conditionally render the canvases only on the default route */}
      {location.pathname === '/' && (
        <>
          {/* Canvas for the first 3D animation */}
          <canvas id="canvas3d1" style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}></canvas>

          {/* Canvas for the second 3D animation, positioned at the top left corner */}
          {/* <canvas id="canvas3d2" style={{ position: 'absolute', top: '-50px', left: '-300px', width: '50px', height: '6rem' }}></canvas> */}
        </>
      )}
      <canvas id="canvas3d2" style={{ position: 'absolute', top: '-50px', left: '-300px', width: '50px', height: '6rem' }}></canvas>
      <button style={{ 
      position: 'absolute', 
      left: 0, 
      top: 0, 
      height: '6rem', 
      width: '20%', 
      opacity: 0 
    }} onClick={() => window.location.href = '/'}></button>
    </div>
  );
}

export default App;