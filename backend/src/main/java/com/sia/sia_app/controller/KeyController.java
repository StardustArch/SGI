package com.sia.sia_app.controller;

import com.sia.sia_app.dto.PublicKeyResponse;
import com.sia.sia_app.service.RsaKeyService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api/v1/keys")
public class KeyController {

    @Autowired
    private RsaKeyService rsaKeyService;

    @GetMapping("/public")
    public PublicKeyResponse getPublicKey() {
        return new PublicKeyResponse(
            rsaKeyService.getKeyId(),
            rsaKeyService.getPublicKeyForFrontend()
        );
    }
}