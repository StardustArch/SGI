package com.sia.sia_app.dto;

public class PublicKeyResponse {
    private String keyId;
    private String publicKeyPem;
    private String algorithm;
    
    public PublicKeyResponse(String keyId, String publicKeyPem) {
        this.keyId = keyId;
        this.publicKeyPem = publicKeyPem;
        this.algorithm = "RSA-OAEP";
    }
    
    // Getters
    public String getKeyId() { return keyId; }
    public String getPublicKeyPem() { return publicKeyPem; }
    public String getAlgorithm() { return algorithm; }
}
