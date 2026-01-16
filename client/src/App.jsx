import { Routes, Route } from "react-router-dom";
import { useState } from 'react';
import axios from "axios";

import './App.css';
import Header from "./components/Header";
import Home from "./pages/Home";
import OpponentSelect from "./pages/OpponentSelect";
import Results from "./pages/Results";



function App() {
  const [result, setResult] = useState({
    champ: null,
    opponents: Array(5).fill(null),
  });

  return (
    <div>
      <Header />

      <Routes>
        <Route path="/" element={<Home result={result} setResult={setResult} />} />
        <Route path="/opponents" element={<OpponentSelect result={result} setResult={setResult} />} />
        <Route path="/results" element={<Results /> } />
      </Routes>
    </div>
  );
}

export default App;


