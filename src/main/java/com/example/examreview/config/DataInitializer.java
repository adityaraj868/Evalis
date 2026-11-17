package com.example.examreview.config;

import com.example.examreview.entity.*;
import com.example.examreview.repository.*;
import com.example.examreview.service.MarksService;
import org.springframework.boot.CommandLineRunner;
import org.springframework.context.annotation.Profile;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import org.springframework.transaction.annotation.Transactional;

import java.time.LocalDate;
import java.time.LocalDateTime;

@Component
@Profile("!test")
public class DataInitializer implements CommandLineRunner {

    private final UserRepository userRepository;
    private final ExamRepository examRepository;
    private final QuestionRepository questionRepository;
    private final RecheckRequestRepository recheckRequestRepository;
    private final AuditLogRepository auditLogRepository;
    private final PasswordEncoder passwordEncoder;
    private final MarksService marksService;

    public DataInitializer(UserRepository userRepository,
                           ExamRepository examRepository,
                           QuestionRepository questionRepository,
                           RecheckRequestRepository recheckRequestRepository,
                           AuditLogRepository auditLogRepository,
                           PasswordEncoder passwordEncoder,
                           MarksService marksService) {
        this.userRepository = userRepository;
        this.examRepository = examRepository;
        this.questionRepository = questionRepository;
        this.recheckRequestRepository = recheckRequestRepository;
        this.auditLogRepository = auditLogRepository;
        this.passwordEncoder = passwordEncoder;
        this.marksService = marksService;
    }

    @Override
    @Transactional
    public void run(String... args) {
        if (userRepository.count() > 0) {
            return;
        }

        // Seed Users
        User admin = new User("System Administrator", "admin@example.com", passwordEncoder.encode("admin123"), Role.ADMIN);
        User faculty = new User("Prof. Alan Turing", "faculty@example.com", passwordEncoder.encode("faculty123"), Role.FACULTY);
        User student1 = new User("John Student", "student@example.com", passwordEncoder.encode("student123"), Role.STUDENT);
        User student2 = new User("Alice Smith", "alice@example.com", passwordEncoder.encode("alice123"), Role.STUDENT);

        userRepository.save(admin);
        userRepository.save(faculty);
        userRepository.save(student1);
        userRepository.save(student2);

        // Seed Exam: Data Structures Mid-Semester Examination
        Exam exam = new Exam("Data Structures Mid-Semester Examination", "Data Structures & Algorithms",
                LocalDate.now().minusDays(10), LocalDate.now().minusDays(3));
        exam.setStatus(ExamStatus.RE_EVALUATION_OPEN);
        exam.setReevaluationStart(LocalDateTime.now().minusDays(1));
        exam.setReevaluationEnd(LocalDateTime.now().plusDays(7));
        examRepository.save(exam);

        // Seed Questions
        Question q1 = new Question(exam, 1, "Explain asymptotic time complexity of Merge Sort.", 10.0);
        Question q2 = new Question(exam, 2, "Implement insert operation in a Red-Black Tree.", 10.0);
        Question q3 = new Question(exam, 3, "Differentiate between BFS and DFS traversal with code snippets.", 10.0);
        Question q4 = new Question(exam, 4, "Describe Dijkstra's shortest path algorithm with a pseudocode example.", 10.0);
        Question q5 = new Question(exam, 5, "Prove why finding a minimum spanning tree using Kruskal's algorithm is optimal.", 10.0);

        questionRepository.save(q1);
        questionRepository.save(q2);
        questionRepository.save(q3);
        questionRepository.save(q4);
        questionRepository.save(q5);

        // Seed Marks for student1 (matches demo-script: 8, 3, 9, 2, 10)
        marksService.recordMark(student1, q1, 8.0);
        marksService.recordMark(student1, q2, 3.0);
        marksService.recordMark(student1, q3, 9.0);
        marksService.recordMark(student1, q4, 2.0);
        marksService.recordMark(student1, q5, 10.0);

        // Seed Marks for student2
        marksService.recordMark(student2, q1, 7.0);
        marksService.recordMark(student2, q2, 4.0);
        marksService.recordMark(student2, q3, 8.0);
        marksService.recordMark(student2, q4, 3.0);
        marksService.recordMark(student2, q5, 9.0);

        // Seed a recheck request for student2 on Q4
        RecheckRequest requestAlice = new RecheckRequest(student2, exam, q4,
                "The relaxation condition in Dijkstra's step was correctly implemented using priority queues. Please recheck step 4.");
        requestAlice.setStatus(RequestStatus.SUBMITTED);
        recheckRequestRepository.save(requestAlice);

        // Seed initial audit log
        auditLogRepository.save(new AuditLog(admin, "SYSTEM_INIT", "Seeded initial demonstration users, exam, and questions."));
        auditLogRepository.save(new AuditLog(faculty, "EXAM_PUBLISHED", "Published exam results for Data Structures Mid-Semester Examination."));
        auditLogRepository.save(new AuditLog(student2, "REQUEST_SUBMITTED", "Alice Smith submitted recheck request for Q4."));
    }
}
