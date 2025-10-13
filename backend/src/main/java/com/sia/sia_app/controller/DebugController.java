package com.sia.sia_app.controller;

import com.sia.sia_app.service.RsaKeyService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.security.spec.MGF1ParameterSpec;
import java.util.Base64;
import java.util.HashMap;
import java.util.Map;

import javax.crypto.Cipher;
import javax.crypto.spec.OAEPParameterSpec;
import javax.crypto.spec.PSource;

@Slf4j
@RestController
@RequestMapping("/api/v1/debug")
public class DebugController {

    @Autowired
    private RsaKeyService rsaKeyService;

    /**
     * Teste apenas a descriptografia RSA com diferentes algoritmos
     */
    @PostMapping("/test-rsa-only")
    public Map<String, Object> testRsaOnly(@RequestBody Map<String, String> request) {
        try {
            String wrappedKeyBase64 = request.get("wrappedKey");

            log.info("🔍 TESTE RSA APENAS - INICIANDO");
            log.info("WrappedKey recebido: {} caracteres Base64", wrappedKeyBase64.length());
            log.info("WrappedKey (primeiros 50 chars): {}...",
                    wrappedKeyBase64.length() > 50 ? wrappedKeyBase64.substring(0, 50) : wrappedKeyBase64);

            // Decodificar Base64
            byte[] wrappedKey = Base64.getDecoder().decode(wrappedKeyBase64);
            log.info("WrappedKey decodificado: {} bytes", wrappedKey.length);

            // Log dos primeiros bytes em HEX para debug
            StringBuilder hex = new StringBuilder();
            for (int i = 0; i < Math.min(16, wrappedKey.length); i++) {
                hex.append(String.format("%02X ", wrappedKey[i]));
            }
            log.info("Primeiros bytes (HEX): {}", hex.toString());

            // Testar diferentes algoritmos de descriptografia
            Map<String, Object> results = new HashMap<>();
            String[] algorithms = {
                    "RSA/ECB/OAEPWithSHA-1AndMGF1Padding",
                    "RSA/ECB/OAEPWithSHA-256AndMGF1Padding",
                    "RSA/ECB/PKCS1Padding"
            };

            for (String algorithm : algorithms) {
                try {
                    log.info("🧪 Testando algoritmo: {}", algorithm);

                    Cipher cipher = Cipher.getInstance(algorithm);

                    if (algorithm.equals("RSA/ECB/OAEPWithSHA-256AndMGF1Padding")) {
                        // ⚙️ Corrige o MGF1 para SHA-256 — compatível com WebCrypto
                        OAEPParameterSpec oaepParams = new OAEPParameterSpec(
                                "SHA-256", // Hash principal
                                "MGF1", // MGF1
                                MGF1ParameterSpec.SHA256, // Hash dentro do MGF1
                                PSource.PSpecified.DEFAULT);
                        cipher.init(Cipher.DECRYPT_MODE, rsaKeyService.getPrivateKey(), oaepParams);
                    } else {
                        // Outros algoritmos usam init padrão
                        cipher.init(Cipher.DECRYPT_MODE, rsaKeyService.getPrivateKey());
                    }

                    // Tentar descriptografar
                    byte[] dek = cipher.doFinal(wrappedKey);
                    log.info("✅ {}: SUCESSO - {} bytes descriptografados", algorithm, dek.length);

                    StringBuilder dekHex = new StringBuilder();
                    for (int i = 0; i < Math.min(8, dek.length); i++) {
                        dekHex.append(String.format("%02X ", dek[i]));
                    }

                    results.put(algorithm, Map.of(
                            "status", "SUCCESS",
                            "dekLength", dek.length,
                            "dekFirstBytesHex", dekHex.toString().trim(),
                            "dekBase64", Base64.getEncoder().encodeToString(dek)));

                } catch (Exception e) {
                    log.info("❌ {}: ERRO - {}", algorithm, e.getMessage());
                    results.put(algorithm, Map.of(
                            "status", "ERROR",
                            "error", e.getMessage(),
                            "errorType", e.getClass().getSimpleName()));
                }
            }

            Map<String, Object> response = new HashMap<>();
            response.put("testType", "RSA_DECRYPTION_ONLY");
            response.put("inputWrappedKeyLength", wrappedKeyBase64.length());
            response.put("inputWrappedKeyBytes", wrappedKey.length);
            response.put("algorithmsTested", results);

            log.info("🔍 TESTE RSA APENAS - CONCLUSÃO");
            return response;

        } catch (Exception e) {
            log.error("❌ ERRO GERAL no teste RSA: {}", e.getMessage(), e);
            return Map.of(
                    "status", "ERROR",
                    "error", e.getMessage(),
                    "errorType", e.getClass().getSimpleName());
        }
    }

