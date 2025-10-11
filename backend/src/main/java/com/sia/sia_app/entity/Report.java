package com.sia.sia_app.entity;

import jakarta.persistence.*;
import lombok.Data;
import org.hibernate.annotations.CreationTimestamp;
import org.hibernate.annotations.UpdateTimestamp;

import java.time.LocalDateTime;
import java.util.UUID;

@Data
@Entity
@Table(name = "reports")
public class Report {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(name = "encrypted_blob", columnDefinition = "TEXT", nullable = false)
    private String encryptedBlob;

    @Column(name = "wrapped_key", columnDefinition = "TEXT", nullable = false)
    private String wrappedKey;

    @Column(name = "token_hash", nullable = false, unique = true, length = 64)
    private String tokenHash;

    @Column(name = "status", length = 20)
    private String status = "RECEIVED";

    @Column(name = "category", length = 50)
    private String category;

    @Column(name = "priority_score")
    private Integer priorityScore;

    @Column(name = "redacted_summary", columnDefinition = "TEXT")
    private String redactedSummary;

    @Column(name = "analysis_json", columnDefinition = "TEXT")
    private String analysisJson;

    @CreationTimestamp
    @Column(name = "created_at", updatable = false)
    private LocalDateTime createdAt;

    @UpdateTimestamp
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;

    // Construtor padrão
    public Report() {
    }

    // Construtor para criação de novas denúncias
    public Report(String encryptedBlob, String wrappedKey, String tokenHash) {
        this.encryptedBlob = encryptedBlob;
        this.wrappedKey = wrappedKey;
        this.tokenHash = tokenHash;
        this.status = "RECEIVED";
    }
}