package ch.benlegiang.annotation.api.services;

import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import ch.benlegiang.annotation.api.enums.CodeLanguage;
import ch.benlegiang.annotation.api.repositories.AnnotationRepository;
import ch.benlegiang.annotation.api.utils.AnnotationUtil;
import lexer.HTok;
import lexer.LTok;
import lombok.AllArgsConstructor;
import org.springframework.boot.web.reactive.function.client.WebClientCustomizer;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;
import java.util.List;

@AllArgsConstructor
@Service
public class AnnotationService {

    private final AnnotationRepository annotationRepository;
    private final MongoTemplate mongoTemplate;

    public void addAnnotationEntityToDatabase(AnnotationEntity annotationEntity) {
        annotationRepository.save(annotationEntity);
    }

}
