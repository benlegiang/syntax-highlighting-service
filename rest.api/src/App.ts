import express from "express";
import { Rest } from "./routes/v1/rest";

class App {
  public express: express.Express;

  constructor() {
    this.express = express();
    this.express.use(express.json());
    this.mountRoutes();
  }

  private mountRoutes(): void {
    const router = express.Router();

    router.get("/", (req, res) => {
      res.json({ message: "syntax highlighting api" });
    });
    this.express.use("/", router);
    this.express.use("/api/v1", new Rest().getRouter());
  }
}

export default new App().express;
