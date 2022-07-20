package ch.benlegiang.annotation.api.entities;

import org.springframework.data.annotation.TypeAlias;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "pythonAnnotations")
@TypeAlias("PYTHON3")
public class PythonAnnotationEntity extends AnnotationEntity {

}
