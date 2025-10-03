/**
 * API Configuration and Utility Functions
 * NASA Space Apps 2024 - AstroShield
 */

// API Configuration
export const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
  ENDPOINTS: {
    // Impact Analysis
    IMPACT_ANALYZE: '/api/impact/analyze',
    IMPACT_CUSTOM: '/api/impact/custom',
    IMPACT_PARAMETER_STUDY: '/api/impact/parameter-study',
    
    // Scenarios
    SCENARIOS: '/api/scenarios',
    SCENARIOS_COMPARE: '/api/scenarios/compare',
    SCENARIOS_SEARCH: '/api/scenarios/search',
    
    // Tsunami Assessment
    TSUNAMI_ASSESS: '/api/tsunami/assess',
    TSUNAMI_QUICK_CHECK: '/api/tsunami/quick-check',
    TSUNAMI_RISK_LEVELS: '/api/tsunami/risk-levels',
    
    // Visualizations
    VIZ_SHAKE_MAP: '/api/visualization/shake-map',
    VIZ_IMPACT_CHART: '/api/visualization/impact-chart',
    
    // Health & Info
    HEALTH: '/api/health',
    INFO: '/api/info'
  }
};

/**
 * Generic API call function with error handling
 * @param {string} endpoint - API endpoint path
 * @param {Object} options - Fetch options (method, headers, body, etc.)
 * @returns {Promise<Object>} - API response data
 */
export const apiCall = async (endpoint, options = {}) => {
  const url = `${API_CONFIG.BASE_URL}${endpoint}`;
  
  const defaultOptions = {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json',
    },
  };
  
  const requestOptions = { ...defaultOptions, ...options };
  
  try {
    console.log(`API Call: ${requestOptions.method} ${url}`);
    
    const response = await fetch(url, requestOptions);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    
    if (!data.success) {
      throw new Error(data.error || 'API request failed');
    }
    
    return data;
  } catch (error) {
    console.error(`API Error for ${endpoint}:`, error);
    throw error;
  }
};

/**
 * Analyze asteroid impact
 * @param {Object} impactParams - Impact parameters
 * @returns {Promise<Object>} - Impact analysis data
 */
export const analyzeImpact = async (impactParams) => {
  return await apiCall(API_CONFIG.ENDPOINTS.IMPACT_ANALYZE, {
    method: 'POST',
    body: JSON.stringify(impactParams)
  });
};

/**
 * Assess tsunami risk
 * @param {Object} tsunamiParams - Tsunami assessment parameters
 * @returns {Promise<Object>} - Tsunami risk data
 */
export const assessTsunamiRisk = async (tsunamiParams) => {
  return await apiCall(API_CONFIG.ENDPOINTS.TSUNAMI_ASSESS, {
    method: 'POST',
    body: JSON.stringify(tsunamiParams)
  });
};

/**
 * Get all available scenarios
 * @returns {Promise<Object>} - Scenarios data
 */
export const getScenarios = async () => {
  return await apiCall(API_CONFIG.ENDPOINTS.SCENARIOS);
};

/**
 * Run a specific scenario
 * @param {string} scenarioName - Name of the scenario
 * @param {Object} options - Optional parameters
 * @returns {Promise<Object>} - Scenario run results
 */
export const runScenario = async (scenarioName, options = {}) => {
  return await apiCall(`${API_CONFIG.ENDPOINTS.SCENARIOS}/${scenarioName}/run`, {
    method: 'POST',
    body: JSON.stringify(options)
  });
};

/**
 * Generate shake map data
 * @param {Object} shakeMapParams - Shake map parameters
 * @returns {Promise<Object>} - Shake map data
 */
export const generateShakeMap = async (shakeMapParams) => {
  return await apiCall(API_CONFIG.ENDPOINTS.VIZ_SHAKE_MAP, {
    method: 'POST',
    body: JSON.stringify(shakeMapParams)
  });
};

/**
 * Check API health
 * @returns {Promise<Object>} - Health status
 */
export const checkHealth = async () => {
  return await apiCall(API_CONFIG.ENDPOINTS.HEALTH);
};

/**
 * Get API information
 * @returns {Promise<Object>} - API info and capabilities
 */
export const getApiInfo = async () => {
  return await apiCall(API_CONFIG.ENDPOINTS.INFO);
};