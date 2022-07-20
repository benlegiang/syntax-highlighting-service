import axios from "axios";
import { environment } from "../../environments/environment-prod";

const url = `http://${environment.annotationApi.host}:${environment.annotationApi.port}/api/v1/annotate`;

interface HighlightingResult {
  codeLanguage: String;
  sourceCode: String;
  hCodes: number[];
}

export class HighlightingService {
  public async highlight(codeLanguage: String, sourceCode: String): Promise<HighlightingResult> {
    const requestBody = JSON.stringify({
      codeLanguage: codeLanguage.toUpperCase(),
      sourceCode: sourceCode,
    });

    try {
      const response: any = await axios.post(url, requestBody, {
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

// POST REQUEST VIA COMMAND LINE
// curl -d '{"codeLanguage":"java", "sourceCode":" public String annotate(@RequestBody AnnotationPostDTO annotationPostDto) {}"}' -H "Content-Type: application/json" -X POST http://localhost:8081/api/v1/highlight
