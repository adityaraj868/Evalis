package com.example.examreview.service;

import com.example.examreview.entity.Role;
import com.example.examreview.entity.User;
import com.example.examreview.exception.UnauthorizedAccessException;
import com.example.examreview.repository.UserRepository;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Service;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    private final UserRepository userRepository;

    public UserService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    public Optional<User> findByEmail(String email) {
        return userRepository.findByEmail(email);
    }

    public Optional<User> findById(Long id) {
        return userRepository.findById(id);
    }

    public User getCurrentUser() {
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth == null || !auth.isAuthenticated() || "anonymousUser".equals(auth.getPrincipal())) {
            return null;
        }
        return userRepository.findByEmail(auth.getName()).orElse(null);
    }

    public User getRequiredCurrentUser() {
        User user = getCurrentUser();
        if (user == null) {
            throw new UnauthorizedAccessException("Authentication required to perform this action.");
        }
        return user;
    }

    public void validateRole(User user, Role expectedRole) {
        if (user == null || user.getRole() != expectedRole) {
            throw new UnauthorizedAccessException("Operation requires role: " + expectedRole);
        }
    }

    public List<User> findAllStudents() {
        return userRepository.findByRole(Role.STUDENT);
    }

    public List<User> findAllFaculty() {
        return userRepository.findByRole(Role.FACULTY);
    }

    public List<User> findAllUsers() {
        return userRepository.findAll();
    }
}
