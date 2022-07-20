import { HighlightingService } from "./services/HighlightingService";
import { RequestCheckUtil } from "./utils/requestCheckUtil";

export class HighlightingApp {
  public async start(req: any): Promise<any> {
    const requestBody = req?.body || null;

    if (RequestCheckUtil.check(requestBody)) {
      const highlightingService = new HighlightingService();
      const result = await highlightingService.highlight(requestBody.codeLanguage, requestBody.sourceCode);

      return result;
    }

    return {
      error: "Invalid input",
    };
  }
}
