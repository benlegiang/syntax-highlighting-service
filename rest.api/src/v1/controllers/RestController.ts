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
    // Entry endpoint for micro services
    this.router.post("/highlight", (req, res) => {
      new HighlightingApp().start(req).then((result) => {
        res.json(result);
      });
    });

    // Add additional endpoints here if needed
  }
}
