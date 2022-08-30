import { HCode } from "../enums/HCode";
import { HighlightingResult } from "../services/HighlightingService";

export class OutputBindingUtil {
  public static getBindings(input: HighlightingResult) {
    const src = input?.sourceCode;
    const prediction = input?.prediction;

    const bindings = input?.tokens?.map((token, index) => {
      const stringToken = src.substring(token?.startIndex, token?.endIndex + 1);

      return { class: HCode[prediction[index]], token: stringToken };
    });

    return bindings;
  }
}
