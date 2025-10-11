package com.sia.sia_app.service;

import org.springframework.stereotype.Service;

import javax.crypto.Cipher;
import java.security.*;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;

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
        } catch (Exception e) {
            throw new RuntimeException("Erro ao gerar par de chaves RSA", e);
        }
    }
    
    public String getPublicKeyPem() {
        byte[] publicKeyBytes = keyPair.getPublic().getEncoded();
        String base64PublicKey = Base64.getEncoder().encodeToString(publicKeyBytes);
        
        return "-----BEGIN PUBLIC KEY-----\n" +
               base64PublicKey.replaceAll("(.{64})", "$1\n") +
               "\n-----END PUBLIC KEY-----";
    }
    
    public String getKeyId() {
        return keyId;
    }
    
    public byte[] decryptWithPrivateKey(byte[] encryptedData) {
        try {
            Cipher cipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-256AndMGF1Padding");
            cipher.init(Cipher.DECRYPT_MODE, keyPair.getPrivate());
            return cipher.doFinal(encryptedData);
        } catch (Exception e) {
            throw new RuntimeException("Erro ao descriptografar com chave privada", e);
        }
    }
    
    public String getPublicKeyForFrontend() {
        // Formato para Web Crypto API
        return Base64.getEncoder().encodeToString(keyPair.getPublic().getEncoded());
    }
}