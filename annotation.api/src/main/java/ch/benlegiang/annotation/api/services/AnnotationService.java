package ch.benlegiang.annotation.api.services;

import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import ch.benlegiang.annotation.api.enums.CodeLanguage;
import ch.benlegiang.annotation.api.repositories.AnnotationRepository;
import ch.benlegiang.annotation.api.utils.AnnotationUtil;
import lexer.HTok;
import lexer.LTok;
import lombok.AllArgsConstructor;
import org.bson.types.Code;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@AllArgsConstructor
@Service
public class AnnotationService {

    private final AnnotationRepository annotationRepository;


    public List<Integer> lexSourceCode(CodeLanguage codeLanguage, String sourceCode) {
        LTok[] lToks = AnnotationUtil.lex(codeLanguage, sourceCode);

        List<Integer> tokenIds = new ArrayList<>();
        for (LTok lTok : lToks) {
            tokenIds.add(lTok.tokenId);
        }

        return tokenIds;
    }

    public List<Integer> highlightSourceCode(CodeLanguage codeLanguage, String sourceCode) {
        HTok[] hToks = AnnotationUtil.highlight(codeLanguage, sourceCode);
        List<Integer> hCodeValues = new ArrayList<>();
        for (HTok hTok : hToks) {
            hCodeValues.add(hTok.hCodeValue);
        }
        return hCodeValues;
    }

    public void addAnnotationEntityToDatabase(AnnotationEntity annotationEntity) {
        annotationRepository.save(annotationEntity);
    }
}
