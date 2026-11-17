package com.example.examreview.service;

import com.example.examreview.entity.AuditLog;
import com.example.examreview.entity.Role;
import com.example.examreview.entity.User;
import com.example.examreview.exception.UnauthorizedAccessException;
import com.example.examreview.repository.AuditLogRepository;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;

@Service
public class AuditService {

    private final AuditLogRepository auditLogRepository;

    public AuditService(AuditLogRepository auditLogRepository) {
        this.auditLogRepository = auditLogRepository;
    }

    @Transactional
    public AuditLog log(User user, String action, String description) {
        AuditLog auditLog = new AuditLog(user, action, description);
        return auditLogRepository.save(auditLog);
    }

    @Transactional
    public AuditLog log(User user, String action, String resourceType, Long resourceId,
                        String previousValue, String updatedValue, String description) {
        AuditLog auditLog = new AuditLog(user, action, resourceType, resourceId, previousValue, updatedValue, description);
        return auditLogRepository.save(auditLog);
    }

    public List<AuditLog> getAllLogs() {
        return auditLogRepository.findAllByOrderByTimestampDesc();
    }

    public List<AuditLog> getLogsByUser(Long userId) {
        return auditLogRepository.findByUserIdOrderByTimestampDesc(userId);
    }

    public List<AuditLog> filterLogs(String action, String resourceType, Long userId) {
        String cleanAction = (action != null && !action.isBlank() && !"ALL".equalsIgnoreCase(action)) ? action.trim() : null;
        String cleanResource = (resourceType != null && !resourceType.isBlank() && !"ALL".equalsIgnoreCase(resourceType)) ? resourceType.trim() : null;
        return auditLogRepository.filterLogs(cleanAction, cleanResource, userId);
    }
}
