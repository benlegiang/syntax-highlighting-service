package ch.benlegiang.annotation.api.utils;

import ch.benlegiang.annotation.api.enums.CodeLanguage;
import lexer.HTok;
import lexer.LTok;
import resolver.JavaResolver;
import resolver.KotlinResolver;
import resolver.Python3Resolver;
import resolver.Resolver;

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
}
