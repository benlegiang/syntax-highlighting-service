package ch.benlegiang.annotation.api.repositories;

import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import ch.benlegiang.annotation.api.enums.CodeLanguage;
import org.springframework.data.mongodb.repository.MongoRepository;

import java.util.List;

public interface AnnotationRepository extends MongoRepository<AnnotationEntity, String> {

    List<AnnotationEntity> getAnnotationsByCodeLanguage(CodeLanguage codeLanguage);
}

