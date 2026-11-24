package com.example.examreview.security;

import com.example.examreview.entity.*;
import com.example.examreview.repository.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import java.time.LocalDate;

import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestBuilders.formLogin;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
public class SecurityAccessTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ExamRepository examRepository;

    @Autowired
    private QuestionRepository questionRepository;

    @Autowired
    private RecheckRequestRepository recheckRequestRepository;

    @Autowired
    private ReviewRepository reviewRepository;

    @Autowired
    private AuditLogRepository auditLogRepository;

    @Autowired
    private StudentResultRepository studentResultRepository;

    @Autowired
    private QuestionMarkRepository questionMarkRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    private User student1;
    private User student2;
    private User faculty;
    private User admin;
    private Exam testExam;
    private Question question1;
    private RecheckRequest student1Request;

    @BeforeEach
    void setUp() {
        auditLogRepository.deleteAll();
        reviewRepository.deleteAll();
        recheckRequestRepository.deleteAll();
        questionMarkRepository.deleteAll();
        studentResultRepository.deleteAll();
        questionRepository.deleteAll();
        examRepository.deleteAll();
        userRepository.deleteAll();

        admin = userRepository.save(new User("Admin User", "admin_sec@example.com", passwordEncoder.encode("secret123"), Role.ADMIN));
        faculty = userRepository.save(new User("Faculty User", "faculty_sec@example.com", passwordEncoder.encode("secret123"), Role.FACULTY));
        student1 = userRepository.save(new User("Student One", "student1_sec@example.com", passwordEncoder.encode("secret123"), Role.STUDENT));
        student2 = userRepository.save(new User("Student Two", "student2_sec@example.com", passwordEncoder.encode("secret123"), Role.STUDENT));

        testExam = examRepository.save(new Exam("Operating Systems", "CS302", LocalDate.now(), LocalDate.now().plusDays(10)));
        question1 = questionRepository.save(new Question(testExam, 1, "Explain Semaphore concept.", 10.0));

        student1Request = new RecheckRequest(student1, testExam, question1, "Mark calculation in question 1 seems low.");
        student1Request = recheckRequestRepository.save(student1Request);
    }

    @Test
    @DisplayName("Public routes are accessible without authentication")
    void testPublicRoutesPermitted() throws Exception {
        mockMvc.perform(get("/"))
                .andExpect(status().isOk());

        mockMvc.perform(get("/login"))
                .andExpect(status().isOk());

        mockMvc.perform(get("/403"))
                .andExpect(status().isOk());
    }

    @Test
    @DisplayName("Unauthenticated requests to protected routes redirect to login")
    void testUnauthenticatedRedirectsToLogin() throws Exception {
        mockMvc.perform(get("/student/dashboard"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrlPattern("**/login"));

        mockMvc.perform(get("/faculty/dashboard"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrlPattern("**/login"));

        mockMvc.perform(get("/admin/dashboard"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrlPattern("**/login"));
    }

    @Test
    @DisplayName("Valid credentials authenticate and redirect to role dashboard")
    void testValidLoginRedirects() throws Exception {
        mockMvc.perform(formLogin("/login").user("student1_sec@example.com").password("secret123"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/student/dashboard"));

        mockMvc.perform(formLogin("/login").user("faculty_sec@example.com").password("secret123"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/faculty/dashboard"));

        mockMvc.perform(formLogin("/login").user("admin_sec@example.com").password("secret123"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/admin/dashboard"));
    }

    @Test
    @DisplayName("Invalid credentials fail authentication")
    void testInvalidLoginFails() throws Exception {
        mockMvc.perform(formLogin("/login").user("student1_sec@example.com").password("wrongpassword"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/login?error=true"));
    }

    @Test
    @WithMockUser(username = "student1_sec@example.com", roles = {"STUDENT"})
    @DisplayName("Student can access student dashboard but is forbidden from faculty and admin areas")
    void testStudentRoleRestrictions() throws Exception {
        mockMvc.perform(get("/student/dashboard"))
                .andExpect(status().isOk());

        mockMvc.perform(get("/faculty/dashboard"))
                .andExpect(status().isForbidden());

        mockMvc.perform(get("/admin/dashboard"))
                .andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(username = "faculty_sec@example.com", roles = {"FACULTY"})
    @DisplayName("Faculty can access faculty dashboard but is forbidden from student and admin areas")
    void testFacultyRoleRestrictions() throws Exception {
        mockMvc.perform(get("/faculty/dashboard"))
                .andExpect(status().isOk());

        mockMvc.perform(get("/student/dashboard"))
                .andExpect(status().isForbidden());

        mockMvc.perform(get("/admin/dashboard"))
                .andExpect(status().isForbidden());
    }

    @Test
    @WithMockUser(username = "admin_sec@example.com", roles = {"ADMIN"})
    @DisplayName("Admin can access admin dashboard, student list, and audit logs")
    void testAdminRoleAccess() throws Exception {
        mockMvc.perform(get("/admin/dashboard"))
                .andExpect(status().isOk());

        mockMvc.perform(get("/admin/students"))
                .andExpect(status().isOk());

        mockMvc.perform(get("/admin/audit-logs"))
                .andExpect(status().isOk());
    }

    @Test
    @WithMockUser(username = "student2_sec@example.com", roles = {"STUDENT"})
    @DisplayName("Horizontal privilege escalation: Student cannot access another student's re-evaluation request")
    void testHorizontalPrivilegeEscalationPrevented() throws Exception {
        // student2 attempts to access student1's request
        mockMvc.perform(get("/student/requests/" + student1Request.getId()))
                .andExpect(status().isForbidden())
                .andExpect(view().name("error/403"));
    }
}
