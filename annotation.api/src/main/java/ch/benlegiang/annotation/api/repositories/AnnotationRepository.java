package ch.benlegiang.annotation.api.repositories;

import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import org.springframework.data.mongodb.repository.MongoRepository;

public interface AnnotationRepository extends MongoRepository<AnnotationEntity, String> {}

