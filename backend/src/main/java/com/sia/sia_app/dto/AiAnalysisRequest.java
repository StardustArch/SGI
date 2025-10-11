package com.sia.sia_app.dto;


import lombok.Data;

@Data
public class AiAnalysisRequest {
    private String text;
    private String language = "pt";

    public AiAnalysisRequest(String text) {
        this.text = text;
    }
}