package ch.benlegiang.annotation.api.entities;

import lexer.LTok;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@Document(collection = "annotations")
public class AnnotationEntity {
    @Id
    private String id;
    private String sourceCode;
    private LTok[] lexTokens;
    private String[] hCodes;
}
