import express from "express";
import { RestController } from "./v1/controllers/RestController";
import * as Sentry from "@sentry/node";
import { RewriteFrames } from "@sentry/integrations";
const Tracing = require("@sentry/tracing");

class App {
  public express: express.Express;
  public compression = require("compression");

  constructor() {
    this.express = express();
    // Parses all bodies to json
    this.express.use(express.json({ limit: "50mb" }));
    // Uses compression for all HTTP responses
    this.express.use(this.compression());
    // To avoid "Request Entity too large" error

    Sentry.init({
      environment: "TEST1",
      dsn: "https://b2a73205682f49299647b69434915dbe@o1173927.ingest.sentry.io/6652790",
      integrations: [
        // enable HTTP calls tracing
        new Sentry.Integrations.Http({ tracing: true }),
        // enable Express.js middleware tracing
        new Tracing.Integrations.Express({ express }),
        new RewriteFrames({
          root: process.cwd(),
        }) as any,
      ],
      tracesSampleRate: 1.0,
    });

    this.express.use(Sentry.Handlers.requestHandler());
    this.express.use(Sentry.Handlers.tracingHandler());

    this.mountRoutes();

    this.express.use(Sentry.Handlers.errorHandler());
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
