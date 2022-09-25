import express from "express";
import { HighlightingApp } from "../HighlightingApp";

export class RestController {
  private router: any;
  constructor() {
    this.router = express.Router();
    this.mountRoutes();
  }

  public getRouter(): any {
    return this.router;
  }

  private mountRoutes(): void {
    this.router.use("/", (req, res, next) => {
      res.header("Access-Control-Allow-Origin", "*");
      res.header("Access-Control-Allow-Methods", "GET, POST, DELETE, PUT");

      res.header(
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Headers, Origin, Content-Type, Authorization, Content-Length, X-Requested-With, Accept"
      );
      if (req.method === "OPTIONS") {
        res.sendStatus(200);
      } else {
        next();
      }
    });

    // Entry endpoint for micro services
    this.router.post("/highlight", (req, res) => {
      new HighlightingApp()
        .process(req)
        .then((result) => {
          res.json(result);
        })
        .catch((e) => {
          res.json(null);
        });
    });

    // Add additional routes in this function if needed
  }
}
