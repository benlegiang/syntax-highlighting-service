package ch.benlegiang.annotation.api.mappers;

import ch.benlegiang.annotation.api.dtos.AnnotationGetDTO;
import ch.benlegiang.annotation.api.dtos.AnnotationPostDTO;
import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface AnnotationMapper {

    AnnotationMapper INSTANCE = Mappers.getMapper(AnnotationMapper.class);

    @Mapping(source = "codeLanguage", target = "codeLanguage")
    @Mapping(source = "sourceCode", target = "sourceCode")
    AnnotationEntity convertAnnotationPostDTOToAnnotationEntity(AnnotationPostDTO annotationPostDTO);

    @Mapping(target = "id")
    @Mapping(target = "codeLanguage")
    @Mapping(target = "sourceCode")
    @Mapping(target = "tokens")
    @Mapping(target = "prediction")
    AnnotationGetDTO convertAnnotationEntityToGetDTO(AnnotationEntity annotationEntity);

}
