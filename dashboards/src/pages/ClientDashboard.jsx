import React, { useEffect, useState } from 'react';
import { LogOut, FileText, Download, CheckCircle, Clock, User, Upload, MessageSquare } from 'lucide-react';

export default function ClientDashboard({ session }) {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState('audits'); // 'audits' | 'profile'

  useEffect(() => {
    setTimeout(() => {
      setReports([
        { id: '1', type: 'DPDP Readiness Assessment', status: 'Completed', date: '2026-06-01', score: 94 },
        { id: '2', type: 'GST Compliance Audit', status: 'In Progress', date: '2026-06-02', score: null },
      ]);
      setLoading(false);
    }, 1000);
  }, []);

  const handleSignOut = () => {
    localStorage.removeItem('mock_session');
    window.location.reload();
  };

  return (
    <div className="dashboard-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div style={{ padding: '24px 24px', borderBottom: '1px solid rgba(197, 160, 89, 0.1)', display: 'flex', alignItems: 'center', gap: '12px' }}>
          <img src={`${import.meta.env.BASE_URL}logo.jpg`} alt="Logo" style={{ width: '40px', height: '40px', borderRadius: '50%' }} />
          <div>
            <h2 className="text-gold" style={{ fontSize: '15px', letterSpacing: '0.1em' }}>VEXT AUDIT</h2>
            <p className="ui-text text-muted" style={{ fontSize: '10px', letterSpacing: '0.15em', marginTop: '2px' }}>CLIENT PORTAL</p>
          </div>
        </div>
        
        <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '12px' }}>
          <button 
            onClick={() => setActiveTab('audits')}
            className="ui-text text-gold" 
            style={{ border: 'none', cursor: 'pointer', textAlign: 'left', textDecoration: 'none', padding: '12px', background: activeTab === 'audits' ? 'rgba(197,160,89,0.1)' : 'transparent', borderRadius: '6px', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '12px', transition: 'background 0.2s' }}>
            <FileText size={16} /> My Audits
          </button>
          <button 
            onClick={() => setActiveTab('profile')}
            className="ui-text text-gold" 
            style={{ border: 'none', cursor: 'pointer', textAlign: 'left', textDecoration: 'none', padding: '12px', background: activeTab === 'profile' ? 'rgba(197,160,89,0.1)' : 'transparent', borderRadius: '6px', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '12px', transition: 'background 0.2s' }}>
            <User size={16} /> My Profile &amp; Documents
          </button>
        </div>

        <div className="mt-auto" style={{ padding: '24px', borderTop: '1px solid rgba(197, 160, 89, 0.1)' }}>
          <p className="ui-text text-muted mb-4" style={{ fontSize: '11px' }}>
            Support: <a href="mailto:support@vextaudit.com" style={{ color: 'var(--gold)' }}>support@vextaudit.com</a>
          </p>
          <button onClick={handleSignOut} className="btn-ghost" style={{ width: '100%', padding: '10px', fontSize: '11px' }}>
            <LogOut size={14} /> Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="topbar">
          <h3 className="text-cream" style={{ fontSize: '14px', letterSpacing: '0.1em' }}>{activeTab === 'audits' ? 'COMPLIANCE OVERVIEW' : 'CLIENT PROFILE'}</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ display: 'block', width: '6px', height: '6px', borderRadius: '50%', background: '#4ade80', boxShadow: '0 0 8px #4ade80' }}></span>
            <span className="ui-text text-muted" style={{ fontSize: '11px', letterSpacing: '0.1em' }}>SECURE CONNECTION</span>
          </div>
        </header>

        <div className="content-area">
          
          {activeTab === 'audits' && (
            <>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '24px', marginBottom: '32px' }}>
                <div className="glass-panel" style={{ padding: '24px' }}>
                  <p className="ui-text text-gold mb-2" style={{ fontSize: '11px', letterSpacing: '0.2em' }}>OVERALL COMPLIANCE SCORE</p>
                  <div style={{ display: 'flex', alignItems: 'flex-end', gap: '8px' }}>
                    <span style={{ fontFamily: 'var(--ff-display)', fontSize: '40px', color: 'var(--cream)', lineHeight: '1' }}>94</span>
                    <span className="text-muted ui-text" style={{ paddingBottom: '6px', fontSize: '14px' }}>/ 100</span>
                  </div>
                  <p className="ui-text text-muted mt-4" style={{ fontSize: '13px' }}>Your business entity is currently in good standing. Next statutory filing due in 14 days.</p>
                </div>
                
                <div className="glass-panel" style={{ padding: '24px', display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
                   <p className="ui-text text-gold mb-4" style={{ fontSize: '11px', letterSpacing: '0.2em' }}>SECURE ACTIONS</p>
                   <button className="btn-primary" onClick={() => alert('Feedback form would open here.')} style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: '8px' }}><MessageSquare size={14} /> Submit Feedback / NPS</button>
                </div>
              </div>

              <h3 className="text-cream mb-4" style={{ fontSize: '16px', letterSpacing: '0.05em' }}>Audit Ledger &amp; Reports</h3>
              
              <div className="glass-panel" style={{ overflow: 'hidden' }}>
                {loading ? (
                  <div style={{ padding: '40px', textAlign: 'center' }} className="ui-text text-muted">Loading audit ledger...</div>
                ) : (
                  <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left' }} className="ui-text">
                    <thead>
                      <tr style={{ borderBottom: '1px solid rgba(197, 160, 89, 0.2)' }}>
                        <th style={{ padding: '16px 20px', color: 'var(--gold)', fontSize: '11px', letterSpacing: '0.1em' }}>AUDIT TYPE</th>
                        <th style={{ padding: '16px 20px', color: 'var(--gold)', fontSize: '11px', letterSpacing: '0.1em' }}>DATE INITIATED</th>
                        <th style={{ padding: '16px 20px', color: 'var(--gold)', fontSize: '11px', letterSpacing: '0.1em' }}>STATUS</th>
                        <th style={{ padding: '16px 20px', color: 'var(--gold)', fontSize: '11px', letterSpacing: '0.1em' }}>SCORE</th>
                        <th style={{ padding: '16px 20px', color: 'var(--gold)', fontSize: '11px', letterSpacing: '0.1em', textAlign: 'right' }}>ACTION</th>
                      </tr>
                    </thead>
                    <tbody>
                      {reports.map((report) => (
                        <tr key={report.id} style={{ borderBottom: '1px solid rgba(197, 160, 89, 0.1)' }}>
                          <td style={{ padding: '16px 20px', fontSize: '13px' }}>{report.type}</td>
                          <td style={{ padding: '16px 20px', color: 'rgba(245, 245, 220, 0.6)', fontSize: '13px' }}>{report.date}</td>
                          <td style={{ padding: '16px 20px' }}>
                            <div style={{ 
                              display: 'inline-flex', alignItems: 'center', gap: '6px', 
                              padding: '4px 10px', borderRadius: '20px', fontSize: '11px',
                              background: report.status === 'Completed' ? 'rgba(74, 222, 128, 0.1)' : 'rgba(197, 160, 89, 0.1)',
                              color: report.status === 'Completed' ? '#4ade80' : 'var(--gold)'
                            }}>
                              {report.status === 'Completed' ? <CheckCircle size={12} /> : <Clock size={12} />}
                              {report.status}
                            </div>
                          </td>
                          <td style={{ padding: '16px 20px', fontFamily: 'var(--ff-display)', fontSize: '15px' }}>
                            {report.score ? report.score : '--'}
                          </td>
                          <td style={{ padding: '16px 20px', textAlign: 'right' }}>
                            {report.status === 'Completed' ? (
                              <button style={{ background: 'none', border: 'none', color: 'var(--gold)', cursor: 'pointer', display: 'inline-flex', alignItems: 'center', gap: '6px', fontSize: '12px', fontFamily: 'var(--ff-ui)' }}>
                                <Download size={14} /> PDF
                              </button>
                            ) : (
                              <span style={{ color: 'rgba(245, 245, 220, 0.3)', fontSize: '12px' }}>Processing...</span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>
            </>
          )}

          {activeTab === 'profile' && (
            <div className="glass-panel" style={{ padding: '32px' }}>
              <h3 className="text-gold mb-6" style={{ fontSize: '16px', letterSpacing: '0.05em' }}>Personal &amp; Corporate Details</h3>
              <form className="ui-text" style={{ display: 'flex', flexDirection: 'column', gap: '20px', maxWidth: '600px' }} onSubmit={(e) => { e.preventDefault(); alert("Profile updated successfully!"); }}>
                
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                  <div>
                    <label style={{ display: 'block', fontSize: '11px', color: 'var(--gold)', letterSpacing: '0.1em', marginBottom: '6px' }}>FULL NAME</label>
                    <input type="text" value="Registered Client" disabled style={{ opacity: 0.6, cursor: 'not-allowed', fontSize: '13px', padding: '10px' }} />
                  </div>
                  <div>
                    <label style={{ display: 'block', fontSize: '11px', color: 'var(--gold)', letterSpacing: '0.1em', marginBottom: '6px' }}>DATE OF BIRTH</label>
                    <input type="text" value="XX/XX/XXXX" disabled style={{ opacity: 0.6, cursor: 'not-allowed', fontSize: '13px', padding: '10px' }} />
                  </div>
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '11px', color: 'var(--gold)', letterSpacing: '0.1em', marginBottom: '6px' }}>COMPANY NAME</label>
                  <input type="text" placeholder="Enter registered entity name" style={{ fontSize: '13px', padding: '10px' }} />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '11px', color: 'var(--gold)', letterSpacing: '0.1em', marginBottom: '6px' }}>GSTIN</label>
                  <input type="text" placeholder="e.g. 27AAAAA0000A1Z5" style={{ fontSize: '13px', padding: '10px' }} />
                </div>

                <div>
                  <label style={{ display: 'block', fontSize: '11px', color: 'var(--gold)', letterSpacing: '0.1em', marginBottom: '6px' }}>REGISTERED ADDRESS</label>
                  <textarea placeholder="Full corporate address" rows="3" style={{ fontSize: '13px', padding: '10px', resize: 'vertical' }}></textarea>
                </div>

                <div style={{ borderTop: '1px solid rgba(197, 160, 89, 0.2)', paddingTop: '24px', marginTop: '8px' }}>
                  <h4 className="text-gold mb-4" style={{ fontSize: '14px', letterSpacing: '0.05em', fontFamily: 'var(--ff-display)' }}>Document Upload</h4>
                  <p className="text-muted mb-4" style={{ fontSize: '12px' }}>Upload PAN, Incorporation Certificate, or financial statements here. Documents are encrypted at rest.</p>
                  
                  <div style={{ border: '1px dashed rgba(197, 160, 89, 0.4)', borderRadius: '6px', padding: '32px', textAlign: 'center', background: 'rgba(29, 4, 4, 0.3)' }}>
                    <Upload size={24} color="var(--gold)" style={{ marginBottom: '12px' }} />
                    <p style={{ fontSize: '13px', color: 'var(--cream)', marginBottom: '8px' }}>Click to browse or drag and drop files</p>
                    <p style={{ fontSize: '11px', color: 'rgba(245, 245, 220, 0.4)' }}>PDF, JPG, PNG (Max 10MB)</p>
                  </div>
                </div>

                <button type="submit" className="btn-primary" style={{ marginTop: '16px', alignSelf: 'flex-start' }}>Save Changes</button>

              </form>
            </div>
          )}

        </div>
      </main>
    </div>
  );
}
