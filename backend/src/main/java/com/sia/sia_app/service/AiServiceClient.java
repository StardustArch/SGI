package com.sia.sia_app.service;


import com.sia.sia_app.dto.AiAnalysisRequest;
import com.sia.sia_app.dto.AiAnalysisResponse;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

@Slf4j
@Service
public class AiServiceClient {

    @Value("${app.ai-service.url:http://ai-service:8000}")
    private static String aiServiceUrl;

    @Autowired
    private static RestTemplate restTemplate;

    public AiAnalysisResponse analyzeText(String text) {
        try {
            log.info("Enviando texto para análise IA: {} caracteres", text.length());
            
            AiAnalysisRequest request = new AiAnalysisRequest(text);
            
            ResponseEntity<AiAnalysisResponse> response = restTemplate.postForEntity(
                aiServiceUrl + "/analyze",
                request,
                AiAnalysisResponse.class
            );

            if (response.getStatusCode().is2xxSuccessful() && response.getBody() != null) {
                log.info("Análise IA concluída: {}", response.getBody().getCategory());
                return response.getBody();
            } else {
                throw new RuntimeException("Resposta inválida do AI Service: " + response.getStatusCode());
            }

        } catch (Exception e) {
            log.error("Erro ao comunicar com AI Service: {}", e.getMessage());
            throw new RuntimeException("Falha na análise IA: " + e.getMessage(), e);
        }
    }

    public static boolean isHealthy() {
        try {
            ResponseEntity<String> response = restTemplate.getForEntity(
                aiServiceUrl + "/health", 
                String.class
            );
            return response.getStatusCode().is2xxSuccessful();
        } catch (Exception e) {
            log.warn("AI Service não está saudável: {}", e.getMessage());
            return false;
        }
    }
}