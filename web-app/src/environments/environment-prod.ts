export const environment = {
  port: process.env.WEB_APP_PORT || 3000,
  restApi: {
    host: process.env.REACT_APP_REST_API_PORT,
    port: process.env.REACT_APP_REST_API_PORT || 8081,
    highlightUrl: `http://${process.env.REACT_APP_REST_API_HOST}:${process.env.REACT_APP_REST_API_PORT}/api/v1/highlight`,
  },
};
