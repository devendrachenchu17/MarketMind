import React, { useState } from 'react';
import { scoreLead } from '../services/api';
import '../styles/LeadScoring.css';
import { Loader2, TrendingUp, CheckCircle, AlertTriangle } from 'lucide-react';

const LeadScoring = () => {
    const [formData, setFormData] = useState({
        name: '',
        company: '',
        budget: '',
        urgency: 'Medium',
        needs: '',
        notes: ''
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);

        try {
            const response = await scoreLead(formData);
            setResult(response);
        } catch (err) {
            setError(err.detail || 'Failed to analyze lead.');
        } finally {
            setLoading(false);
        }
    };

    const getScoreColor = (score) => {
        if (score >= 80) return '#10b981'; // Green
        if (score >= 50) return '#f59e0b'; // Yellow
        return '#ef4444'; // Red
    };

    return (
        <div className="lead-container">
            <header className="lead-header">
                <h1>AI Lead Scoring</h1>
                <p>Qualify leads instantly with predictive intelligence.</p>
            </header>

            <div className="lead-dashboard">
                <form onSubmit={handleSubmit} className="lead-form">
                    <h3 style={{ marginBottom: '1.5rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '0.5rem' }}>Lead Details</h3>
                    <div className="form-group">
                        <label>Lead Name</label>
                        <input type="text" name="name" className="form-input" value={formData.name} onChange={handleInputChange} required placeholder="John Doe" />
                    </div>
                    <div className="form-group">
                        <label>Company</label>
                        <input type="text" name="company" className="form-input" value={formData.company} onChange={handleInputChange} required placeholder="Acme Corp" />
                    </div>
                    <div className="form-group">
                        <label>Budget</label>
                        <input type="text" name="budget" className="form-input" value={formData.budget} onChange={handleInputChange} required placeholder="$50k - $100k" />
                    </div>
                    <div className="form-group">
                        <label>Urgency</label>
                        <select name="urgency" className="form-select" value={formData.urgency} onChange={handleInputChange}>
                            <option>Low</option>
                            <option>Medium</option>
                            <option>High</option>
                        </select>
                    </div>
                    <div className="form-group">
                        <label>Business Needs</label>
                        <textarea name="needs" className="form-textarea" rows="2" value={formData.needs} onChange={handleInputChange} required placeholder="Looking to automate X..." />
                    </div>
                    <button type="submit" className="btn-primary" disabled={loading} style={{ background: 'linear-gradient(90deg, #f59e0b, #d97706)' }}>
                        {loading ? <><Loader2 className="animate-spin" style={{ display: 'inline', marginRight: '0.5rem' }} /> Analyzing...</> : 'Analyze Lead'}
                    </button>
                    {error && <p style={{ color: '#ef4444', marginTop: '1rem' }}>{error}</p>}
                </form>

                <div className="results-panel">
                    {result ? (
                        <>
                            <div className="score-display">
                                <div className="score-circle" style={{ borderColor: getScoreColor(result.score), color: getScoreColor(result.score) }}>
                                    {result.score}
                                </div>
                                <h3>{result.priority} Priority</h3>
                                <p style={{ color: '#a0a0a0' }}>Conversion Probability: <span style={{ color: getScoreColor(result.score) }}>{result.conversion_probability}</span></p>
                            </div>

                            <div className="summary-box">
                                "{result.qualification_summary}"
                            </div>

                            <div className="recommendations">
                                <h4>Recommended Actions</h4>
                                <ul>
                                    {result.recommended_actions.map((action, i) => (
                                        <li key={i}><CheckCircle size={16} color="#10b981" /> {action}</li>
                                    ))}
                                </ul>
                            </div>

                            <div className="xai-box" style={{ borderColor: '#f59e0b', color: '#f59e0b', background: 'rgba(245, 158, 11, 0.05)' }}>
                                <span className="xai-label" style={{ color: '#f59e0b' }}>Score Reasoning</span>
                                {result.xai_explanation}
                            </div>
                        </>
                    ) : (
                        <div style={{ height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: '#64748b', flexDirection: 'column' }}>
                            <TrendingUp size={48} style={{ opacity: 0.5, marginBottom: '1rem' }} />
                            <p>Enter lead details to generate a predictive score.</p>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default LeadScoring;
