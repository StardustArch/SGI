package com.sia.sia_app.controller;

import com.sia.sia_app.dto.AiAnalysisResponse;
import com.sia.sia_app.dto.ReportRequest;
import com.sia.sia_app.dto.ReportResponse;
import com.sia.sia_app.entity.Report;
import com.sia.sia_app.repository.ReportRepository;
import com.sia.sia_app.service.TokenService;
import jakarta.validation.Valid;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import com.sia.sia_app.service.AiServiceClient;
import com.sia.sia_app.service.EncryptionService;

import java.util.Map;
import java.util.UUID;

@Slf4j
@RestController
@RequestMapping("/api/v1/reports")
public class ReportController {

    @Autowired
    private ReportRepository reportRepository;

    @Autowired
    private TokenService tokenService;

    @Autowired
    private EncryptionService encryptionService;

    @PostMapping
    public ResponseEntity<ReportResponse> submitReport(@Valid @RequestBody ReportRequest request) {
        try {
            log.info("Recebendo nova denúncia - Tamanho do blob: {} bytes", request.getEncryptedBlob().length());

            // Gerar token público e hash
            String publicToken = tokenService.generateToken();
            String tokenHash = tokenService.hashToken(publicToken);

            log.info("Token gerado: {} (hash: {})", publicToken, tokenHash.substring(0, 16) + "...");

            // Criar e salvar entidade
            Report report = new Report();
            report.setEncryptedBlob(request.getEncryptedBlob());
            report.setWrappedKey(request.getWrappedKey());
            report.setTokenHash(tokenHash);
            report.setStatus("RECEIVED");

            Report savedReport = reportRepository.save(report);
            log.info("Denúncia salva com ID: {}", savedReport.getId());

            // Retornar resposta
            ReportResponse response = new ReportResponse(
                    publicToken,
                    savedReport.getStatus(),
                    savedReport.getCreatedAt());

            return ResponseEntity.ok(response);

        } catch (Exception e) {
            log.error("Erro ao processar denúncia: {}", e.getMessage(), e);
            return ResponseEntity.internalServerError().build();
        }
    }

    @GetMapping("/status/{token}")
    public ResponseEntity<?> getReportStatus(@PathVariable String token) {
        try {
            String tokenHash = tokenService.hashToken(token);

            return reportRepository.findByTokenHash(tokenHash)
                    .map(report -> ResponseEntity.ok().body(
                            new ReportResponse(token, report.getStatus(), report.getCreatedAt())))
                    .orElse(ResponseEntity.notFound().build());

        } catch (Exception e) {
            log.error("Erro ao consultar status: {}", e.getMessage());
            return ResponseEntity.badRequest().body("Token inválido");
        }
    }

@PostMapping("/{id}/process")
public ResponseEntity<?> processReport(@PathVariable UUID id) {
    try {
        Report report = reportRepository.findById(id)
                .orElseThrow(() -> new RuntimeException("Denúncia não encontrada"));

        log.info("Processando denúncia ID: {}", id);

        // Verificar se AI Service está saudável
        try {
            if (!AiServiceClient.isHealthy()) {
                return ResponseEntity.status(503).body(Map.of(
                    "error", "Serviço de IA indisponível",
                    "status", "service_unavailable"
                ));
            }
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }

        // Processar com IA real
        AiAnalysisResponse analysis = encryptionService.processReport(report);
        
        // Atualizar relatório com resultados da análise
        report.setCategory(analysis.getCategory());
        report.setPriorityScore((int) (analysis.getConfidence() * 100));
        report.setRedactedSummary(analysis.getSummary());
        report.setAnalysisJson("{\"confidence\": " + analysis.getConfidence() + 
                              ", \"redacted_text\": \"" + analysis.getRedactedText() + "\"}");
        report.setStatus("ANALYZED");

        Report updatedReport = reportRepository.save(report);

        log.info("Denúncia processada com sucesso: {}", updatedReport.getId());

        return ResponseEntity.ok().body(Map.of(
            "status", "processed",
            "reportId", updatedReport.getId(),
            "category", updatedReport.getCategory(),
            "confidence", analysis.getConfidence(),
            "summary", analysis.getSummary()
        ));

    } catch (Exception e) {
        log.error("Erro ao processar denúncia: {}", e.getMessage(), e);
        return ResponseEntity.internalServerError()
                .body(Map.of("error", "Erro no processamento: " + e.getMessage()));
    }
}
}