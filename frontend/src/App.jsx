import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import CampaignGenerator from './pages/CampaignGenerator';
import SalesPitch from './pages/SalesPitch';
import LeadScoring from './pages/LeadScoring';
import './styles/global.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Dashboard />}>
          <Route index element={<Navigate to="/campaigns" replace />} />
          <Route path="campaigns" element={<CampaignGenerator />} />
          <Route path="sales-pitch" element={<SalesPitch />} />
          <Route path="lead-scoring" element={<LeadScoring />} />
        </Route>
      </Routes>
    </Router>
  );
}


export default App;
