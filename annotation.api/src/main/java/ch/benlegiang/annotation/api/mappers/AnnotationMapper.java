package ch.benlegiang.annotation.api.mappers;

import ch.benlegiang.annotation.api.dtos.AnnotationPostDTO;
import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.factory.Mappers;

@Mapper()
public interface AnnotationMapper {

    AnnotationMapper INSTANCE = Mappers.getMapper(AnnotationMapper.class);

    @Mapping(source = "codeLanguage", target = "codeLanguage")
    @Mapping(source = "sourceCode", target = "sourceCode")
    AnnotationEntity convertAnnotationPostDTOToEntity(AnnotationPostDTO annotationPostDTO);

}
