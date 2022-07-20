package ch.benlegiang.annotation.api.entities;

import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "pythonAnnotations")
public class PythonAnnotationEntity extends AnnotationEntity {

}
