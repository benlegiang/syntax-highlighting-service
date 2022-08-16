import { HighlightingService } from "./services/HighlightingService";
import { RequestCheckUtil } from "./utils/requestCheckUtil";
import * as Sentry from "@sentry/node";

export class HighlightingApp {
  public async execute(req: any): Promise<any> {
    const scope = Sentry.getCurrentHub().getScope();
    const span = scope.getTransaction().startChild({
      op: "execute",
      description: this.constructor.name,
    });

    const requestBody = req?.body || null;

    const t = performance.now();

    if (RequestCheckUtil.check(requestBody)) {
      const highlightingService = new HighlightingService();

      const t2 = performance.now();
      const result = await highlightingService.highlight(requestBody.codeLanguage, requestBody.sourceCode);
      const d2 = performance.now() - t2;
      console.log("🚀 ~ file: HighlightingApp.ts ~ line 19 ~ HighlightingApp ~ start ~ prediction", d2);

      const t1 = performance.now();
      highlightingService.parse(result);
      const d1 = performance.now() - t1;
      console.log("🚀 ~ file: HighlightingApp.ts ~ line 14 ~ HighlightingApp ~ start ~ parser", d1);

      const duration = performance.now() - t;
      console.log("🚀 ~ file: HighlightingApp.ts ~ line 25 ~ HighlightingApp ~ start ~ total", duration);

      console.log("-----------");

      span.finish();
      return result;
    }

    span.finish();

    return {
      error: "Invalid input",
    };
  }
}
