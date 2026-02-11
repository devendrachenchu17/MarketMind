import React from 'react';
import { Link, Outlet, useLocation } from 'react-router-dom';
import { LayoutDashboard, Megaphone, Mic2, Target, Settings } from 'lucide-react';
import '../styles/Dashboard.css';

const Dashboard = () => {
    const location = useLocation();

    const isActive = (path) => {
        return location.pathname.includes(path) ? 'nav-item active' : 'nav-item';
    };

    return (
        <div className="dashboard-layout">
            <aside className="sidebar">
                <div className="sidebar-header">
                    <h2>MarketMind</h2>
                </div>
                <nav className="sidebar-nav">
                    <Link to="/campaigns" className={isActive('campaigns')}>
                        <Megaphone size={20} />
                        <span>Campaign Generator</span>
                    </Link>
                    <Link to="/sales-pitch" className={isActive('sales-pitch')}>
                        <Mic2 size={20} />
                        <span>Sales Pitch</span>
                    </Link>
                    <Link to="/lead-scoring" className={isActive('lead-scoring')}>
                        <Target size={20} />
                        <span>Lead Scoring</span>
                    </Link>
                    <div style={{ marginTop: 'auto' }}>
                        <Link to="/settings" className={isActive('settings')}>
                            <Settings size={20} />
                            <span>Settings</span>
                        </Link>
                    </div>
                </nav>
            </aside>
            <main className="main-content">
                <Outlet />
            </main>
        </div>
    );
};

export default Dashboard;
