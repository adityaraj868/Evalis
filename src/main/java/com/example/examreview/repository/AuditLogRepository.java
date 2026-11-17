package com.example.examreview.repository;

import com.example.examreview.entity.AuditLog;
import org.springframework.data.jpa.repository.EntityGraph;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface AuditLogRepository extends JpaRepository<AuditLog, Long> {

    @EntityGraph(attributePaths = {"user"})
    List<AuditLog> findByUserIdOrderByTimestampDesc(Long userId);

    @EntityGraph(attributePaths = {"user"})
    List<AuditLog> findAllByOrderByTimestampDesc();

    @EntityGraph(attributePaths = {"user"})
    List<AuditLog> findByActionOrderByTimestampDesc(String action);

    @EntityGraph(attributePaths = {"user"})
    List<AuditLog> findByResourceTypeOrderByTimestampDesc(String resourceType);

    @EntityGraph(attributePaths = {"user"})
    @Query("SELECT a FROM AuditLog a WHERE " +
           "(:action IS NULL OR a.action = :action) AND " +
           "(:resourceType IS NULL OR a.resourceType = :resourceType) AND " +
           "(:userId IS NULL OR a.user.id = :userId) " +
           "ORDER BY a.timestamp DESC")
    List<AuditLog> filterLogs(@Param("action") String action,
                              @Param("resourceType") String resourceType,
                              @Param("userId") Long userId);
}
