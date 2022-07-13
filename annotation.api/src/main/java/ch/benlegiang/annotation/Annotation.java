package ch.benlegiang.annotation;

import ch.benlegiang.annotation.enums.CodeLanguage;
import lexer.*;
import resolver.*;

import java.util.Arrays;

public class Annotation {

    public static void main(String[] args) {

        String code = "def my_function():\n" +
                "  print(\"Hello from a function\")";

        String lexed = lex(code, CodeLanguage.PYTHON3);
        String highlighted = highlight(code, CodeLanguage.PYTHON3);

        System.out.println("Lexed: " + lexed);
        System.out.println("Highlighted : " + highlighted);

    }
    private static String lex(String code, CodeLanguage lang) {
        Resolver resolver = getResolverByLang(lang);
        LTok[] lToks = resolver.lex(code);

        return Arrays.toString((lToks));
    }

    private static String highlight(String code, CodeLanguage lang) {
        Resolver resolver = getResolverByLang(lang);
        HTok[] hToks = resolver.highlight(code);
        return Arrays.toString(hToks);
    }


    private static Resolver getResolverByLang(CodeLanguage lang) {
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

