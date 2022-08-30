import { OutputBindingUtil } from "./utils/outputBindingUtil";
import { HighlightingService } from "./services/HighlightingService";
import { RequestCheckUtil } from "./utils/requestCheckUtil";
import * as Sentry from "@sentry/node";

export class HighlightingApp {
  public async process(req: any): Promise<any> {
    const scope = Sentry.getCurrentHub().getScope();
    const span = scope.getTransaction().startChild({
      op: "execute",
      description: this.constructor.name,
    });

    const requestBody = req?.body || null;

    if (RequestCheckUtil.check(requestBody)) {
      const highlightingService = new HighlightingService();

      const prediction = await highlightingService.highlight(requestBody.codeLanguage, requestBody.sourceCode);

      highlightingService.parse(prediction);
      const result = OutputBindingUtil.getBindings(prediction);

      span.finish();
      return result;
    }

    span.finish();

    return {
      error: "Invalid input",
    };
  }
}
