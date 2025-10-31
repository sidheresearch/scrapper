const { createProxyMiddleware } = require('http-proxy-middleware');

module.exports = function(app) {
  app.use(
    '/api',
    createProxyMiddleware({
      target: 'http://localhost:5000',
      changeOrigin: true,
      secure: false,
      logLevel: 'debug',
      onError: (err, req, res) => {
        console.log('Proxy Error:', err);
      },
      onProxyReq: (proxyReq, req, res) => {
        console.log('Proxying:', req.method, req.path);
      }
    })
  );
};
