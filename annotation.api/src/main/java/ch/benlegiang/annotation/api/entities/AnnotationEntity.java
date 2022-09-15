package ch.benlegiang.annotation.api.entities;

import ch.benlegiang.annotation.api.enums.CodeLanguage;
import lexer.LTok;
import lombok.Data;
import org.springframework.data.annotation.Id;
import org.springframework.data.annotation.Transient;
import org.springframework.data.mongodb.core.mapping.Document;
import java.util.List;

@Data
@Document(collection = "annotations")
public class AnnotationEntity {
    @Id
    public String id;
    public CodeLanguage codeLanguage;
    public String sourceCode;
    @Transient
    public LTok[] tokens;
    @Transient
    public List<Integer> lexed;
    public List<Integer> hCodeTokenIds;
    public List<Integer> hCodeValues;
    @Transient
    public List<Integer> prediction;
    public Boolean isTrainable;
    public Boolean isTestItem = false;
}
