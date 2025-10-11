package com.sia.sia_app.service;

import com.sia.sia_app.dto.AiAnalysisResponse;
import com.sia.sia_app.entity.Report;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Base64;

@Slf4j
@Service
public class EncryptionService {

    @Autowired
    private RsaKeyService rsaKeyService;
    
    @Autowired
    private AesEncryptionService aesEncryptionService;
    
    @Autowired
    private AiServiceClient aiServiceClient;

    public String decryptReport(String encryptedBlobBase64, String wrappedKeyBase64) {
        try {
            log.info("Iniciando descriptografia do relatório");
            
            // 1. Desembrulhar a DEK usando RSA
            byte[] wrappedKey = Base64.getDecoder().decode(wrappedKeyBase64);
            byte[] dek = rsaKeyService.decryptWithPrivateKey(wrappedKey);
            
            log.info("DEK desembrulhada: {} bytes", dek.length);
            
            // 2. Decodificar o blob cifrado (formato: IV + dados cifrados)
            byte[] encryptedData = Base64.getDecoder().decode(encryptedBlobBase64);
            
            // Extrair IV (primeiros 12 bytes) e dados cifrados
            byte[] iv = new byte[12];
            byte[] ciphertext = new byte[encryptedData.length - 12];
            System.arraycopy(encryptedData, 0, iv, 0, 12);
            System.arraycopy(encryptedData, 12, ciphertext, 0, ciphertext.length);
            
            log.info("IV extraído: {} bytes, Ciphertext: {} bytes", iv.length, ciphertext.length);
            
            // 3. Descriptografar com AES-GCM
            String decryptedText = aesEncryptionService.decryptAesGcm(ciphertext, dek, iv);
            
            log.info("Texto descriptografado: {} caracteres", decryptedText.length());
            
            return decryptedText;
            
        } catch (Exception e) {
            log.error("Erro na descriptografia: {}", e.getMessage(), e);
            throw new RuntimeException("Falha na descriptografia: " + e.getMessage(), e);
        }
    }

    public AiAnalysisResponse processReport(Report report) {
        try {
            log.info("Processando relatório ID: {}", report.getId());
            
            // 1. Descriptografar
            String decryptedText = decryptReport(report.getEncryptedBlob(), report.getWrappedKey());
            
            // 2. Enviar para análise IA
            AiAnalysisResponse analysis = aiServiceClient.analyzeText(decryptedText);
            
            log.info("Análise IA concluída: {} (confiança: {})", 
                analysis.getCategory(), analysis.getConfidence());
            
            return analysis;
            
        } catch (Exception e) {
            log.error("Erro no processamento do relatório: {}", e.getMessage(), e);
            throw new RuntimeException("Falha no processamento: " + e.getMessage(), e);
        }
    }
}