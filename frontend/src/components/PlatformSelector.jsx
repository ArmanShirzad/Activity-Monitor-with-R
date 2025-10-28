import React, { useState } from 'react';

function PlatformSelector({ platforms, onPlatformSelect, loading }) {
  const [selectedPlatform, setSelectedPlatform] = useState(null);
  const [credentials, setCredentials] = useState({});

  const handlePlatformClick = (platform) => {
    setSelectedPlatform(platform);
  };

  const handleConnect = () => {
    if (selectedPlatform) {
      onPlatformSelect(selectedPlatform, credentials);
    }
  };

  const handleCredentialChange = (field, value) => {
    setCredentials({
      ...credentials,
      [field]: value
    });
  };

  return (
    <div className="max-w-6xl mx-auto">
      <h2 className="text-2xl font-bold text-gray-900 mb-6">
        Connect Your Fitness Platform
      </h2>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {platforms.map((platform) => (
          <div
            key={platform.id}
            className={`bg-white rounded-lg shadow-md p-6 cursor-pointer transition-all ${
              selectedPlatform?.id === platform.id
                ? 'ring-4 ring-blue-500'
                : 'hover:shadow-lg'
            }`}
            onClick={() => handlePlatformClick(platform)}
          >
            <div className="flex items-center mb-4">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-lg flex items-center justify-center text-white font-bold text-xl">
                {platform.name.charAt(0)}
              </div>
              <div className="ml-4">
                <h3 className="text-xl font-bold text-gray-900">
                  {platform.name}
                </h3>
                <p className="text-sm text-gray-500">
                  {platform.supports_direct_integration ? 'Direct Integration' : 'Export Required'}
                </p>
              </div>
            </div>

            <p className="text-gray-600 text-sm mb-4">
              Connect your {platform.name} account to analyze your activity data
            </p>

            {platform.note && (
              <p className="text-xs text-orange-600">{platform.note}</p>
            )}
          </div>
        ))}
      </div>

      {selectedPlatform && (
        <div className="mt-8 bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-bold text-gray-900 mb-4">
            Connect to {selectedPlatform.name}
          </h3>

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Access Token (Optional)
              </label>
              <input
                type="text"
                placeholder="Enter access token"
                value={credentials.accessToken || ''}
                onChange={(e) => handleCredentialChange('accessToken', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Refresh Token (Optional)
              </label>
              <input
                type="text"
                placeholder="Enter refresh token"
                value={credentials.refreshToken || ''}
                onChange={(e) => handleCredentialChange('refreshToken', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500"
              />
            </div>

            <button
              onClick={handleConnect}
              disabled={loading}
              className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors disabled:bg-gray-400"
            >
              {loading ? 'Connecting...' : 'Connect & Analyze'}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

export default PlatformSelector;

