package ch.benlegiang.annotation.api.services;

import ch.benlegiang.annotation.api.dtos.ParserPostDTO;
import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import ch.benlegiang.annotation.api.repositories.AnnotationRepository;
import ch.benlegiang.annotation.api.utils.AnnotationUtil;
import com.mongodb.MongoCursorNotFoundException;
import lombok.AllArgsConstructor;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.scheduling.annotation.Async;
import org.springframework.stereotype.Service;

import java.nio.charset.StandardCharsets;
import java.util.List;

@AllArgsConstructor
@Service
public class AnnotationService {

    private final AnnotationRepository annotationRepository;
    private final MongoTemplate mongoTemplate;


    @Async
    public void setHCodeValues(AnnotationEntity annotationEntity) {
        List<Integer> formal = AnnotationUtil.getHCodeValuesFromHToks(AnnotationUtil.parse(annotationEntity.getCodeLanguage(), annotationEntity.getSourceCode()));
        formal.remove(formal.size() - 1);
        annotationEntity.setFormal(formal);

        if (annotationEntity.getTokenIds() != null && formal != null) {
            Boolean isTrainable = annotationEntity.getTokenIds().size() == formal.size();
            annotationEntity.setIsTrainable(isTrainable);
        }

        System.out.println(annotationEntity);
        annotationRepository.save(annotationEntity);
    }

    @Async
    public void setFormalHCodeValuesByIdOnDatabaseObject(ParserPostDTO parserPostDTO) {
        try {

            Query query = new Query(Criteria.where("id").is(parserPostDTO.getId()));
            AnnotationEntity annotationEntity = mongoTemplate.findOne(query, AnnotationEntity.class);

            /*
            byte[] bytes = parserPostDTO.getSourceCode().getBytes(StandardCharsets.UTF_8);

            String utf8EncodedString = new String(bytes, StandardCharsets.UTF_8);

            parserPostDTO.setSourceCode(utf8EncodedString);
            */
            List<Integer> formal = AnnotationUtil.parse(parserPostDTO);

            annotationEntity.setFormal(AnnotationUtil.parse(parserPostDTO));

            if (annotationEntity.getTokenIds() != null && formal != null) {
                Boolean isTrainable = annotationEntity.getTokenIds().size() == formal.size();
                annotationEntity.setIsTrainable(isTrainable);
            }

            annotationRepository.save(annotationEntity);
        } catch (MongoCursorNotFoundException e) {
            e.printStackTrace();
        }
    }
}
