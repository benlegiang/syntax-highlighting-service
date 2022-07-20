package ch.benlegiang.annotation.api.services;

import ch.benlegiang.annotation.api.enums.CodeLanguage;
import ch.benlegiang.annotation.api.repositories.AnnotationRepository;
import ch.benlegiang.annotation.api.utils.AnnotationUtil;
import lexer.HTok;
import lexer.LTok;
import lombok.AllArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
@AllArgsConstructor
@Service
public class AnnotationService {

    private final AnnotationRepository annotationRepository;

    public LTok[] lexSourceCode(CodeLanguage codeLanguage, String sourceCode) {
        LTok[] lToks = AnnotationUtil.lex(codeLanguage, sourceCode);

        return lToks;
    }

    public HTok[] highlightSourceCode(CodeLanguage codeLanguage, String sourceCode) {
        HTok[] hToks = AnnotationUtil.highlight(codeLanguage, sourceCode);

        return hToks;
    }
}
