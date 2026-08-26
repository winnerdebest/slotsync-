import React from 'react';
import { 
  LayoutDashboard, 
  UserCheck, 
  Clock, 
  Calendar, 
  Users,
  Settings,
  Sparkles,
  Server,
  Activity
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab, backendStatus, onLogout }) {
  const navItems = [
    { id: 'dashboard', label: 'Admin Overview', icon: LayoutDashboard },
    { id: 'creators', label: 'Creator Profiles', icon: UserCheck },
    { id: 'availability', label: 'Availability Rules', icon: Clock },
    { id: 'appointments', label: 'All Appointments', icon: Calendar },
    { id: 'users', label: 'User Accounts', icon: Users },
    { id: 'settings', label: 'Server Settings', icon: Settings },
  ];

  return (
    <aside className="consult-sidebar">
      {/* Brand Header */}
      <div className="brand-header">
        <div className="brand-logo-icon">
          <Sparkles size={22} />
        </div>
        <div>
          <span className="brand-title">SLOTSYNC</span>
          <div style={{ fontSize: '0.675rem', color: 'var(--text-dim)', fontWeight: 700, letterSpacing: '0.08em' }}>
            ADMIN PORTAL
          </div>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="sidebar-nav-menu">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              className={`sidebar-link ${isActive ? 'active' : ''}`}
              onClick={() => setActiveTab(item.id)}
            >
              <Icon className="link-icon" size={19} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      {/* Admin Engine Status Widget */}
      <div className="pro-upgrade-card" style={{ background: '#f8fafc', border: '1px solid #e2e8f0' }}>
        <button className="btn-upgrade" onClick={onLogout}
          style={{ background: 'linear-gradient(135deg, #ef4444, #f97316)' }}
        >
          Sign Out
        </button>
      </div>
    </aside>
  );
}
