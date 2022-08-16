package ch.benlegiang.annotation.api.dtos;

import lombok.Data;

@Data
public class ParserPostDTO {
    private String id;
    private String codeLanguage;
    private String sourceCode;
}
