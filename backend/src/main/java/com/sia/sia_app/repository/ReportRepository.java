package com.sia.sia_app.repository;

import com.sia.sia_app.entity.Report;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.Optional;
import java.util.UUID;

@Repository
public interface ReportRepository extends JpaRepository<Report, UUID> {
    
    Optional<Report> findByTokenHash(String tokenHash);
    
    boolean existsByTokenHash(String tokenHash);
    
    @Query("SELECT r.status FROM Report r WHERE r.tokenHash = :tokenHash")
    Optional<String> findStatusByTokenHash(@Param("tokenHash") String tokenHash);
}