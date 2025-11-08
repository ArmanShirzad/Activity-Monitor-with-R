import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Dashboard from './components/Dashboard';
import PlatformSelector from './components/PlatformSelector';
import ActivityCharts from './components/ActivityCharts';
import './App.css';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

function App() {
  const [platforms, setPlatforms] = useState([]);
  const [selectedPlatform, setSelectedPlatform] = useState(null);
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchPlatforms = async () => {
    try {
      const response = await axios.get(`${API_URL}/api/v1/platforms`);
      setPlatforms(response.data.platforms);
      return response.data.platforms;
    } catch (err) {
      setError('Failed to load platforms');
      console.error(err);
      return [];
    }
  };

  const handlePlatformConnect = useCallback(async (platform, credentials) => {
    setLoading(true);
    setError(null);
    
    try {
      // Calculate date range (last 3 days to minimize API calls)
      // Fitbit rate limit is 150 requests/hour - server-side restriction
      const endDate = new Date();
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - 3);
      
      const response = await axios.post(`${API_URL}/api/v1/activity/analyze`, {
        platform: platform.id,
        start_date: startDate.toISOString().split('T')[0],
        end_date: endDate.toISOString().split('T')[0],
        access_token: credentials.accessToken,
        refresh_token: credentials.refreshToken
      });
      
      setAnalysisData(response.data);
      setSelectedPlatform(platform);
    } catch (err) {
      setError('Failed to analyze activity data: ' + (err.response?.data?.detail || err.message));
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    // Check for OAuth callback parameters first
    const urlParams = new URLSearchParams(window.location.search);
    const accessToken = urlParams.get('access_token');
    const refreshToken = urlParams.get('refresh_token');
    const platform = urlParams.get('platform');
    const errorParam = urlParams.get('error');
    
    if (errorParam) {
      setError(`OAuth Error: ${urlParams.get('error_description') || errorParam}`);
      // Clean URL
      window.history.replaceState({}, document.title, window.location.pathname);
      fetchPlatforms();
      return;
    }
    
    // Fetch supported platforms
    fetchPlatforms().then((platformsList) => {
      if (accessToken && refreshToken && platform) {
        // OAuth callback successful - find platform and connect
        const platformObj = platformsList.find(p => p.id === platform);
        if (platformObj) {
          handlePlatformConnect(
            platformObj,
            { accessToken, refreshToken }
          );
        }
        
        // Clean URL
        window.history.replaceState({}, document.title, window.location.pathname);
      }
    });
  }, [handlePlatformConnect]);


  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <header className="bg-white shadow-sm">
        <div className="container mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">
            Activity Monitor
          </h1>
          <p className="text-gray-600 mt-2">
            Multi-device activity tracking and analytics
          </p>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-6">
            {error}
          </div>
        )}

        {!selectedPlatform ? (
          <PlatformSelector
            platforms={platforms}
            onPlatformSelect={handlePlatformConnect}
            loading={loading}
          />
        ) : (
          <div>
            <button
              onClick={() => {
                setSelectedPlatform(null);
                setAnalysisData(null);
              }}
              className="mb-4 text-blue-600 hover:text-blue-800"
            >
              ← Connect Different Platform
            </button>

            {analysisData && (
              <Dashboard
                data={analysisData}
                platform={selectedPlatform}
              />
            )}

            {analysisData && (
              <ActivityCharts
                data={analysisData}
              />
            )}
          </div>
        )}
      </main>

      <footer className="bg-gray-800 text-white mt-12">
        <div className="container mx-auto px-4 py-6 text-center">
          <p>Activity Monitor - Marketplace Edition</p>
          <p className="text-sm text-gray-400 mt-2">
            Powered by advanced statistical analysis
          </p>
        </div>
      </footer>
    </div>
  );
}

export default App;

