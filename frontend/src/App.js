import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const [translated, setTranslated] = useState('');
  const [loading, setLoading] = useState(false);
  const [sourceLang, setSourceLang] = useState('en');
  const [targetLang, setTargetLang] = useState('de');
  const [apiUrl, setApiUrl] = useState('http://localhost:8000'); // fallback
  const [languages, setLanguages] = useState({
    en: 'English',
    de: 'German',
    fr: 'French',
    es: 'Spanish',
    it: 'Italian',
    pt: 'Portuguese',
    ru: 'Russian',
    zh: 'Chinese'
  });

  // Fetch supported languages from backend
  const fetchLanguages = async () => {
    try {
      // Use relative path for nginx proxy
      const response = await fetch('/api/languages');
      if (response.ok) {
        const data = await response.json();
        setLanguages(data);
      }
    } catch (error) {
      console.error('Failed to fetch languages:', error);
    }
  };

  // Load supported languages on component mount
  useEffect(() => {
    fetchLanguages();
  }, []);

  const handleTranslate = async () => {
    if (!text.trim()) {
      alert('Please enter text to translate');
      return;
    }
    
    setLoading(true);
    setTranslated('');
    
    try {
      // Use relative path for nginx proxy
      const response = await fetch('/api/translate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
          text,
          target_lang: targetLang  // Only send target language, as source is always English for now
        }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || 'Translation failed');
      }

      const data = await response.json();
      setTranslated(data.translated_text);
    } catch (error) {
      console.error('Translation error:', error);
      setTranslated(`Error: ${error.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleClear = () => {
    setText('');
    setTranslated('');
  };

  const handleCopy = () => {
    if (!translated) return;
    navigator.clipboard.writeText(translated);
    alert('Translated text copied to clipboard!');
  };

  return (
    <div className="app-container">
      <div className="header">
        <h1>AI TRANSLATOR test2  </h1>
        <div className="language-selectors">
          <div className="language-selector-container">
            <label>From:</label>
            <select 
              value={sourceLang} 
              onChange={(e) => setSourceLang(e.target.value)}
              className="language-selector"
              disabled={true}  // Currently only English is supported as source
            >
              <option value="en">English</option>
            </select>
          </div>
          
          <div className="language-selector-container">
            <label>To:</label>
            <select 
              value={targetLang} 
              onChange={(e) => setTargetLang(e.target.value)}
              className="language-selector"
            >
              {Object.entries(languages).map(([code, name]) => (
                code !== 'en' && (
                  <option key={code} value={code}>
                    {name} ({code.toUpperCase()})
                  </option>
                )
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="translation-container">
        <div className="input-section">
          <textarea
            rows="6"
            placeholder="Enter text to translate..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            className="text-input"
          />
          <div className="button-group">
            <button 
              onClick={handleTranslate} 
              disabled={loading || !text.trim()}
              className="action-button translate-button"
            >
              {loading ? 'Translating...' : 'Translate'}
            </button>
            <button 
              onClick={handleClear} 
              disabled={!text.trim()}
              className="action-button clear-button"
            >
              Clear
            </button>
          </div>
        </div>

        <div className="output-section">
          <h3>Translated Text:</h3>
          <div className="translated-text">
            {translated || 'No translation yet'}
          </div>
          <button 
            onClick={handleCopy} 
            disabled={!translated}
            className="action-button copy-button"
          >
            Copy to Clipboard
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;
