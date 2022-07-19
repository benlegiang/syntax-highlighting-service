import express from "express";
import { RestController } from "./v1/controllers/RestController";

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
    this.express.use("/api/v1", new RestController().getRouter());
  }
}

export default new App().express;
