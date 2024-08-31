import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Navbar from './components/Navbar';
import AboutPage from './components/AboutPage';
import StaticGraphs from './components/StaticGraphs';
import GraphBuilder from './components/GraphBuilder';
import SuggestionForm from './components/SuggestionForm';
import ThankYouPage from './components/ThankYouPage';

function App() {
  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<AboutPage />} />
        <Route path="/graphs" element={<StaticGraphs />} />
        <Route path="/build-graph" element={<GraphBuilder />} />
        <Route path="/suggestions" element={<SuggestionForm />} /> 
        <Route path="/thank-you" element={<ThankYouPage />} />
      </Routes>
    </Router>
  );
}

export default App;
