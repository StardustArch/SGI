package com.sia.sia_app.dto;


import lombok.Data;

@Data
public class AiAnalysisResponse {
    private String category;
    private Double confidence;
    private String summary;
    private String redactedText;
    
    // Construtor padrão para deserialização
    public AiAnalysisResponse() {}
}
