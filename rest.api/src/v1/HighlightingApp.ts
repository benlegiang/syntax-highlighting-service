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

      const result = await highlightingService.highlight(requestBody.codeLanguage, requestBody.sourceCode);

      highlightingService.parse(result);

      span.finish();
      return result;
    }

    span.finish();

    return {
      error: "Invalid input",
    };
  }
}
