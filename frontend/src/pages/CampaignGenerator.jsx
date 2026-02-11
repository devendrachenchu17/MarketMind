import React, { useState } from 'react';
import { generateCampaign } from '../services/api';
import '../styles/CampaignGenerator.css';
import { Loader2, Copy, Check } from 'lucide-react';

// Helper Component for Video/Image
const MediaDisplay = ({ url, isVideo, style, keyword }) => {
    const [imgSrc, setImgSrc] = React.useState(url);

    React.useEffect(() => {
        setImgSrc(url);
    }, [url]);

    if (!imgSrc) return <div style={{ padding: '20px', background: '#222', textAlign: 'center', color: '#555' }}>No Media</div>;

    if (isVideo || imgSrc.toString().endsWith('.mp4')) {
        return (
            <video controls autoPlay loop muted style={style}>
                <source src={imgSrc} type="video/mp4" />
            </video>
        );
    }

    const handleError = (e) => {
        console.log("Image failed to load:", imgSrc);
        // Fallback to a relevant placeholder if the AI image fails
        if (imgSrc && !imgSrc.includes('loremflickr.com')) {
            const searchTerm = keyword ? keyword.replace(/\s+/g, ',') : 'product';
            setImgSrc(`https://loremflickr.com/1024/1024/${searchTerm}?random=${Math.floor(Math.random() * 1000)}`);
        }
    };

    return <img src={imgSrc} onError={handleError} alt="Content" style={style} />;
};



