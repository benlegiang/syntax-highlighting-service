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
  // Only send user input for ANTLR parsing using the Formal Model
  // Does not need to be awaited because response is irrelevant
  public parse(input: HighlightingResult): void {
    const requestBody = JSON.stringify({
      id: input?.id,
      codeLanguage: input?.codeLanguage?.toUpperCase(),
      sourceCode: input?.sourceCode,
    });

    try {
      axios.post(environment.annotationApi.parserUrl, requestBody, {
        headers: {
          "Content-Type": "application/json",
        },
      });
    } catch (err) {
      console.log(err);
    }
  }

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
      console.log(err.code);
      return Promise.resolve(null);
    }
  }
}
