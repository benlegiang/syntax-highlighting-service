package ch.benlegiang.annotation.api.services;

import ch.benlegiang.annotation.api.dtos.AnnotationPostDTO;
import ch.benlegiang.annotation.api.enums.CodeLanguage;
import ch.benlegiang.annotation.api.repositories.AnnotationRepository;
import ch.benlegiang.annotation.api.utils.AnnotationUtil;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
@RequiredArgsConstructor
@Service
public class AnnotationService {

    private final AnnotationRepository annotationRepository;

    public String lexSourceCode(CodeLanguage codeLanguage, String sourceCode) {
        String lToks = AnnotationUtil.lex(codeLanguage, sourceCode);

        return lToks;
    }

    public String highlightSourceCode(CodeLanguage codeLanguage, String sourceCode) {
        String hToks = AnnotationUtil.highlight(codeLanguage, sourceCode);

        return hToks;
    }
}
