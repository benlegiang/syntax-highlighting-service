package ch.benlegiang.annotation.api.services;

import ch.benlegiang.annotation.api.entities.AnnotationEntity;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.ObjectReader;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Service;

import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

import java.io.IOException;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

@Service
public class PredictionService {

    private final WebClient webClient;


    public PredictionService(WebClient.Builder webClientBuilder) {
        // this.webClient = webClientBuilder.baseUrl("http://syntax-highlighting-service-prediction-api:8000").build();
        this.webClient = webClientBuilder.baseUrl("http://localhost:8000").build();

    }

    public AnnotationEntity setPrediction(AnnotationEntity annotationEntity) throws IOException {

        Map<String, Object> requestBody = new HashMap();

        requestBody.put("codeLanguage", annotationEntity.getCodeLanguage());
        requestBody.put("tokenIds", annotationEntity.getTokenIds());

        String response = this.webClient.post()
                .uri("/predict")
                .header("Content-Type", "application/json")
                .contentType(MediaType.APPLICATION_JSON)
                .accept(MediaType.APPLICATION_JSON)
                .body(BodyInserters.fromValue(requestBody))
                .retrieve()
                .bodyToMono(String.class)
                .block();

        ObjectMapper mapper = new ObjectMapper();
        JsonNode rootNode = mapper.readTree(response).get("prediction");

        ObjectReader reader = mapper.readerFor(new TypeReference<List<Integer>>() {
        });

        List<Integer> prediction = reader.readValue(rootNode);

        annotationEntity.setPrediction(prediction);

        return annotationEntity;
    }
}
