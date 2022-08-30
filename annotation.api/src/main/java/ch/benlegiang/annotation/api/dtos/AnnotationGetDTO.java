package ch.benlegiang.annotation.api.dtos;

import lexer.LTok;
import lombok.Data;

import java.util.List;

@Data
public class AnnotationGetDTO {
    private String id;
    private String codeLanguage;
    private String sourceCode;
    private LTok[] tokens;
    private List<Integer> prediction;
}
