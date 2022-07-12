package ch.benlegiang.annotationService;

import lexer.LTok;
import resolver.Python3Resolver;

import java.util.Arrays;

public class AnnotationService {
    public static void main(String[] args) {
        Python3Resolver resolver = new Python3Resolver();
        LTok[] lToks = resolver.lex("public class Test {}");
        System.out.println(Arrays.toString(lToks));
    }
}
