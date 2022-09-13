package ch.benlegiang.annotation.api.utils;

import ch.benlegiang.annotation.api.dtos.ParserPostDTO;
import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import ch.benlegiang.annotation.api.enums.CodeLanguage;
import lexer.HTok;
import lexer.LTok;
import resolver.JavaResolver;
import resolver.KotlinResolver;
import resolver.Python3Resolver;
import resolver.Resolver;


import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

public class AnnotationUtil {

    public static LTok[] lex(CodeLanguage codeLanguage, String sourceCode) {
        Resolver resolver = getResolverByLang(codeLanguage);
        LTok[] lToks = resolver.lex(sourceCode);

        return lToks;
    }

    public static HTok[] parse(CodeLanguage codeLanguage, String sourceCode) {
        Resolver resolver = getResolverByLang(codeLanguage);
        HTok[] hToks = resolver.highlight(sourceCode);

        return hToks;
    }

    public static HTok[] highlight(ParserPostDTO parserPostDTO) {
        CodeLanguage codeLanguage = CodeLanguage.valueOf(parserPostDTO.getCodeLanguage());

        Resolver resolver = getResolverByLang(codeLanguage);
        HTok[] hToks = resolver.highlight(parserPostDTO.getSourceCode());
        return hToks;
    }

    public static LTok[] lexSourceCode(AnnotationEntity annotationEntity) {
        LTok[] lToks = lex(annotationEntity.getCodeLanguage(), annotationEntity.getSourceCode());

        if (lToks == null) {
            throw new NullPointerException("Lexing the source code failed");
        }

        return lToks;
    }

    public static List<Integer> getTokenIdsFromLToks(LTok[] lToks) {
        return Arrays.stream(lToks).map(lTok -> lTok.tokenId).collect(Collectors.toList());
    }

    public static List<Integer> getHCodeValuesFromHToks(HTok[] hToks) {
        return Arrays.stream(hToks).map(hTok -> hTok.hCodeValue).collect(Collectors.toList());
    }
    public static List<Integer> parse(ParserPostDTO parserPostDTO) {
        HTok[] hToks = AnnotationUtil.highlight(parserPostDTO);

        if (hToks == null) {
            throw new NullPointerException("Highlighting source code failed");
        }
        return getHCodeValuesFromHToks(hToks);
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
