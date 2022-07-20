package ch.benlegiang.annotation.api.utils;

import ch.benlegiang.annotation.api.dtos.AnnotationPostDTO;
import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import ch.benlegiang.annotation.api.entities.JavaAnnotationEntity;
import ch.benlegiang.annotation.api.entities.KotlinAnnotationEntity;
import ch.benlegiang.annotation.api.entities.PythonAnnotationEntity;
import ch.benlegiang.annotation.api.enums.CodeLanguage;
import ch.benlegiang.annotation.api.mappers.AnnotationMapper;
import lexer.HTok;
import lexer.LTok;
import resolver.JavaResolver;
import resolver.KotlinResolver;
import resolver.Python3Resolver;
import resolver.Resolver;

import java.util.Arrays;

public class AnnotationUtil {

    public static LTok[] lex(CodeLanguage codeLanguage, String sourceCode) {
        Resolver resolver = getResolverByLang(codeLanguage);
        LTok[] lToks = resolver.lex(sourceCode);

        return lToks;
        //return Arrays.toString((lToks));
    }

    public static HTok[] highlight(CodeLanguage codeLanguage, String sourceCode) {
        Resolver resolver = getResolverByLang(codeLanguage);
        HTok[] hToks = resolver.highlight(sourceCode);
        return hToks;
        //return Arrays.toString(hToks);
    }

    public static Resolver getResolverByLang(CodeLanguage lang) {
        Resolver resolver;

        switch (lang) {
            case JAVA:
                resolver = new JavaResolver();
                return resolver;
            case PYTHON3:
                resolver = new Python3Resolver();
                return resolver;
            case KOTLIN:
                resolver = new KotlinResolver();
                return resolver;
            default:
                throw new IllegalArgumentException("Please provide a code language!");
        }
    }

    public static AnnotationEntity getAnnotationEntityByPostDTO(AnnotationPostDTO annotationPostDTO) {

        AnnotationEntity annotationEntity;

        switch (CodeLanguage.valueOf(annotationPostDTO.getCodeLanguage())) {
            case JAVA:
                annotationEntity = AnnotationMapper.INSTANCE.convertAnnotationPostDTOToJavaEntity(annotationPostDTO);
                return annotationEntity;
            case PYTHON3:
                annotationEntity = AnnotationMapper.INSTANCE.convertAnnotationPostDTOToPythonEntity(annotationPostDTO);
                return annotationEntity;
            case KOTLIN:
                annotationEntity = AnnotationMapper.INSTANCE.convertAnnotationPostDTOToKotlinEntity(annotationPostDTO);
                return annotationEntity;
            default:
                throw new IllegalArgumentException("Please provide a code language!");
        }

    }
}
