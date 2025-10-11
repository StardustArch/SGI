package com.sia.sia_app.dto;

import lombok.Data;
import java.time.LocalDateTime;

@Data
public class ReportResponse {
    private String token;
    private String status;
    private LocalDateTime createdAt;
    private String message;
    
    public ReportResponse(String token, String status, LocalDateTime createdAt) {
        this.token = token;
        this.status = status;
        this.createdAt = createdAt;
        this.message = "Denúncia recebida com sucesso. Use o token para acompanhar.";
    }
}