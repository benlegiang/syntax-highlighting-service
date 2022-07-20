package ch.benlegiang.annotation.api.dtos;

import lombok.Data;

import java.util.List;

@Data
public class AnnotationGetDTO {
    private String codeLanguage;
    private String sourceCode;
    private List<Integer> hCodeValues;
}
