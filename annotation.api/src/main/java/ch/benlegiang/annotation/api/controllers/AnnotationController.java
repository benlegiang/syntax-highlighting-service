package ch.benlegiang.annotation.api.controllers;

import ch.benlegiang.annotation.api.dtos.AnnotationGetDTO;
import ch.benlegiang.annotation.api.dtos.AnnotationPostDTO;
import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import ch.benlegiang.annotation.api.enums.CodeLanguage;
import ch.benlegiang.annotation.api.mappers.AnnotationMapper;
import ch.benlegiang.annotation.api.services.AnnotationService;
import ch.benlegiang.annotation.api.services.PredictionService;
import ch.benlegiang.annotation.api.utils.AnnotationUtil;
import com.fasterxml.jackson.core.JsonProcessingException;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;
import resolver.Python3Resolver;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@RestController
@RequestMapping("api/v1")
public class AnnotationController {

    private final AnnotationService annotationService;
    private final PredictionService predictionService;

    public AnnotationController(AnnotationService annotationService, PredictionService predictionService) {
        this.annotationService = annotationService;
        this.predictionService = predictionService;
    }

    // For now, this endpoint returns the hCodeValues from the AST
    // hCodeValues from AST is stored on DB for fine-tuning
    // TODO: Needs to return the hCodeValues from the SHModel
    @PostMapping(path = "/annotate")
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    public AnnotationGetDTO annotate(@RequestBody AnnotationPostDTO annotationPostDto) throws IOException {
        AnnotationEntity annotationEntity = AnnotationMapper.INSTANCE.convertAnnotationPostDTOToAnnotationEntitiy(annotationPostDto);

        List<Integer> tokenIds = AnnotationUtil.lexSourceCode(annotationEntity);
        List<Integer> hCodeValues = AnnotationUtil.highlightSourceCode(annotationEntity);

        Integer diff = tokenIds.size() - hCodeValues.size();
        System.out.println(diff);

        annotationEntity.setTokenIds(tokenIds);
        annotationEntity.setFormal(hCodeValues);

        // Send tokenIds for prediction and set it on Entity object
        predictionService.setPrediction(annotationEntity);

        // Save Entity to Mongo DB
        annotationService.addAnnotationEntityToDatabase(annotationEntity);


        AnnotationGetDTO annotationGetDTO = AnnotationMapper.INSTANCE.convertAnnotationEntityToGetDTO(annotationEntity);
        return annotationGetDTO;
    }

}
