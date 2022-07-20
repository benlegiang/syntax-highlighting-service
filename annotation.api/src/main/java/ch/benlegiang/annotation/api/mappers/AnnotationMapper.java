package ch.benlegiang.annotation.api.mappers;

import ch.benlegiang.annotation.api.dtos.AnnotationPostDTO;
import ch.benlegiang.annotation.api.entities.JavaAnnotationEntity;
import ch.benlegiang.annotation.api.entities.PythonAnnotationEntity;
import org.mapstruct.Mapper;
import org.mapstruct.Mapping;
import org.mapstruct.ReportingPolicy;
import org.mapstruct.factory.Mappers;

@Mapper(unmappedTargetPolicy = ReportingPolicy.IGNORE)
public interface AnnotationMapper {

    AnnotationMapper INSTANCE = Mappers.getMapper(AnnotationMapper.class);

    @Mapping(source = "sourceCode", target = "sourceCode")
    PythonAnnotationEntity convertAnnotationPostDTOToPythonEntity(AnnotationPostDTO annotationPostDTO);

    @Mapping(source = "sourceCode", target = "sourceCode")
    JavaAnnotationEntity convertAnnotationPostDTOToJavaEntity(AnnotationPostDTO annotationPostDTO);


    @Mapping(source = "sourceCode", target = "sourceCode")
    JavaAnnotationEntity convertAnnotationPostDTOToKotlinEntity(AnnotationPostDTO annotationPostDTO);
}
