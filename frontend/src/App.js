import React, { useState, useEffect } from 'react';
import './App.css';
import ScraperAPI from './services/api';
import { 
  Globe, 
  Download, 
  CheckCircle, 
  Loader, 
  Sparkles,
  Clock,
  FileText,
  Eye
} from 'lucide-react';

function App() {
  const [url, setUrl] = useState('');
  const [depth, setDepth] = useState(0);
  const [llmEnabled, setLlmEnabled] = useState(true);
  const [filename, setFilename] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [result, setResult] = useState(null);
  const [apiStatus, setApiStatus] = useState('checking');
  const [history, setHistory] = useState([]);

  // Check API health on mount
  useEffect(() => {
    checkApiHealth();
    loadHistory();
  }, []);

  const checkApiHealth = async () => {
    try {
      console.log('Checking API health...');
      const response = await ScraperAPI.healthCheck();
      console.log('API health response:', response);
      setApiStatus('online');
    } catch (error) {
      console.error('API health check failed:', error);
      setApiStatus('offline');
    }
  };

  const loadHistory = async () => {
    try {
      const data = await ScraperAPI.listResults();
      setHistory(data.results || []);
    } catch (error) {
      console.error('Failed to load history:', error);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setResult(null);
    
    if (!url.trim()) {
      setError('Please enter a URL');
      return;
    }

    if (!url.startsWith('http://') && !url.startsWith('https://')) {
      setError('URL must start with http:// or https://');
      return;
    }

    setLoading(true);

    try {
      const response = await ScraperAPI.scrapeWebsite(
        url.trim(),
        depth,
        llmEnabled,
        filename.trim()
      );
      
      setResult(response);
      setUrl('');
      setFilename('');
      
      // Reload history
      loadHistory();
    } catch (err) {
      setError(err.error || err.message || 'Failed to scrape website. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleDownload = (resultId) => {
    const downloadUrl = ScraperAPI.getDownloadUrl(resultId);
    window.open(downloadUrl, '_blank');
  };

  const handleViewResult = async (resultId) => {
    try {
      const data = await ScraperAPI.getResultDetails(resultId);
      setResult({
        ...data,
        content_preview: data.content
      });
    } catch (error) {
      setError('Failed to load result details');
    }
  };

  return (
    <div className="app">
      <div className="container">
        {/* Header */}
        <header className="header">
          <div className="header-icon">
            <Globe size={60} color="#667eea" />
          </div>
          <h1>Crystal Scraper</h1>
          <p>Advanced Website Content Extraction Tool</p>
        </header>

        {/* Main Content */}
        <div className="main-content">
          {/* Scraper Form */}
          <div className="card">
            <h2>
              <Sparkles size={24} color="#667eea" />
              Scrape Website
            </h2>
            
            {error && (
              <div className="error">
                <strong>Error:</strong> {error}
              </div>
            )}

            <form onSubmit={handleSubmit}>
              <div className="form-group">
                <label htmlFor="url">Website URL *</label>
                <input
                  type="text"
                  id="url"
                  className="form-input"
                  placeholder="https://example.com"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  disabled={loading}
                />
                <p className="help-text">Enter the URL you want to scrape</p>
              </div>

              <div className="form-group">
                <label htmlFor="depth">Scraping Depth</label>
                <select
                  id="depth"
                  className="form-select"
                  value={depth}
                  onChange={(e) => setDepth(parseInt(e.target.value))}
                  disabled={loading}
                >
                  <option value={0}>0 - Single page only (fastest)</option>
                  <option value={1}>1 - Include linked pages (1 level deep)</option>
                  <option value={2}>2 - Include linked pages (2 levels deep)</option>
                </select>
                <p className="help-text">How deep to follow links from the main page</p>
              </div>

              <div className="form-group">
                <label htmlFor="filename">Custom Filename (Optional)</label>
                <input
                  type="text"
                  id="filename"
                  className="form-input"
                  placeholder="my-scraped-content"
                  value={filename}
                  onChange={(e) => setFilename(e.target.value)}
                  disabled={loading}
                />
                <p className="help-text">Leave empty for auto-generated filename</p>
              </div>

              <div className="form-group">
                <div className="checkbox-group">
                  <input
                    type="checkbox"
                    id="llm"
                    className="checkbox-input"
                    checked={llmEnabled}
                    onChange={(e) => setLlmEnabled(e.target.checked)}
                    disabled={loading}
                  />
                  <label htmlFor="llm">Use AI formatting (removes HTML/CSS)</label>
                </div>
                <p className="help-text">Clean and format the content automatically</p>
              </div>

              <button
                type="submit"
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? (
                  <>
                    <Loader className="spinner" size={20} />
                    Scraping...
                  </>
                ) : (
                  <>
                    <Globe size={20} />
                    Start Scraping
                  </>
                )}
              </button>
            </form>
          </div>

          {/* Result Preview */}
          {result && (
            <div className="card">
              <h2>
                <CheckCircle size={24} color="#48bb78" />
                Scraping Complete!
              </h2>
              
              <div className="success">
                Successfully scraped and saved!
              </div>

              <div className="result-stats">
                <div className="stat-item">
                  <div className="stat-label">Scrape Time</div>
                  <div className="stat-value">{result.scrape_time?.toFixed(2)}s</div>
                </div>
                <div className="stat-item">
                  <div className="stat-label">Content Length</div>
                  <div className="stat-value">{result.total_length?.toLocaleString()}</div>
                </div>
                {result.metadata?.total_pages && (
                  <div className="stat-item">
                    <div className="stat-label">Pages</div>
                    <div className="stat-value">{result.metadata.total_pages}</div>
                  </div>
                )}
              </div>

              <div className="result-preview">
                <h3>
                  <FileText size={20} />
                  {result.title}
                </h3>
                <div className="content-text">
                  {result.content_preview || result.content}
                </div>
              </div>

              <button
                onClick={() => handleDownload(result.result_id)}
                className="btn btn-secondary"
                style={{ marginTop: '20px' }}
              >
                <Download size={20} />
                Download File
              </button>
            </div>
          )}

          {loading && !result && (
            <div className="card">
              <div className="loading">
                <div className="spinner"></div>
                <p>Scraping in progress... This may take a few moments.</p>
              </div>
            </div>
          )}

          {/* History */}
          {history.length > 0 && (
            <div className="card full-width-card">
              <h2>
                <Clock size={24} color="#667eea" />
                Recent Scrapes
              </h2>
              
              <div className="history-list">
                {history.map((item) => (
                  <div key={item.result_id} className="history-item">
                    <div className="history-info">
                      <div className="history-url">{item.url}</div>
                      <div className="history-meta">
                        {new Date(item.timestamp).toLocaleString()} • 
                        {' '}{(item.file_size / 1024).toFixed(2)} KB
                      </div>
                    </div>
                    <div className="history-actions">
                      <button
                        onClick={() => handleViewResult(item.result_id)}
                        className="btn-small btn-view"
                      >
                        <Eye size={16} />
                        View
                      </button>
                      <button
                        onClick={() => handleDownload(item.result_id)}
                        className="btn-small btn-download"
                      >
                        <Download size={16} />
                        Download
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* API Status Indicator */}
        <div className="api-status">
          <div className={`status-indicator ${apiStatus === 'offline' ? 'offline' : ''}`}></div>
          API {apiStatus === 'online' ? 'Online' : 'Offline'}
        </div>
      </div>
    </div>
  );
}

export default App;
