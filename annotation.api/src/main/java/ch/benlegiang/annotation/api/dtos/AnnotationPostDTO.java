package ch.benlegiang.annotation.api.dtos;

import ch.benlegiang.annotation.api.enums.CodeLanguage;
import lombok.Data;

@Data
public class AnnotationPostDTO {

    private String codeLanguage;
    private String sourceCode;

}
