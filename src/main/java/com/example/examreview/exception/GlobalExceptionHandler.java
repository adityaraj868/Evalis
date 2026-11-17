package com.example.examreview.exception;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.http.HttpStatus;
import org.springframework.security.access.AccessDeniedException;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import org.springframework.web.bind.annotation.ResponseStatus;

@ControllerAdvice
public class GlobalExceptionHandler {

    private static final Logger log = LoggerFactory.getLogger(GlobalExceptionHandler.class);

    @ExceptionHandler(UnauthorizedAccessException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public String handleUnauthorizedAccess(UnauthorizedAccessException ex, Model model) {
        log.warn("Unauthorized access attempt: {}", ex.getMessage());
        model.addAttribute("errorMessage", ex.getMessage());
        return "error/403";
    }

    @ExceptionHandler(AccessDeniedException.class)
    @ResponseStatus(HttpStatus.FORBIDDEN)
    public String handleSpringSecurityAccessDenied(AccessDeniedException ex, Model model) {
        log.warn("Access denied: {}", ex.getMessage());
        model.addAttribute("errorMessage", "You do not have permission to access this resource.");
        return "error/403";
    }

    @ExceptionHandler(ResourceNotFoundException.class)
    @ResponseStatus(HttpStatus.NOT_FOUND)
    public String handleResourceNotFound(ResourceNotFoundException ex, Model model) {
        log.info("Resource not found: {}", ex.getMessage());
        model.addAttribute("errorMessage", ex.getMessage());
        return "error/404";
    }

    @ExceptionHandler(InvalidStateTransitionException.class)
    @ResponseStatus(HttpStatus.BAD_REQUEST)
    public String handleInvalidStateTransition(InvalidStateTransitionException ex, Model model) {
        log.warn("Invalid state transition: {}", ex.getMessage());
        model.addAttribute("errorMessage", ex.getMessage());
        return "error/400";
    }

    @ExceptionHandler(DuplicateRequestException.class)
    @ResponseStatus(HttpStatus.CONFLICT)
    public String handleDuplicateRequest(DuplicateRequestException ex, Model model) {
        log.warn("Duplicate request conflict: {}", ex.getMessage());
        model.addAttribute("errorMessage", ex.getMessage());
        return "error/400";
    }
}
