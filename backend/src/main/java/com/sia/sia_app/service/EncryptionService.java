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
            log.info("EncryptedBlob (Base64): {} caracteres", encryptedBlobBase64.length());
            log.info("WrappedKey (Base64): {} caracteres", wrappedKeyBase64.length());
            
            // 1. Desembrulhar a DEK usando RSA
            byte[] wrappedKey = Base64.getDecoder().decode(wrappedKeyBase64);
            log.info("WrappedKey decodificado: {} bytes", wrappedKey.length);
            
            byte[] dek = rsaKeyService.decryptWithPrivateKey(wrappedKey);
            log.info("DEK desembrulhada: {} bytes", dek.length);
            
            // 2. Decodificar o blob cifrado
            byte[] encryptedData = Base64.getDecoder().decode(encryptedBlobBase64);
            log.info("EncryptedData decodificado: {} bytes", encryptedData.length);
            
            // Verificar se temos dados suficientes para IV + ciphertext
            if (encryptedData.length < 12) {
                throw new RuntimeException("Dados criptografados insuficientes para conter IV");
            }
            
            // Extrair IV (primeiros 12 bytes) e dados cifrados
            byte[] iv = new byte[12];
            byte[] ciphertext = new byte[encryptedData.length - 12];
            System.arraycopy(encryptedData, 0, iv, 0, 12);
            System.arraycopy(encryptedData, 12, ciphertext, 0, ciphertext.length);
            
            log.info("IV extraído: {} bytes", iv.length);
            log.info("Ciphertext extraído: {} bytes", ciphertext.length);
            
            // 3. Descriptografar com AES-GCM
            String decryptedText = aesEncryptionService.decryptAesGcm(ciphertext, dek, iv);
            
            log.info("Texto descriptografado: {} caracteres", decryptedText.length());
            log.info("Primeiros 50 caracteres: {}", 
                decryptedText.length() > 50 ? decryptedText.substring(0, 50) + "..." : decryptedText);
            
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