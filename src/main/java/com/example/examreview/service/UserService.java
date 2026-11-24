package com.example.examreview.service;

import com.example.examreview.dto.RegisterFormDto;
import com.example.examreview.entity.*;
import com.example.examreview.exception.UnauthorizedAccessException;
import com.example.examreview.exception.ValidationException;
import com.example.examreview.repository.*;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Optional;

@Service
public class UserService {

    private final UserRepository userRepository;
    private final PasswordEncoder passwordEncoder;
    private final ExamRepository examRepository;
    private final QuestionRepository questionRepository;
    private final StudentResultRepository studentResultRepository;
    private final QuestionMarkRepository questionMarkRepository;
    private final AuditService auditService;

    public UserService(UserRepository userRepository,
                       PasswordEncoder passwordEncoder,
                       ExamRepository examRepository,
                       QuestionRepository questionRepository,
                       StudentResultRepository studentResultRepository,
                       QuestionMarkRepository questionMarkRepository,
                       AuditService auditService) {
        this.userRepository = userRepository;
        this.passwordEncoder = passwordEncoder;
        this.examRepository = examRepository;
        this.questionRepository = questionRepository;
        this.studentResultRepository = studentResultRepository;
        this.questionMarkRepository = questionMarkRepository;
        this.auditService = auditService;
    }

    @Transactional
    public User registerStudent(RegisterFormDto dto) {
        if (dto.getName() == null || dto.getName().trim().length() < 2) {
            throw new ValidationException("Full name must be at least 2 characters.");
        }
        if (dto.getEmail() == null || !dto.getEmail().contains("@")) {
            throw new ValidationException("Please provide a valid email address.");
        }
        if (userRepository.findByEmail(dto.getEmail().trim().toLowerCase()).isPresent()) {
            throw new ValidationException("An account with this email address already exists.");
        }
        if (dto.getPassword() == null || dto.getPassword().length() < 6) {
            throw new ValidationException("Password must be at least 6 characters.");
        }
        if (!dto.getPassword().equals(dto.getConfirmPassword())) {
            throw new ValidationException("Passwords do not match.");
        }

        User student = new User(
                dto.getName().trim(),
                dto.getEmail().trim().toLowerCase(),
                passwordEncoder.encode(dto.getPassword()),
                Role.STUDENT
        );
        student = userRepository.save(student);

        // Auto-enroll new student into active exams so they have sample marks to inspect and dispute
        List<Exam> activeExams = examRepository.findAll().stream()
                .filter(e -> e.getStatus() == ExamStatus.RE_EVALUATION_OPEN || e.getStatus() == ExamStatus.PUBLISHED)
                .toList();

        for (Exam exam : activeExams) {
            List<Question> questions = questionRepository.findByExamIdOrderByQuestionNumberAsc(exam.getId());
            double totalMarks = 0.0;
            for (Question q : questions) {
                // Award a baseline mark (e.g., 60-70% of max marks)
                double baseline = Math.max(1.0, Math.round(q.getMaxMarks() * 0.65 * 2.0) / 2.0);
                questionMarkRepository.save(new QuestionMark(student, q, baseline));
                totalMarks += baseline;
            }
            studentResultRepository.save(new StudentResult(student, exam, totalMarks));
        }

        auditService.log(student, "STUDENT_REGISTERED", "USER", student.getId(), null,
                student.getEmail(), "New student self-registered: " + student.getEmail());

        return student;
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
