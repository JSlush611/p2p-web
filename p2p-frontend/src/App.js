import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import AboutPage from './components/AboutPage';
import StaticGraphs from './components/StaticGraphs';
import GraphBuilder from './components/GraphBuilder';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<AboutPage />} />
        <Route path="/graphs" element={<StaticGraphs />} />
        <Route path="/build-graph" element={<GraphBuilder />} />
      </Routes>
    </Router>
  );
}

export default App;
