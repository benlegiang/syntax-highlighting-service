package ch.benlegiang.annotation.api.dtos;

import ch.benlegiang.annotation.api.enums.CodeLanguage;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
public class AnnotationPostDTO {

    private CodeLanguage codeLanguage;
    private String sourceCode;

}