const CampaignGenerator = () => {
    const [formData, setFormData] = useState({
        product_name: '',
        product_description: '',
        target_audience: '',
        platforms: ['LinkedIn', 'Twitter', 'Instagram'],
        tone: 'Professional'
    });
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleInputChange = (e) => {
        const { name, value } = e.target;
        setFormData(prev => ({ ...prev, [name]: value }));
    };

    const handlePlatformChange = (e) => {
        const { value, checked } = e.target;
        setFormData(prev => {
            if (checked) return { ...prev, platforms: [...prev.platforms, value] };
            return { ...prev, platforms: prev.platforms.filter(p => p !== value) };
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');
        setResult(null);

        try {
            const response = await generateCampaign(formData);
            setResult(response);
        } catch (err) {
            setError(err.detail || 'Failed to generate campaign. Please check backend.');
        } finally {
            setLoading(false);
        }
    };

    const renderCard = (item, index) => {
        const platform = item.platform.toLowerCase();

        // Instagram Layout
        if (platform === 'instagram') {
            return (
                <div key={index} className="content-card instagram-card">
                    <div className="insta-header">
                        <div className="insta-avatar"></div>
                        <div className="insta-username">MarketMind_AI</div>
                    </div>
                    <div className="insta-media-container">
                        <MediaDisplay
                            url={item.media_url}
                            isVideo={item.visual_prompt.toLowerCase().includes('video')}
                            style={{ width: '100%', display: 'block' }}
                            keyword={formData.product_name}
                        />
                    </div>
                    <div className="insta-actions">
                        {/* Simple SVG icons for Like, Comment, Share */}
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2"><path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"></path></svg>
                        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="white" strokeWidth="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
                    </div>
                    <div className="insta-caption">
                        <strong>MarketMind_AI</strong>
                        <span style={{ whiteSpace: 'pre-line' }}>{item.content}</span>
                        <div style={{ color: '#999', fontSize: '12px', marginTop: '5px' }}>
                            {item.hashtags.join(' ')}
                        </div>
                    </div>
                    <div className="xai-box">
                        <span className="xai-label">AI Strategy</span>
                        {item.xai_explanation}
                    </div>
                </div>
            );
        }

        // LinkedIn Layout
        if (platform === 'linkedin') {
            return (
                <div key={index} className="content-card linkedin-card">
                    <div className="linkedin-header">
                        <div className="linkedin-avatar">MM</div>
                        <div className="linkedin-info">
                            <h4>MarketMind AI Platform</h4>
                            <span>12,453 followers • Just now • 🌐</span>
                        </div>
                    </div>
                    <div className="linkedin-content">
                        {item.content}
                        <br /><br />
                        <span style={{ color: '#0a66c2', fontWeight: '600' }}>{item.hashtags.join(' ')}</span>
                    </div>
                    <div className="linkedin-media-container">
                        <MediaDisplay
                            url={item.media_url}
                            isVideo={false}
                            style={{ width: '100%', display: 'block' }}
                            keyword={formData.product_name}
                        />
                    </div>
                    <div className="linkedin-actions">
                        <button className="linkedin-btn">Like</button>
                        <button className="linkedin-btn">Comment</button>
                        <button className="linkedin-btn">Repost</button>
                        <button className="linkedin-btn">Send</button>
                    </div>
                    <div className="xai-box" style={{ margin: '0', border: 'none', borderTop: '1px solid #e0e0e0', background: '#f3f2ef', borderRadius: '0', color: '#555' }}>
                        <span className="xai-label" style={{ color: '#0a66c2' }}>Why this works</span>
                        {item.xai_explanation}
                    </div>
                </div>
            );
        }

        // Poster Layout
        if (platform.toLowerCase().includes('poster')) {
            return (
                <div key={index} className="content-card poster-card">
                    <div className="poster-media">
                        <MediaDisplay
                            url={item.media_url}
                            isVideo={false}
                            style={{ width: '100%', height: '100%', objectFit: 'cover' }}
                            keyword={formData.product_name}
                        />
                        <div className="poster-overlay">
                            {/* Attempt to parse content for headline/subhead if structured, else dump text */}
                            <div className="poster-headline">{item.content.split('\n')[0].replace('HEADLINE:', '')}</div>
                            <div className="poster-subhead">{item.content.split('\n')[1]?.replace('SUBHEAD:', '') || ''}</div>
                            <div style={{ marginTop: '1rem', padding: '0.5rem 1rem', border: '1px solid #fbbf24', display: 'inline-block', color: '#fbbf24', fontSize: '0.8rem', letterSpacing: '1px' }}>
                                {item.content.split('\n')[2]?.replace('CTA:', '') || 'LEARN MORE'}
                            </div>
                        </div>
                    </div>
                </div>
            );
        }

        // Default / Twitter Layout
        return (
            <div key={index} className="content-card twitter-card">
                <div className="twitter-header">
                    <div className="twitter-avatar"></div>
                    <div>
                        <span className="twitter-name">MarketMind</span>
                        <span className="twitter-handle">@MarketMindAI</span>
                    </div>
                </div>
                <div className="twitter-text">
                    {item.content}
                    <div style={{ color: '#1d9bf0', marginTop: '5px' }}>
                        {item.hashtags.join(' ')}
                    </div>
                </div>
                {item.media_url && (
                    <div className="twitter-media">
                        <MediaDisplay
                            url={item.media_url}
                            isVideo={item.visual_prompt?.toLowerCase().includes('video')}
                            style={{ width: '100%', display: 'block' }}
                            keyword={formData.product_name}
                        />
                    </div>
                )}
                <div className="xai-box" style={{ background: '#111', borderColor: '#333' }}>
                    <span className="xai-label">Rationale</span>
                    {item.xai_explanation}
                </div>
            </div>
        );
    };

    return (
        <div className="campaign-container">
            <header className="campaign-header">
                <h1>AI Campaign Generator</h1>
                <p>Create platform-specific content with transparent AI reasoning.</p>
            </header>

            <form onSubmit={handleSubmit} className="campaign-form">
                <div className="form-group">
                    <label>Product / Service Name</label>
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
                    <label>Description</label>
                    <textarea
                        name="product_description"
                        className="form-textarea"
                        rows="3"
                        value={formData.product_description}
                        onChange={handleInputChange}
                        required
                        placeholder="Key features and value proposition..."
                    />
                </div>

                <div className="form-group">
                    <label>Target Audience</label>
                    <input
                        type="text"
                        name="target_audience"
                        className="form-input"
                        value={formData.target_audience}
                        onChange={handleInputChange}
                        required
                        placeholder="e.g. B2B Marketing Managers"
                    />
                </div>

                <div className="form-group">
                    <label>Platforms</label>
                    <div className="checkbox-group">
                        {['LinkedIn', 'Twitter', 'Instagram', 'Facebook', 'Marketing Poster'].map(p => (
                            <label key={p} style={{ display: 'inline-flex', alignItems: 'center', marginRight: '1rem', cursor: 'pointer', color: '#fff' }}>
                                <input
                                    type="checkbox"
                                    value={p}
                                    checked={formData.platforms.includes(p)}
                                    onChange={handlePlatformChange}
                                    style={{ marginRight: '0.5rem' }}
                                />
                                {p}
                            </label>
                        ))}
                    </div>
                </div>

                <button type="submit" className="btn-primary" disabled={loading}>
                    {loading ? <><Loader2 className="animate-spin" style={{ display: 'inline', marginRight: '0.5rem' }} /> Generating Strategy...</> : 'Generate Campaign'}
                </button>
            </form>

            {error && <div style={{ color: '#ef4444', background: 'rgba(239, 68, 68, 0.1)', padding: '1rem', borderRadius: '8px', marginBottom: '2rem' }}>{error}</div>}

            {result && (
                <div className="results-container">
                    <div style={{ marginBottom: '2rem', padding: '1.5rem', background: 'rgba(59, 130, 246, 0.1)', borderRadius: '12px', border: '1px solid rgba(59, 130, 246, 0.2)' }}>
                        <h3 style={{ color: '#93c5fd', marginBottom: '0.5rem' }}>Strategy Overview</h3>
                        <p>{result.strategy_explanation}</p>
                    </div>

                    <div className="results-section">
                        {result.generated_content.map((item, index) => renderCard(item, index))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default CampaignGenerator;