    /**
     * Teste completo de descriptografia (RSA + AES)
     */
    @PostMapping("/test-complete-decrypt")
    public Map<String, Object> testCompleteDecryption(@RequestBody Map<String, String> request) {
        try {
            String encryptedBlob = request.get("encryptedBlob");
            String wrappedKey = request.get("wrappedKey");

            log.info("🔍 TESTE COMPLETO - INICIANDO");
            log.info("EncryptedBlob: {} caracteres", encryptedBlob.length());
            log.info("WrappedKey: {} caracteres", wrappedKey.length());
            log.info("Primeiros 30 chars EncryptedBlob: {}...",
                    encryptedBlob.length() > 30 ? encryptedBlob.substring(0, 30) : encryptedBlob);

            // 1. Primeiro testar apenas RSA
            Map<String, Object> rsaResults = testRsaOnly(Map.of("wrappedKey", wrappedKey));

            Map<String, Object> response = new HashMap<>();
            response.put("testType", "COMPLETE_DECRYPTION");
            response.put("rsaTest", rsaResults);

            // Se RSA falhou, não continuar
            if (rsaResults.containsKey("status") && "ERROR".equals(rsaResults.get("status"))) {
                response.put("overallStatus", "RSA_FAILED");
                return response;
            }

            // 2. Se RSA funcionou, tentar descriptografia completa
            // (Você precisaria injetar o EncryptionService aqui)
            response.put("overallStatus", "RSA_SUCCESS_AES_PENDING");
            response.put("message", "RSA funcionou, mas AES não testado (injetar EncryptionService)");

            log.info("🔍 TESTE COMPLETO - CONCLUSÃO");
            return response;

        } catch (Exception e) {
            log.error("❌ ERRO no teste completo: {}", e.getMessage(), e);
            return Map.of(
                    "status", "ERROR",
                    "error", e.getMessage());
        }
    }

    /**
     * Obter informações da chave pública para debug
     */
    @GetMapping("/key-info")
    public Map<String, Object> getKeyInfo() {
        try {
            String publicKeyBase64 = rsaKeyService.getPublicKeyForFrontend();
            byte[] publicKeyBytes = Base64.getDecoder().decode(publicKeyBase64);

            Map<String, Object> keyInfo = new HashMap<>();
            keyInfo.put("keyId", rsaKeyService.getKeyId());
            keyInfo.put("publicKeyBase64Length", publicKeyBase64.length());
            keyInfo.put("publicKeyBytesLength", publicKeyBytes.length);
            keyInfo.put("publicKeyFirst50Chars",
                    publicKeyBase64.substring(0, Math.min(50, publicKeyBase64.length())) + "...");
            keyInfo.put("algorithm", "RSA");
            keyInfo.put("keySize", "2048");

            return keyInfo;

        } catch (Exception e) {
            log.error("Erro ao obter info da chave: {}", e.getMessage());
            return Map.of("error", e.getMessage());
        }
    }

    /**
     * Gerar um teste de criptografia no servidor (para comparar com frontend)
     */
    @GetMapping("/server-encryption-test")
    public Map<String, Object> serverEncryptionTest() {
        try {
            // Este método seria para testar criptografia no servidor
            // e comparar com o que o frontend está fazendo
            return Map.of(
                    "status", "NOT_IMPLEMENTED",
                    "message", "Este endpoint seria para criptografia de teste no servidor");

        } catch (Exception e) {
            return Map.of("error", e.getMessage());
        }
    }
}