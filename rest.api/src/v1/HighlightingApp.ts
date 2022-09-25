import { OutputBindingUtil } from "./utils/outputBindingUtil";
import { HighlightingService } from "./services/HighlightingService";
import { RequestCheckUtil } from "./utils/requestCheckUtil";

export class HighlightingApp {
  public async process(req: any): Promise<any> {
    const requestBody = req?.body || null;

    if (RequestCheckUtil.check(requestBody)) {
      const highlightingService = new HighlightingService();

      const prediction = await highlightingService.highlight(requestBody.codeLanguage, requestBody.sourceCode);
      const result = OutputBindingUtil.getBindings(prediction);

      return result;
    }

    return {
      error: "Invalid input",
    };
  }
}
