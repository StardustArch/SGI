package com.sia.sia_app.service;

import org.springframework.stereotype.Service;

import java.security.MessageDigest;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
import java.util.UUID;

@Service
public class TokenService {

    private static final String TOKEN_PREFIX = "DC";
    
    public String generateToken() {
        String randomPart = UUID.randomUUID().toString().replace("-", "").substring(0, 12).toUpperCase();
        return TOKEN_PREFIX + randomPart;
    }
    
    public String hashToken(String token) {
        try {
            MessageDigest digest = MessageDigest.getInstance("SHA-256");
            byte[] hash = digest.digest(token.getBytes());
            return bytesToHex(hash);
        } catch (NoSuchAlgorithmException e) {
            throw new RuntimeException("Erro ao gerar hash do token", e);
        }
    }
    
    private String bytesToHex(byte[] bytes) {
        StringBuilder hexString = new StringBuilder();
        for (byte b : bytes) {
            String hex = Integer.toHexString(0xff & b);
            if (hex.length() == 1) {
                hexString.append('0');
            }
            hexString.append(hex);
        }
        return hexString.toString();
    }
    
    public boolean verifyToken(String token, String storedHash) {
        return hashToken(token).equals(storedHash);
    }
}