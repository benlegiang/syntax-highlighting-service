import axios from "axios";
import { environment } from "../../environments/environment-prod";

const url = `http://${environment.annotationApi.host}:${environment.annotationApi.port}/api/v1/annotate`;

enum CodeLanguage {
  PYTHON3,
  JAVA,
  KOTLIN,
}

export class HighlightingService {
  public async highlight(codeLanguage: CodeLanguage, sourceCode: String): Promise<any> {
    let result = null;
    const payload = {
      codeLanguage: codeLanguage,
      sourceCode: sourceCode,
    };
    await axios
      .post(url, {
        payload,
      })
      .then((res) => {
        result = res.data;
      });

    return Promise.resolve({
      codeLanguage: "",
      sourceCode: "",
      lToks: "",
      hToks: "",
    });
  }
}
