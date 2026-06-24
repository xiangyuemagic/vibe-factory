// Vercel Serverless Function
// Wraps existing Netlify handler (CommonJS compatible)

const { handler } = require('../netlify/functions/api');

module.exports = async (req, res) => {
  // Convert Vercel request to Netlify event format
  const event = {
    path: req.url || '/',
    httpMethod: req.method || 'GET',
    headers: Object.fromEntries(
      Object.entries(req.headers || {}).map(([k, v]) => [k, String(v)])
    ),
    queryStringParameters: req.query || {},
    body: req.body ? JSON.stringify(req.body) : null
  };

  try {
    const result = await handler(event);

    if (result.headers) {
      for (const [key, value] of Object.entries(result.headers)) {
        res.setHeader(key, String(value));
      }
    }

    const body = typeof result.body === 'string' ? result.body : JSON.stringify(result.body);
    return res.status(result.statusCode || 200).send(body);
  } catch (e) {
    return res.status(500).json({ error: e.message });
  }
};
