import React, { useEffect, useState } from 'react';
import { HashRouter, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import ClientDashboard from './pages/ClientDashboard';
import VCDashboard from './pages/VCDashboard';

function App() {
  const [session, setSession] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const mockSession = localStorage.getItem('mock_session');
    if (mockSession) {
      setSession(JSON.parse(mockSession));
    }
    setLoading(false);
  }, []);

  if (loading) {
    return (
      <div style={{ display: 'flex', height: '100vh', alignItems: 'center', justifyContent: 'center' }}>
        <h2 className="text-gold" style={{ fontFamily: 'var(--ff-display)', letterSpacing: '0.1em' }}>INITIALIZING...</h2>
      </div>
    );
  }

  // Strictly route based on the access URL path
  const isCEOPortal = window.location.pathname.includes('revVAC-ceo');

  return (
    <HashRouter>
      <Routes>
        <Route path="/login" element={!session ? <Login /> : <Navigate to="/" />} />
        
        <Route 
          path="/" 
          element={
            session ? (
              isCEOPortal ? (
                session.user.email === 'ceo@vextaudit.com' ? <VCDashboard /> : <Navigate to="/login" />
              ) : (
                <ClientDashboard session={session} />
              )
            ) : <Navigate to="/login" />
          } 
        />
      </Routes>
    </HashRouter>
  );
}

export default App;
