import React, { useState, useEffect } from 'react';
import './index.css';

function App() {
  const [dirtLevel, setDirtLevel] = useState(50);
  const [loadSize, setLoadSize] = useState(50);
  const [cycleTime, setCycleTime] = useState(null);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const res = await fetch('http://127.0.0.1:8000/history');
      const data = await res.json();
      setHistory(data);
    } catch (err) {
      console.error("Failed to fetch history:", err);
    }
  };

  const calculateCycleTime = async () => {
    setLoading(true);
    setCycleTime(null); // Reset to trigger animation
    
    try {
      // Small artificial delay for a satisfying smooth animation effect
      await new Promise(resolve => setTimeout(resolve, 800));

      const res = await fetch('http://127.0.0.1:8000/predict', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          dirt_level: parseFloat(dirtLevel),
          load_size: parseFloat(loadSize)
        })
      });
      
      const data = await res.json();
      setCycleTime(data.cycle_time);
      fetchHistory(); // Refresh the list
    } catch (error) {
      console.error("Fetch error:", error);
      alert("Error: Could not connect to backend. Is it running on port 8000?");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app-container">
      <div className="card">
        <h1>FuzzyWash™</h1>
        <p className="subtitle">AI-Powered Cycle Time Predictor</p>

        <div className="slider-group">
          <label>
            <span>Dirt Level</span>
            <span>{dirtLevel}%</span>
          </label>
          <input 
            type="range" 
            min="0" max="100" 
            value={dirtLevel}
            onChange={(e) => setDirtLevel(e.target.value)}
          />
        </div>

        <div className="slider-group">
          <label>
            <span>Load Size</span>
            <span>{loadSize}%</span>
          </label>
          <input 
            type="range" 
            min="0" max="100" 
            value={loadSize}
            onChange={(e) => setLoadSize(e.target.value)}
          />
        </div>

        <button onClick={calculateCycleTime} disabled={loading}>
          {loading ? <div className="spinner"></div> : "Calculate Optimal Cycle"}
        </button>

        <div style={{ marginTop: '2.5rem' }}>
          <h3 style={{ fontSize: '1.05rem', marginBottom: '1rem', color: '#334155' }}>
            Recent History
          </h3>
          <ul className="history-list">
            {history.length === 0 && <li className="history-item">No calculations yet.</li>}
            {history.map((item, idx) => (
              <li key={idx} className="history-item">
                <span>Dirt: {item.dirt_level}% | Load: {item.load_size}%</span>
                <strong>{item.cycle_time} min</strong>
              </li>
            ))}
          </ul>
        </div>
      </div>

      <div className="card result-card">
        <h2>Optimal Cycle Time</h2>
        {cycleTime !== null ? (
          <>
            <div className="result-time">{cycleTime}</div>
            <div className="result-unit">Minutes</div>
          </>
        ) : (
          <div style={{ marginTop: '2rem', opacity: 0.8, fontSize: '1.1rem', lineHeight: '1.5' }}>
            Adjust the sliders and calculate<br/>to find the ideal timing.
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
