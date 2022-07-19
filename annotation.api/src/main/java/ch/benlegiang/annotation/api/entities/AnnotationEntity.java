package ch.benlegiang.annotation.api.entities;

import ch.benlegiang.annotation.api.enums.CodeLanguage;
import lexer.LTok;
import lombok.Data;
import org.springframework.data.annotation.Id;

import java.util.List;


@Data
// @Document
public class AnnotationEntity {
    @Id
    private String id;
    private CodeLanguage codeLanguage;
    private String sourceCode;
    private List<LTok> lexTokens;

}
