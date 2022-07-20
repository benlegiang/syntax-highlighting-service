package ch.benlegiang.annotation.api.entities;

import org.springframework.data.annotation.TypeAlias;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "kotlinAnnotations")
@TypeAlias("KOTLIN")
public class KotlinAnnotationEntity extends AnnotationEntity {

}
