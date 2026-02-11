import React, { useState } from 'react';
import { generatePitch } from '../services/api';
import '../styles/SalesPitch.css';
import { Loader2, Copy, Check, MessageSquare } from 'lucide-react';

const SalesPitch = () => {
    const [formData, setFormData] = useState({
        product_name: '',
        product_description: '',
        persona: '',
        industry: '',
        tone: 'Professional'
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [copiedIndex, setCopiedIndex] = useState(null);

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
            const response = await generatePitch(formData);
            setResult(response);
        } catch (err) {
            setError(err.detail || 'Failed to generate pitch. Please check backend.');
        } finally {
            setLoading(false);
        }
    };

    const copyToClipboard = (text, index) => {
        navigator.clipboard.writeText(text);
        setCopiedIndex(index);
        setTimeout(() => setCopiedIndex(null), 2000);
    };

    return (
        <div className="pitch-container">
            <header className="pitch-header">
                <h1>Sales Pitch Generator</h1>
                <p>Craft personalized outreach that converts.</p>
            </header>

            <form onSubmit={handleSubmit} className="pitch-form">
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1.5rem' }}>
                    <div className="form-group">
                        <label>Product Name</label>
                        <input
                            type="text"
                            name="product_name"
                            className="form-input"
                            value={formData.product_name}
                            onChange={handleInputChange}
                            required
                            placeholder="e.g. MarketMind AI"
                        />
                    </div>
                    <div className="form-group">
                        <label>Industry</label>
                        <input
                            type="text"
                            name="industry"
                            className="form-input"
                            value={formData.industry}
                            onChange={handleInputChange}
                            required
                            placeholder="e.g. SaaS, Healthcare"
                        />
                    </div>
                </div>

                <div className="form-group">
                    <label>Target Persona</label>
                    <input
                        type="text"
                        name="persona"
                        className="form-input"
                        value={formData.persona}
                        onChange={handleInputChange}
                        required
                        placeholder="e.g. CTO, VP of Sales"
                    />
                </div>

                <div className="form-group">
                    <label>Product Description & Value Prop</label>
                    <textarea
                        name="product_description"
                        className="form-textarea"
                        rows="3"
                        value={formData.product_description}
                        onChange={handleInputChange}
                        required
                        placeholder="What problem does it solve?"
                    />
                </div>

                <div className="form-group">
                    <label>Tone</label>
                    <select name="tone" className="form-select" value={formData.tone} onChange={handleInputChange}>
                        <option>Professional</option>
                        <option>Friendly</option>
                        <option>Urgent</option>
                        <option>Persuasive</option>
                    </select>
                </div>

                <button type="submit" className="btn-primary" disabled={loading} style={{ background: 'linear-gradient(90deg, #c084fc, #ec4899)' }}>
                    {loading ? <><Loader2 className="animate-spin" style={{ display: 'inline', marginRight: '0.5rem' }} /> Crafting Pitch...</> : 'Generate Pitches'}
                </button>
            </form>

            {error && <div style={{ color: '#ef4444', background: 'rgba(239, 68, 68, 0.1)', padding: '1rem', borderRadius: '8px', marginBottom: '2rem' }}>{error}</div>}

            {result && (
                <div className="results-container">
                    <div style={{ marginBottom: '2rem', padding: '1.5rem', background: 'rgba(236, 72, 153, 0.1)', borderRadius: '12px', border: '1px solid rgba(236, 72, 153, 0.2)' }}>
                        <h3 style={{ color: '#f9a8d4', marginBottom: '0.5rem' }}>Strategy Insight</h3>
                        <p>{result.strategy_explanation}</p>
                    </div>

                    {result.variants.map((variant, index) => (
                        <div key={index} className="variant-card">
                            <div className="variant-header">
                                <span className="variant-type"><MessageSquare size={16} style={{ marginRight: '0.5rem', display: 'inline' }} /> {variant.variant_type}</span>
                                <button className="btn-secondary" onClick={() => copyToClipboard(variant.content, index)}>
                                    {copiedIndex === index ? <Check size={14} /> : <Copy size={14} />}
                                    {copiedIndex === index ? 'Copied' : 'Copy'}
                                </button>
                            </div>

                            {variant.subject_line && (
                                <div style={{ marginBottom: '0.5rem', color: '#e2e8f0', fontWeight: '500' }}>
                                    Subject: {variant.subject_line}
                                </div>
                            )}

                            <div className="pitch-content">
                                {variant.content}
                            </div>

                            <div className="xai-box" style={{ borderColor: '#ec4899', color: '#face15', background: 'rgba(236, 72, 153, 0.05)' }}>
                                <span className="xai-label" style={{ color: '#ec4899' }}>Why this works</span>
                                {variant.xai_explanation}
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
};

export default SalesPitch;
