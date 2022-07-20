package ch.benlegiang.annotation.api.entities;

import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "kotlinAnnotations")
public class KotlinAnnotationEntity extends AnnotationEntity {

}
