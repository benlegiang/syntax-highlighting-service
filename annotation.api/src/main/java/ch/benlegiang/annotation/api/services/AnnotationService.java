package ch.benlegiang.annotation.api.services;

import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import ch.benlegiang.annotation.api.repositories.AnnotationRepository;
import ch.benlegiang.annotation.api.utils.AnnotationUtil;
import lexer.HTok;
import lexer.LTok;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

@AllArgsConstructor
@Service
public class AnnotationService {

    private final AnnotationRepository annotationRepository;

    public List<Integer> lexSourceCode(AnnotationEntity annotationEntity) {
        LTok[] lToks = AnnotationUtil.lex(annotationEntity.getCodeLanguage(), annotationEntity.getSourceCode());

        List<Integer> tokenIds = new ArrayList<>();
        for (LTok lTok : lToks) {
            tokenIds.add(lTok.tokenId);
        }

        return tokenIds;
    }

    public List<Integer> highlightSourceCode(AnnotationEntity annotationEntity) {
        HTok[] hToks = AnnotationUtil.highlight(annotationEntity.getCodeLanguage(), annotationEntity.getSourceCode());
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
