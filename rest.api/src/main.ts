import App from "./App";
import "dotenv/config";

const PORT = process.env.REST_API_PORT;

App.listen(PORT, () => {
  console.log(`Server is listening on ${PORT}`);
});
