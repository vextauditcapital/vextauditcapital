import React, { useState } from 'react';
import { ShieldCheck, Mail, Lock, ArrowRight, KeyRound } from 'lucide-react';

export default function Login() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [step, setStep] = useState(1); // 1 = credentials, 2 = OTP

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setSuccessMsg('');

    // Hardcode CEO check if attempting to login to revVAC-ceo portal
    if (window.location.pathname.includes('revVAC-ceo') && email !== 'ceo@vextaudit.com') {
        setError('Access Denied. Unauthorized clearance level for Executive Command Center.');
        setLoading(false);
        return;
    }

    // Simulate sending 2FA / OTP
    setTimeout(() => {
      setStep(2);
      setSuccessMsg(`Two-step verification code sent to ${email}`);
      setLoading(false);
    }, 600);
  };

  const handleVerifyOTP = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Simulate OTP verification
    setTimeout(() => {
      if (otp.length < 4) {
        setError('Invalid verification code.');
        setLoading(false);
        return;
      }
      localStorage.setItem('mock_session', JSON.stringify({ user: { email } }));
      window.location.reload();
    }, 800);
  };

  return (
    <div style={{
      minHeight: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      background: 'radial-gradient(circle at center, var(--burgundy) 0%, var(--burgundy-dark) 100%)',
      padding: '20px'
    }}>
      <div className="glass-panel" style={{
        maxWidth: '420px',
        width: '100%',
        padding: '40px 32px',
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center'
      }}>
        
        <img 
          src={`${import.meta.env.BASE_URL}logo.jpg`}
          alt="Vext Audit Capital" 
          style={{ width: '64px', height: '64px', borderRadius: '50%', marginBottom: '20px', border: '1px solid rgba(197, 160, 89, 0.3)', objectFit: 'cover' }} 
        />

        <h1 className="mb-2" style={{ textAlign: 'center', fontSize: '20px' }}>
          SECURE <span className="text-gold">PORTAL</span>
        </h1>
        <p className="text-muted ui-text mb-6" style={{ textAlign: 'center', fontSize: '13px', letterSpacing: '0.05em' }}>
          Prudentia · Integritas · Fidelitas
        </p>

        {error && (
          <div style={{ width: '100%', padding: '10px', background: 'rgba(255, 0, 0, 0.1)', border: '1px solid rgba(255,0,0,0.3)', borderRadius: '4px', color: '#ff8a8a', fontSize: '12px', marginBottom: '16px', fontFamily: 'var(--ff-ui)' }}>
            {error}
          </div>
        )}
        
        {successMsg && (
          <div style={{ width: '100%', padding: '10px', background: 'rgba(197, 160, 89, 0.1)', border: '1px solid rgba(197,160,89,0.3)', borderRadius: '4px', color: 'var(--gold)', fontSize: '12px', marginBottom: '16px', fontFamily: 'var(--ff-ui)' }}>
            {successMsg}
          </div>
        )}

        {step === 1 ? (
          <form onSubmit={handleLogin} style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '14px' }}>
            
            <div style={{ position: 'relative' }}>
              <Mail size={16} color="var(--gold)" style={{ position: 'absolute', top: '12px', left: '14px', opacity: 0.7 }} />
              <input 
                type="email" 
                placeholder="Institutional Email" 
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                style={{ paddingLeft: '40px', fontSize: '14px', padding: '10px 10px 10px 40px' }}
              />
            </div>

            <div style={{ position: 'relative' }}>
              <Lock size={16} color="var(--gold)" style={{ position: 'absolute', top: '12px', left: '14px', opacity: 0.7 }} />
              <input 
                type="password" 
                placeholder="Access Passcode" 
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={{ paddingLeft: '40px', fontSize: '14px', padding: '10px 10px 10px 40px' }}
              />
            </div>

            <button type="submit" className="btn-primary" style={{ marginTop: '4px', width: '100%', fontSize: '12px', padding: '12px' }} disabled={loading}>
              {loading ? 'Authenticating...' : 'Secure Login'}
              {!loading && <ArrowRight size={14} />}
            </button>
          </form>
        ) : (
          <form onSubmit={handleVerifyOTP} style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '14px' }}>
            <p className="ui-text text-cream" style={{ fontSize: '13px', textAlign: 'center', marginBottom: '8px' }}>
              We've sent a temporary verification code to your registered email to secure this session.
            </p>
            <div style={{ position: 'relative' }}>
              <KeyRound size={16} color="var(--gold)" style={{ position: 'absolute', top: '12px', left: '14px', opacity: 0.7 }} />
              <input 
                type="text" 
                placeholder="Enter Verification Code" 
                required
                value={otp}
                onChange={(e) => setOtp(e.target.value)}
                style={{ paddingLeft: '40px', fontSize: '14px', padding: '10px 10px 10px 40px', letterSpacing: '0.2em', textAlign: 'center' }}
              />
            </div>
            <button type="submit" className="btn-primary" style={{ marginTop: '4px', width: '100%', fontSize: '12px', padding: '12px' }} disabled={loading}>
              {loading ? 'Verifying...' : 'Verify & Enter'}
            </button>
            <button 
              type="button"
              onClick={() => { setStep(1); setSuccessMsg(''); setError(''); setOtp(''); }}
              className="ui-text text-muted"
              style={{ background: 'none', border: 'none', marginTop: '12px', fontSize: '11px', cursor: 'pointer', textDecoration: 'underline' }}
            >
              Back to Login
            </button>
          </form>
        )}

      </div>
    </div>
  );
}
