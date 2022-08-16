package ch.benlegiang.annotation.api.services;

import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import ch.benlegiang.annotation.api.repositories.AnnotationRepository;
import lombok.AllArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@AllArgsConstructor
@Service
public class AnnotationService {

    private final AnnotationRepository annotationRepository;

    public void saveAnnotationEntityToDatabase(AnnotationEntity annotationEntity) {
        annotationRepository.save(annotationEntity);
    }

    public void setFormalTokenIdsOnDatabaseObject() {


    }

    public void setHCodeValues() {

    }

}
