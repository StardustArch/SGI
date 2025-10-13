package com.sia.sia_app.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.util.Base64;

@Slf4j
@Service
public class AesEncryptionService {
    
    private static final int GCM_TAG_LENGTH = 128;
    private static final int GCM_IV_LENGTH = 12;
    
    public String decryptAesGcm(byte[] encryptedData, byte[] key, byte[] iv) {
        try {
            log.info("🔓 Iniciando descriptografia AES-GCM");
            log.info("   - Key: {} bytes", key.length);
            log.info("   - IV: {} bytes", iv.length);
            log.info("   - Encrypted data: {} bytes", encryptedData.length);
            
            SecretKey secretKey = new SecretKeySpec(key, "AES");
            Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
            GCMParameterSpec spec = new GCMParameterSpec(GCM_TAG_LENGTH, iv);
            cipher.init(Cipher.DECRYPT_MODE, secretKey, spec);
            
            byte[] decryptedData = cipher.doFinal(encryptedData);
            String result = new String(decryptedData);
            
            log.info("✅ Descriptografia AES-GCM bem-sucedida");
            log.info("   - Texto descriptografado: {} caracteres", result.length());
            
            return result;
            
        } catch (Exception e) {
            log.error("❌ Erro na descriptografia AES-GCM: {}", e.getMessage());
            throw new RuntimeException("Erro ao descriptografar AES-GCM: " + e.getMessage(), e);
        }
    }
}