package ch.benlegiang.annotation.api.utils;

import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import ch.benlegiang.annotation.api.enums.CodeLanguage;
import lexer.HTok;
import lexer.LTok;
import resolver.JavaResolver;
import resolver.KotlinResolver;
import resolver.Python3Resolver;
import resolver.Resolver;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class AnnotationUtil {

    public static LTok[] lex(CodeLanguage codeLanguage, String sourceCode) {
        Resolver resolver = getResolverByLang(codeLanguage);
        LTok[] lToks = resolver.lex(sourceCode);

        return lToks;
    }

    public static HTok[] highlight(CodeLanguage codeLanguage, String sourceCode) {
        Resolver resolver = getResolverByLang(codeLanguage);
        HTok[] hToks = resolver.highlight(sourceCode);
        return hToks;
    }

    public static List<Integer> lexSourceCode(AnnotationEntity annotationEntity) {
        LTok[] lToks = lex(annotationEntity.getCodeLanguage(), annotationEntity.getSourceCode());
        List<Integer> tokenIds = new ArrayList<>();

        for (LTok lTok : lToks) {
            tokenIds.add(lTok.tokenId);
        }
        return tokenIds;
    }

    public static List<Integer> highlightSourceCode(AnnotationEntity annotationEntity) {
        HTok[] hToks = AnnotationUtil.highlight(annotationEntity.getCodeLanguage(), annotationEntity.getSourceCode());
        List<Integer> hCodeValues = new ArrayList<>();
        for (HTok hTok : hToks) {
            hCodeValues.add(hTok.hCodeValue);
        }
        return hCodeValues;
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
                throw new IllegalArgumentException("Only Python3, Java and Kotlin are supported!");
        }
    }
}
