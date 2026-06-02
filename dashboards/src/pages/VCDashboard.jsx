import React, { useEffect, useState } from 'react';
import { LogOut, TrendingUp, Users, Activity, BarChart4, DollarSign, Mail, Globe, MapPin, Target, Wallet, AlertCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';

export default function VCDashboard() {
  const [loading, setLoading] = useState(true);

  // TRUE Targets based on CEO Screenshot
  const revenueTargets = [
    { month: 'Jun-26', fy: 'FY 2026-27', target: 7500000 },
    { month: 'Jul-26', fy: 'FY 2026-27', target: 10000000 },
    { month: 'Aug-26', fy: 'FY 2026-27', target: 11000000 },
    { month: 'Sep-26', fy: 'FY 2026-27', target: 12100000 },
    { month: 'Oct-26', fy: 'FY 2026-27', target: 13310000 },
    { month: 'Nov-26', fy: 'FY 2026-27', target: 14641000 },
    { month: 'Dec-26', fy: 'FY 2026-27', target: 16105100 },
    { month: 'Jan-27', fy: 'FY 2026-27', target: 17715610 },
    { month: 'Feb-27', fy: 'FY 2026-27', target: 19487171 },
    { month: 'Mar-27', fy: 'FY 2026-27', target: 21435888 },
  ];

  // Zeroed out real-world metrics (Pending API Integrations)
  const metrics = {
    mrr_growth_rate: "0%",
    yoy_growth_rate: "0%",
    mom_growth_rate: "0%",
    realised_ltv_to_cac: "0x",
    cac_payback_days: 0,
    email_deliverability_rate: "0%",
    leads: {
      total_processed: 0,
      qualified_icp: 0,
      conversion_rate_percentage: 0,
      status: { hot: 0, cold: 0, dead: 0 },
      designation: { ceo: 0, cfo: 0, founders: 0, others: 0 }
    },
    emails: {
      morning: { generated: 0, initial: 0, followUp1: 0, followUp2: 0 },
      evening: { generated: 0, initial: 0, followUp1: 0, followUp2: 0 },
      stats: { openRate: "0%", bounceRate: "0%", replies: "0%", unopened: "0%", spammed: "0%" }
    },
    financials: {
      total_revenue_inr: 0,
      annual_recurring_revenue_estimate: 0,
      unitEconomics: { cac: 0, cpl: 0, epl: 0 },
      expenses: {
        daily: 0, weekly: 0, monthly: 0,
        breakdown: { marketing: 0, api_systems: 0, workspace_zoho: 0, other: 0 }
      }
    }
  };

  useEffect(() => {
    setTimeout(() => {
      setLoading(false);
    }, 800);
  }, []);

  const handleSignOut = () => {
    localStorage.removeItem('mock_session');
    window.location.reload();
  };

  if (loading) {
    return (
      <div style={{ height: '100vh', background: 'radial-gradient(circle at center, var(--burgundy) 0%, var(--burgundy-dark) 100%)', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <div style={{ color: 'var(--gold)', fontFamily: 'var(--ff-ui)', fontSize: '13px', letterSpacing: '0.1em' }}>Establishing Secure Telemetry Link...</div>
      </div>
    );
  }

  // Chart Data (Empty until API connects)
  const countryData = [{ name: 'Pending Integration', morning: 1, evening: 1 }];
  const COLORS = ['#33131a']; // Muted burgundy for pending data

  return (
    <div className="dashboard-container" style={{ background: 'var(--burgundy-dark)', color: 'var(--cream)', display: 'flex', minHeight: '100vh' }}>
      {/* Sidebar */}
      <aside className="sidebar" style={{ background: 'var(--burgundy)', borderRight: '1px solid rgba(197, 160, 89, 0.2)', width: '260px', flexShrink: 0, display: 'flex', flexDirection: 'column' }}>
        <div style={{ padding: '24px', borderBottom: '1px solid rgba(197, 160, 89, 0.2)', display: 'flex', alignItems: 'center', gap: '12px' }}>
          <img src="https://www.vextaudit.com/VEXT-AUDIT-CAPITAL-LOGO.jpeg" alt="Logo" style={{ width: '40px', height: '40px', borderRadius: '50%', objectFit: 'cover', border: '1px solid var(--gold)' }} />
          <div>
            <h2 style={{ fontSize: '15px', letterSpacing: '0.15em', color: 'var(--gold)' }}>INTERNAL HQ</h2>
            <p className="ui-text" style={{ fontSize: '10px', letterSpacing: '0.2em', marginTop: '2px', color: '#888' }}>VC ANALYTICS LIVE</p>
          </div>
        </div>
        
        <div style={{ padding: '24px', display: 'flex', flexDirection: 'column', gap: '8px' }}>
          <a href="#overview" className="ui-text" style={{ textDecoration: 'none', padding: '12px', background: 'rgba(197, 160, 89, 0.1)', color: 'var(--gold)', borderRadius: '6px', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '12px' }}><Activity size={16} /> Overview</a>
          <a href="#acquisition" className="ui-text" style={{ textDecoration: 'none', padding: '12px', color: '#aaa', borderRadius: '6px', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '12px' }}><Users size={16} /> Acquisition Engine</a>
          <a href="#financials" className="ui-text" style={{ textDecoration: 'none', padding: '12px', color: '#aaa', borderRadius: '6px', fontSize: '13px', display: 'flex', alignItems: 'center', gap: '12px' }}><Wallet size={16} /> Financial Ledger</a>
        </div>

        <div className="mt-auto" style={{ padding: '24px', borderTop: '1px solid rgba(197, 160, 89, 0.2)' }}>
          <button onClick={handleSignOut} className="btn-ghost" style={{ width: '100%', padding: '10px', borderColor: 'rgba(197, 160, 89, 0.3)', color: '#aaa', fontSize: '11px' }}>
            <LogOut size={14} /> Terminate Session
          </button>
        </div>
      </aside>

      {/* Main Content Area */}
      <main style={{ flexGrow: 1, height: '100vh', overflowY: 'auto' }}>
        <header style={{ background: 'rgba(42, 10, 16, 0.95)', borderBottom: '1px solid rgba(197, 160, 89, 0.2)', padding: '16px 32px', position: 'sticky', top: 0, zIndex: 10, display: 'flex', justifyContent: 'space-between', alignItems: 'center', backdropFilter: 'blur(10px)' }}>
          <h3 className="text-gold" style={{ fontSize: '14px', letterSpacing: '0.1em' }}>EXECUTIVE COMMAND CENTER</h3>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ display: 'block', width: '6px', height: '6px', borderRadius: '50%', background: 'var(--gold)', boxShadow: '0 0 12px var(--gold)', animation: 'pulse 2s infinite' }}></span>
            <span className="ui-text" style={{ fontSize: '11px', letterSpacing: '0.15em', color: 'var(--gold)' }}>SYSTEMS LIVE</span>
          </div>
        </header>

        <div style={{ padding: '32px', display: 'flex', flexDirection: 'column', gap: '40px', maxWidth: '1400px', margin: '0 auto' }}>
          
          <div style={{ background: 'rgba(197, 160, 89, 0.1)', border: '1px solid rgba(197, 160, 89, 0.3)', borderRadius: '8px', padding: '16px', display: 'flex', alignItems: 'flex-start', gap: '16px', color: 'var(--gold)' }}>
            <AlertCircle size={24} style={{ flexShrink: 0 }} />
            <div>
              <h4 style={{ fontSize: '14px', marginBottom: '4px', letterSpacing: '0.05em' }}>DATA INTEGRATION PENDING</h4>
              <p className="ui-text" style={{ fontSize: '12px', color: '#ddd' }}>The metrics below (except Target Revenue) have been cleared of simulated data. They will display <strong>0</strong> until the dashboard is actively connected to your live CRM, Email sending tool, and Financial software APIs.</p>
            </div>
          </div>

          {/* SECTION 1: MACRO KPI HERO */}
          <section id="overview">
            <h4 className="ui-text mb-4" style={{ color: 'var(--gold)', fontSize: '12px', letterSpacing: '0.15em' }}><TrendingUp size={14} style={{ display: 'inline', marginBottom: '-2px', marginRight: '6px' }}/> MACRO FINANCIALS</h4>
            
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '20px' }}>
              <div style={{ background: 'var(--burgundy)', padding: '24px', borderRadius: '10px', border: '1px solid rgba(197, 160, 89, 0.2)', borderTop: '2px solid var(--gold)' }}>
                <p className="ui-text" style={{ fontSize: '11px', color: '#aaa', marginBottom: '8px' }}>ARR ESTIMATE (INR)</p>
                <h2 style={{ fontSize: '32px', color: '#fff', lineHeight: 1 }}>₹{(metrics.financials.annual_recurring_revenue_estimate / 10000000).toFixed(2)}<span style={{ fontSize: '18px', color: '#888' }}>Cr</span></h2>
                <div style={{ marginTop: '12px', display: 'flex', gap: '12px' }}>
                  <span style={{ fontSize: '11px', color: 'var(--gold)', background: 'rgba(197,160,89,0.1)', padding: '2px 6px', borderRadius: '4px' }}>+{metrics.yoy_growth_rate} YoY</span>
                  <span style={{ fontSize: '11px', color: 'var(--gold)', background: 'rgba(197,160,89,0.1)', padding: '2px 6px', borderRadius: '4px' }}>+{metrics.mom_growth_rate} MoM</span>
                </div>
              </div>

              <div style={{ background: 'var(--burgundy)', padding: '24px', borderRadius: '10px', border: '1px solid rgba(197, 160, 89, 0.2)', borderTop: '2px solid var(--gold)' }}>
                <p className="ui-text" style={{ fontSize: '11px', color: '#aaa', marginBottom: '8px' }}>LTV : CAC</p>
                <h2 style={{ fontSize: '32px', color: '#fff', lineHeight: 1 }}>{metrics.realised_ltv_to_cac}</h2>
                <p className="ui-text mt-3" style={{ fontSize: '12px', color: 'var(--gold)' }}>CAC Payback: {metrics.cac_payback_days} Days</p>
              </div>

              <div style={{ background: 'var(--burgundy)', padding: '24px', borderRadius: '10px', border: '1px solid rgba(197, 160, 89, 0.2)', borderTop: '2px solid var(--gold)' }}>
                <p className="ui-text" style={{ fontSize: '11px', color: '#aaa', marginBottom: '8px' }}>CURRENT REVENUE (API)</p>
                <h2 style={{ fontSize: '32px', color: '#fff', lineHeight: 1 }}>₹0</h2>
                <p className="ui-text mt-3" style={{ fontSize: '12px', color: '#888' }}>Target: See Financial Ledger</p>
              </div>
            </div>
          </section>


          {/* SECTION 2: ACQUISITION & EMAIL ENGINE */}
          <section id="acquisition" style={{ background: 'var(--burgundy)', padding: '32px', borderRadius: '12px', border: '1px solid rgba(197, 160, 89, 0.2)' }}>
            <h4 className="ui-text mb-6" style={{ color: '#fff', fontSize: '14px', letterSpacing: '0.1em' }}><Mail size={16} style={{ display: 'inline', marginBottom: '-3px', marginRight: '8px', color: 'var(--gold)' }}/> OUTREACH & CONVERSION ENGINE</h4>
            
            <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '32px' }}>
              
              {/* Left Col: Volumes & Funnel */}
              <div>
                <h5 className="ui-text mb-4" style={{ color: 'var(--gold)', fontSize: '11px', letterSpacing: '0.1em' }}>DAILY EMAIL VOLUMES</h5>
                <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse', marginBottom: '32px' }} className="ui-text">
                  <thead>
                    <tr style={{ borderBottom: '1px solid rgba(197, 160, 89, 0.2)', color: '#aaa', fontSize: '10px', letterSpacing: '0.1em' }}>
                      <th style={{ padding: '8px 0' }}>PHASE</th>
                      <th style={{ padding: '8px 0' }}>MORNING (AM)</th>
                      <th style={{ padding: '8px 0' }}>EVENING (PM)</th>
                      <th style={{ padding: '8px 0', color: 'var(--gold)' }}>TOTAL</th>
                    </tr>
                  </thead>
                  <tbody style={{ fontSize: '13px', color: '#ddd' }}>
                    <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                      <td style={{ padding: '12px 0' }}>Leads Generated</td>
                      <td>{metrics.emails.morning.generated}</td>
                      <td>{metrics.emails.evening.generated}</td>
                      <td style={{ color: 'var(--gold)' }}>{metrics.emails.morning.generated + metrics.emails.evening.generated}</td>
                    </tr>
                    <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                      <td style={{ padding: '12px 0' }}>Initial Emails Sent</td>
                      <td>{metrics.emails.morning.initial}</td>
                      <td>{metrics.emails.evening.initial}</td>
                      <td style={{ color: 'var(--gold)' }}>{metrics.emails.morning.initial + metrics.emails.evening.initial}</td>
                    </tr>
                    <tr style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                      <td style={{ padding: '12px 0' }}>Follow-up #1</td>
                      <td>{metrics.emails.morning.followUp1}</td>
                      <td>{metrics.emails.evening.followUp1}</td>
                      <td style={{ color: 'var(--gold)' }}>{metrics.emails.morning.followUp1 + metrics.emails.evening.followUp1}</td>
                    </tr>
                    <tr>
                      <td style={{ padding: '12px 0' }}>Follow-up #2</td>
                      <td>{metrics.emails.morning.followUp2}</td>
                      <td>{metrics.emails.evening.followUp2}</td>
                      <td style={{ color: 'var(--gold)' }}>{metrics.emails.morning.followUp2 + metrics.emails.evening.followUp2}</td>
                    </tr>
                  </tbody>
                </table>

                <h5 className="ui-text mb-4" style={{ color: 'var(--gold)', fontSize: '11px', letterSpacing: '0.1em' }}>LEAD STATUS TRACKER</h5>
                <div style={{ display: 'flex', gap: '16px' }}>
                  <div style={{ flex: 1, background: 'var(--burgundy-dark)', padding: '16px', borderRadius: '8px', borderLeft: '2px solid var(--gold)' }}>
                    <p className="ui-text" style={{ fontSize: '10px', color: '#aaa', marginBottom: '4px' }}>HOT LEADS</p>
                    <p style={{ fontSize: '24px', color: '#fff', fontFamily: 'var(--ff-display)' }}>{metrics.leads.status.hot}</p>
                  </div>
                  <div style={{ flex: 1, background: 'var(--burgundy-dark)', padding: '16px', borderRadius: '8px', borderLeft: '2px solid rgba(197, 160, 89, 0.5)' }}>
                    <p className="ui-text" style={{ fontSize: '10px', color: '#aaa', marginBottom: '4px' }}>COLD LEADS</p>
                    <p style={{ fontSize: '24px', color: '#fff', fontFamily: 'var(--ff-display)' }}>{metrics.leads.status.cold}</p>
                  </div>
                  <div style={{ flex: 1, background: 'var(--burgundy-dark)', padding: '16px', borderRadius: '8px', borderLeft: '2px solid #555' }}>
                    <p className="ui-text" style={{ fontSize: '10px', color: '#aaa', marginBottom: '4px' }}>DEAD LEADS</p>
                    <p style={{ fontSize: '24px', color: '#fff', fontFamily: 'var(--ff-display)' }}>{metrics.leads.status.dead}</p>
                  </div>
                </div>

              </div>

              {/* Right Col: Pie Chart & Stats */}
              <div style={{ borderLeft: '1px solid rgba(197, 160, 89, 0.2)', paddingLeft: '32px' }}>
                <h5 className="ui-text mb-2" style={{ color: 'var(--gold)', fontSize: '11px', letterSpacing: '0.1em' }}><MapPin size={12} style={{ display: 'inline' }}/> GEO DISTRIBUTION (EMAILS)</h5>
                <div style={{ height: '200px', width: '100%' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie data={countryData} cx="50%" cy="50%" innerRadius={60} outerRadius={80} paddingAngle={2} dataKey="morning">
                        {countryData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                        ))}
                      </Pie>
                      <Tooltip contentStyle={{ background: '#222', border: '1px solid #333', borderRadius: '6px', fontSize: '12px' }} />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
                
                <h5 className="ui-text mb-3 mt-4" style={{ color: 'var(--gold)', fontSize: '11px', letterSpacing: '0.1em' }}>EMAIL HEALTH METRICS</h5>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '12px', fontSize: '12px', color: '#bbb' }} className="ui-text">
                  <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '4px' }}><span>Open Rate:</span> <span style={{ color: 'var(--gold)' }}>{metrics.emails.stats.openRate}</span></div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '4px' }}><span>Replies:</span> <span style={{ color: 'var(--gold)' }}>{metrics.emails.stats.replies}</span></div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '4px' }}><span>Bounce Rate:</span> <span style={{ color: '#aaa' }}>{metrics.emails.stats.bounceRate}</span></div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', borderBottom: '1px solid rgba(255,255,255,0.05)', paddingBottom: '4px' }}><span>Spam Rate:</span> <span style={{ color: '#aaa' }}>{metrics.emails.stats.spammed}</span></div>
                </div>

                <div style={{ marginTop: '24px', background: 'rgba(197, 160, 89, 0.1)', padding: '12px', borderRadius: '6px', border: '1px solid rgba(197, 160, 89, 0.2)' }}>
                  <p className="ui-text" style={{ fontSize: '10px', color: 'var(--gold)', marginBottom: '4px' }}>TOP ICP DESIGNATION</p>
                  <p style={{ fontSize: '16px', color: '#fff', fontFamily: 'var(--ff-display)' }}>Founders & CEOs <span style={{ fontSize: '12px', color: '#888', float: 'right', marginTop: '4px' }}>{metrics.leads.designation.founders + metrics.leads.designation.ceo} Leads</span></p>
                </div>
              </div>
              
            </div>
          </section>


          {/* SECTION 3: FINANCIAL LEDGER & BURN */}
          <section id="financials" style={{ background: 'var(--burgundy)', padding: '32px', borderRadius: '12px', border: '1px solid rgba(197, 160, 89, 0.2)' }}>
            <h4 className="ui-text mb-6" style={{ color: '#fff', fontSize: '14px', letterSpacing: '0.1em' }}><Target size={16} style={{ display: 'inline', marginBottom: '-3px', marginRight: '8px', color: 'var(--gold)' }}/> TARGET REVENUE MAP</h4>
            
            {/* Real Targets Table */}
            <div style={{ background: 'var(--burgundy-dark)', borderRadius: '8px', border: '1px solid rgba(197, 160, 89, 0.2)', overflow: 'hidden', marginBottom: '40px' }}>
              <table style={{ width: '100%', textAlign: 'left', borderCollapse: 'collapse' }} className="ui-text">
                <thead style={{ background: 'rgba(197, 160, 89, 0.15)' }}>
                  <tr style={{ color: 'var(--gold)', fontSize: '12px', letterSpacing: '0.1em' }}>
                    <th style={{ padding: '16px 24px' }}>MONTH</th>
                    <th style={{ padding: '16px 24px' }}>FINANCIAL YEAR</th>
                    <th style={{ padding: '16px 24px', textAlign: 'right' }}>REVENUE TARGET (₹)</th>
                  </tr>
                </thead>
                <tbody style={{ fontSize: '14px', color: '#ddd' }}>
                  {revenueTargets.map((row, idx) => (
                    <tr key={idx} style={{ borderBottom: '1px solid rgba(255,255,255,0.05)' }}>
                      <td style={{ padding: '16px 24px', fontWeight: row.month === 'Jun-26' ? 'bold' : 'normal', color: row.month === 'Jun-26' ? '#fff' : '#ddd' }}>{row.month}</td>
                      <td style={{ padding: '16px 24px' }}>{row.fy}</td>
                      <td style={{ padding: '16px 24px', textAlign: 'right', color: 'var(--gold)' }}>₹{row.target.toLocaleString('en-IN')}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
              <div>
                <h5 className="ui-text mb-4" style={{ color: 'var(--gold)', fontSize: '11px', letterSpacing: '0.1em' }}>UNIT ECONOMICS</h5>
                <div style={{ display: 'flex', gap: '12px' }}>
                  <div style={{ flex: 1, background: 'var(--burgundy-dark)', padding: '16px', borderRadius: '8px', border: '1px solid rgba(197, 160, 89, 0.2)' }}>
                    <p className="ui-text" style={{ fontSize: '10px', color: 'var(--gold)', marginBottom: '4px' }}>CAC</p>
                    <p style={{ fontSize: '24px', color: '#fff', fontFamily: 'var(--ff-display)' }}>₹{metrics.financials.unitEconomics.cac}</p>
                  </div>
                  <div style={{ flex: 1, background: 'var(--burgundy-dark)', padding: '16px', borderRadius: '8px', border: '1px solid rgba(197, 160, 89, 0.2)' }}>
                    <p className="ui-text" style={{ fontSize: '10px', color: '#aaa', marginBottom: '4px' }}>COST PER LEAD</p>
                    <p style={{ fontSize: '24px', color: '#fff', fontFamily: 'var(--ff-display)' }}>₹{metrics.financials.unitEconomics.cpl}</p>
                  </div>
                  <div style={{ flex: 1, background: 'var(--burgundy-dark)', padding: '16px', borderRadius: '8px', border: '1px solid rgba(197, 160, 89, 0.2)' }}>
                    <p className="ui-text" style={{ fontSize: '10px', color: '#aaa', marginBottom: '4px' }}>EXPENSE PER LEAD</p>
                    <p style={{ fontSize: '24px', color: '#fff', fontFamily: 'var(--ff-display)' }}>₹{metrics.financials.unitEconomics.epl}</p>
                  </div>
                </div>

                <h5 className="ui-text mb-4 mt-6" style={{ color: 'var(--gold)', fontSize: '11px', letterSpacing: '0.1em' }}>BURN RATE TRACKER</h5>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 16px', background: 'var(--burgundy-dark)', borderRadius: '6px', marginBottom: '8px' }}>
                  <span className="ui-text" style={{ color: '#aaa', fontSize: '12px' }}>Daily Burn</span>
                  <span className="ui-text" style={{ color: '#fff', fontSize: '13px' }}>₹{metrics.financials.expenses.daily.toLocaleString()}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 16px', background: 'var(--burgundy-dark)', borderRadius: '6px', marginBottom: '8px' }}>
                  <span className="ui-text" style={{ color: '#aaa', fontSize: '12px' }}>Weekly Burn</span>
                  <span className="ui-text" style={{ color: '#fff', fontSize: '13px' }}>₹{metrics.financials.expenses.weekly.toLocaleString()}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', padding: '12px 16px', background: 'var(--burgundy-dark)', borderRadius: '6px' }}>
                  <span className="ui-text" style={{ color: '#aaa', fontSize: '12px' }}>Monthly Burn</span>
                  <span className="ui-text" style={{ color: 'var(--gold)', fontSize: '13px', fontWeight: 'bold' }}>₹{metrics.financials.expenses.monthly.toLocaleString()}</span>
                </div>
              </div>

              <div>
                 <h5 className="ui-text mb-4" style={{ color: 'var(--gold)', fontSize: '11px', letterSpacing: '0.1em' }}>MONTHLY OPEX BREAKDOWN</h5>
                 <ResponsiveContainer width="100%" height={250}>
                    <BarChart data={[
                      { name: 'Marketing', cost: metrics.financials.expenses.breakdown.marketing },
                      { name: 'APIs/Infra', cost: metrics.financials.expenses.breakdown.api_systems },
                      { name: 'Workspace (Zoho)', cost: metrics.financials.expenses.breakdown.workspace_zoho },
                      { name: 'Misc OPEX', cost: metrics.financials.expenses.breakdown.other },
                    ]} layout="vertical" margin={{ left: 40 }}>
                      <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.05)" horizontal={true} vertical={false} />
                      <XAxis type="number" stroke="#666" tick={{ fill: '#666', fontSize: 10 }} axisLine={false} tickLine={false} />
                      <YAxis dataKey="name" type="category" stroke="#888" tick={{ fill: '#888', fontSize: 11 }} axisLine={false} tickLine={false} />
                      <Tooltip contentStyle={{ background: '#222', border: '1px solid #333', borderRadius: '6px', fontSize: '12px' }} cursor={{ fill: '#1a1a1a' }} />
                      <Bar dataKey="cost" fill="var(--gold)" radius={[0, 4, 4, 0]} barSize={20} />
                    </BarChart>
                  </ResponsiveContainer>
              </div>
            </div>
          </section>

        </div>
      </main>

      <style>{`
        @keyframes pulse {
          0% { opacity: 1; }
          50% { opacity: 0.4; }
          100% { opacity: 1; }
        }
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--burgundy-dark); }
        ::-webkit-scrollbar-thumb { background: var(--burgundy); border: 1px solid rgba(197, 160, 89, 0.2); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: rgba(197, 160, 89, 0.5); }
      `}</style>
    </div>
  );
}
