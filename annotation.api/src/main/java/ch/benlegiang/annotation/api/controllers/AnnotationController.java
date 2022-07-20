package ch.benlegiang.annotation.api.controllers;

import ch.benlegiang.annotation.api.dtos.AnnotationPostDTO;
import ch.benlegiang.annotation.api.enums.CodeLanguage;
import ch.benlegiang.annotation.api.services.AnnotationService;
import lexer.LTok;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("api/v1")
public class AnnotationController {

    private final AnnotationService annotationService;

    public AnnotationController(AnnotationService annotationService) {
        this.annotationService = annotationService;
    }

    @PostMapping(path = "/annotate")
    @ResponseStatus(HttpStatus.OK)
    @ResponseBody
    public String annotate(@RequestBody AnnotationPostDTO annotationPostDto) {


        CodeLanguage codeLanguage = CodeLanguage.valueOf(annotationPostDto.getCodeLanguage());

        System.out.println(codeLanguage);

        /*PythonAnnotationEntity pythonAnnotationEntity = AnnotationMapper.INSTANCE.convertAnnotationPostDTOToEntity(annotationPostDto);

        LTok[] lToks = annotationService.lexSourceCode(CodeLanguage.JAVA, pythonAnnotationEntity.getSourceCode());
        pythonAnnotationEntity.setLexTokens(lToks);

        System.out.println(pythonAnnotationEntity);*/

        return "";

    }
}
