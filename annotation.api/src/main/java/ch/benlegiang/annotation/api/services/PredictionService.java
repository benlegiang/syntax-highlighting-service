package ch.benlegiang.annotation.api.services;

import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class PredictionService {

    private final WebClient webClient;


    public PredictionService(WebClient.Builder webClientBuilder) {
        this.webClient = webClientBuilder.baseUrl("http://syntax-highlighting-service-prediction-api:5555").build();
        // this.webClient = webClientBuilder.baseUrl("http://localhost:5555").build();

    }

    public void predict() {

        // MultiValueMap<String, String> bodyValues = new LinkedMultiValueMap<>();

        String response = this.webClient.post()
                .uri("/predict")
                .retrieve()
                .bodyToMono(String.class)
                .block();

    }
}