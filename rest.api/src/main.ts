import App from "./App";
import "dotenv/config";

const PORT = process.env.PORT || 8080;

App.listen(PORT, () => {
  console.log(`Server is listening on ${PORT}`);
});
