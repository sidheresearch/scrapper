import axios from 'axios';

// API base URL - will use environment variable in production
const API_BASE_URL = process.env.REACT_APP_API_URL 
  ? `${process.env.REACT_APP_API_URL}/api`
  : 'http://localhost:5000/api';

// Configure axios defaults
axios.defaults.timeout = 30000;

class ScraperAPI {
  /**
   * Check API health
   */
  async healthCheck() {
    try {
      const response = await axios.get(`${API_BASE_URL}/health`);
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }

  /**
   * Scrape a website
   * @param {string} url - The URL to scrape
   * @param {number} depth - Scraping depth (0, 1, or 2)
   * @param {boolean} llmEnabled - Whether to use LLM formatting
   * @param {string} filename - Custom filename (optional)
   */
  async scrapeWebsite(url, depth = 0, llmEnabled = true, filename = '') {
    try {
      const response = await axios.post(`${API_BASE_URL}/scrape`, {
        url,
        depth,
        llm_enabled: llmEnabled,
        filename
      });
      return response.data;
    } catch (error) {
      console.error('Scraping failed:', error);
      throw error.response?.data || error;
    }
  }

  /**
   * Get details of a scraping result
   * @param {string} resultId - The result ID
   */
  async getResultDetails(resultId) {
    try {
      const response = await axios.get(`${API_BASE_URL}/results/${resultId}`);
      return response.data;
    } catch (error) {
      console.error('Failed to get result details:', error);
      throw error;
    }
  }

  /**
   * Download a scraping result
   * @param {string} resultId - The result ID
   */
  getDownloadUrl(resultId) {
    return `${API_BASE_URL}/download/${resultId}`;
  }

  /**
   * List all scraping results
   */
  async listResults() {
    try {
      const response = await axios.get(`${API_BASE_URL}/results`);
      return response.data;
    } catch (error) {
      console.error('Failed to list results:', error);
      throw error;
    }
  }
}

const scraperAPIInstance = new ScraperAPI();
export default scraperAPIInstance;
