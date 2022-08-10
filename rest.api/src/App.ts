import express from "express";
import { RestController } from "./v1/controllers/RestController";

class App {
  public express: express.Express;
  public compression = require("compression");

  constructor() {
    this.express = express();
    // Parses all bodies to json
    this.express.use(express.json());
    // Uses compression for all HTTP responses
    this.express.use(this.compression());
    this.mountRoutes();
  }

  private mountRoutes(): void {
    const router = express.Router();

    router.get("/", (req, res) => {
      res.json({ message: "syntax highlighting api" });
    });
    this.express.use("/", router);
    // Additional routes are added in the RestController
    this.express.use("/api/v1", new RestController().getRouter());
  }
}

export default new App().express;
