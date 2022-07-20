export class RequestCheckUtil {
  public static check(requestBody: any): boolean {
    const supportedCodeLanguages = ["JAVA", "PYTHON3", "KOTLIN"];

    if (Object.keys(requestBody).length === 0) {
      return false;
    }

    if (!requestBody?.codeLanguage || !requestBody?.sourceCode) {
      return false;
    }

    if (requestBody?.codeLanguage && !supportedCodeLanguages.includes(requestBody.codeLanguage.toUpperCase())) {
      return false;
    }

    return true;
  }
}
