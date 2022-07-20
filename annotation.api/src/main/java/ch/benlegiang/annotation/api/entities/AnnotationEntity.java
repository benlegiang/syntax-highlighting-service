package ch.benlegiang.annotation.api.entities;

import ch.benlegiang.annotation.api.enums.CodeLanguage;
import lexer.HTok;
import lexer.LTok;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

import java.util.List;

@Data
@Document("annotations")
public class AnnotationEntity {
    @Id
    private String id;
    private CodeLanguage codeLanguage;
    private String sourceCode;
    private List<Integer> tokenIds;
    private List<Integer> hCodeValues;
}
