import { environment } from "./../../environments/environment-prod";
import axios from "axios";

export interface HighlightingResult {
  id: String;
  codeLanguage: String;
  sourceCode: String;
  tokens: any[];
  prediction: number[];
}

export class HighlightingService {
  // Returns prediction in the form of HCode values
  public async highlight(codeLanguage: String, sourceCode: String): Promise<HighlightingResult> {
    const requestBody = JSON.stringify({
      codeLanguage: codeLanguage.toUpperCase(),
      sourceCode: sourceCode,
      // sourceCode: Buffer.from(sourceCode, "utf-8").toString(),
    });

    try {
      const response: any = await axios.post(environment.annotationApi.highlightUrl, requestBody, {
        headers: {
          "Content-Type": "application/json",
        },
      });

      const responseBody: HighlightingResult = response?.data;

      return Promise.resolve(responseBody);
    } catch (err) {
      return Promise.resolve(null);
    }
  }
}
