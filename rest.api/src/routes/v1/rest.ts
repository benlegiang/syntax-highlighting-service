import express from "express";

export class Rest {
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
      res.json({ message: "Successful!" });
    });
  }
}
