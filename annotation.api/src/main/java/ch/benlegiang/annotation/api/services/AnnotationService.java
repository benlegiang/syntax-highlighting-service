package ch.benlegiang.annotation.api.services;

import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import ch.benlegiang.annotation.api.repositories.AnnotationRepository;
import ch.benlegiang.annotation.api.utils.AnnotationUtil;
import lexer.HTok;
import lombok.AllArgsConstructor;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;
import java.util.List;


@AllArgsConstructor
@Service
public class AnnotationService {

    private final AnnotationRepository annotationRepository;

    @Async("cpuBoundThreadPoolTaskExecutor")
    public void highlightAsync(AnnotationEntity annotationEntity) {

        HTok[] hToks = AnnotationUtil.highlightSourceCode(annotationEntity);

        List<Integer> hCodeTokenIds = AnnotationUtil.getHCodeTokenIdsFromHToks(hToks);
        List<Integer> hCodeValues = AnnotationUtil.getHCodeValuesFromHToks(hToks);

        // Both TokenIds and hCodeValue of HTok object is required for fine-tuning
        annotationEntity.setHCodeTokenIds(hCodeTokenIds);
        annotationEntity.setHCodeValues(hCodeValues);

        if (hCodeTokenIds != null && hCodeValues != null) {
            annotationRepository.save(annotationEntity);
        }
    }
}
