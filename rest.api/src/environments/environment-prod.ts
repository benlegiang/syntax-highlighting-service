import "dotenv/config";
export const environment = {
  port: process.env.REST_API_PORT || 8081,
  annotationApi: {
    host: process.env.ANNOTATION_API_HOST,
    port: process.env.ANNOTATION_API_PORT || 8080,
  },
};
