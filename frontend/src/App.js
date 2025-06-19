// src/App.js
import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [apiData, setApiData] = useState(null);

  useEffect(() => {
    fetch('/api/')  // Request to backend root `/api/`
      .then(res => res.json())
      .then(data => setApiData(data))
      .catch(err => {
        console.error("API fetch failed:", err);
        setApiData({ error: "Failed to load API" });
      });
  }, []);

  return (
    <div className="App">
      <h1>Simple DBMS API change from git</h1>
      {apiData ? (
        <>
          <p>{apiData.message}</p>
          <h2>Endpoints:</h2>
          <ul>
            {Object.entries(apiData.endpoints).map(([endpoint, desc]) => (
              <li key={endpoint}>
                <code>{endpoint}</code>: {desc}
              </li>
            ))}
          </ul>
        </>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default App;

