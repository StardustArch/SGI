package com.sia.sia_app.dto;

import jakarta.validation.constraints.NotBlank;
import lombok.Data;

@Data
public class ReportRequest {
    
    @NotBlank(message = "encryptedBlob é obrigatório")
    private String encryptedBlob;
    
    @NotBlank(message = "wrappedKey é obrigatório") 
    private String wrappedKey;
}