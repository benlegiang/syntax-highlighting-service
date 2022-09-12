import express from "express";
import { HighlightingApp } from "../HighlightingApp";
import * as Sentry from "@sentry/node";

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
        "Access-Control-Allow-Headers, Origin, Content-Type, Authorization, Content-Length, X-Requested-With, Accept, Sentry-Trace"
      );
      if (req.method === "OPTIONS") {
        res.sendStatus(200);
      } else {
        next();
      }
    });

    // Entry endpoint for micro services
    this.router.post("/highlight", (req, res) => {
      const scope = Sentry.getCurrentHub().getScope();
      scope.setTransactionName("rest.api-highlight");
      scope.setTag("source", "rest.api");

      new HighlightingApp()
        .process(req)
        .then((result) => {
          scope.getTransaction().finish();
          res.json(result);
        })
        .catch((e) => {
          Sentry.captureException(e);
          res.json(null);
        });
    });

    // Add additional routes in this function if needed
  }
}
