package com.sia.sia_app.service;

import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

import javax.crypto.Cipher;
import javax.crypto.spec.OAEPParameterSpec;
import javax.crypto.spec.PSource;

import java.security.KeyPair;
import java.security.KeyPairGenerator;
import java.security.PrivateKey;
import java.security.spec.MGF1ParameterSpec;
import java.util.Base64;

@Slf4j
@Service
public class RsaKeyService {

    private KeyPair keyPair;
    private final String keyId = "server-key-1";

    public RsaKeyService() {
        generateKeyPair();
    }

    private void generateKeyPair() {
        try {
            KeyPairGenerator keyGen = KeyPairGenerator.getInstance("RSA");
            keyGen.initialize(2048);
            this.keyPair = keyGen.generateKeyPair();
            log.info("✅ Par de chaves RSA gerado - Tamanho: 2048 bits");
        } catch (Exception e) {
            throw new RuntimeException("Erro ao gerar par de chaves RSA", e);
        }
    }

    public String getKeyId() {
        return keyId;
    }

    // NOVO MÉTODO: Para acessar a chave privada no DebugController
    public PrivateKey getPrivateKey() {
        return keyPair.getPrivate();
    }

    public byte[] decryptWithPrivateKey(byte[] encryptedData) {
        try {
            log.info("🔓 Iniciando descriptografia RSA - Dados: {} bytes", encryptedData.length);

            Cipher cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding");
            OAEPParameterSpec oaepParams = new OAEPParameterSpec(
                    "SHA-256", // Hash principal
                    "MGF1", // MGF1
                    MGF1ParameterSpec.SHA256, // Hash dentro do MGF1
                    PSource.PSpecified.DEFAULT);

            cipher.init(Cipher.DECRYPT_MODE, keyPair.getPrivate(), oaepParams);

            byte[] decryptedData = cipher.doFinal(encryptedData);
            log.info("✅ Descriptografia RSA bem-sucedida - Resultado: {} bytes", decryptedData.length);

            return decryptedData;

        } catch (Exception e) {
            log.error("❌ Erro na descriptografia RSA: {}", e.getMessage());
            log.error("Detalhes do erro:", e);
            throw new RuntimeException("Erro ao descriptografar com chave privada: " + e.getMessage(), e);
        }
    }

    public String getPublicKeyForFrontend() {
        byte[] publicKeyBytes = keyPair.getPublic().getEncoded();
        String base64Key = Base64.getEncoder().encodeToString(publicKeyBytes);
        log.info("🔑 Chave pública enviada para frontend: {} caracteres Base64", base64Key.length());
        return base64Key;
    }
}