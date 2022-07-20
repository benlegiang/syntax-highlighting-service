package ch.benlegiang.annotation.api.entities;

import org.springframework.data.mongodb.core.mapping.Document;


@Document(collection = "javaAnnotations")
public class JavaAnnotationEntity extends AnnotationEntity {
}
