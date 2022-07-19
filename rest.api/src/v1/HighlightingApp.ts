import { HighlightingService } from "./services/HighlightingService";

export class HighlightingApp {
  public async start(req: any): Promise<any> {
    const requestBody = req?.body || null;

    if (Object.keys(requestBody).length === 0) {
      return Promise.resolve({ message: "Provide code language and soure code!" });
    }

    const highlightingService = new HighlightingService();
    const result = await highlightingService.highlight(requestBody.codeLanguage, requestBody.sourceCode);

    return result;
  }
}
