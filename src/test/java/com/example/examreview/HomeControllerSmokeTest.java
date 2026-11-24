package com.example.examreview;

import com.example.examreview.entity.Role;
import com.example.examreview.entity.User;
import com.example.examreview.repository.UserRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.security.test.context.support.WithMockUser;
import org.springframework.test.context.ActiveProfiles;
import org.springframework.test.web.servlet.MockMvc;

import static org.hamcrest.Matchers.containsString;
import static org.springframework.security.test.web.servlet.request.SecurityMockMvcRequestPostProcessors.csrf;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.*;

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
class HomeControllerSmokeTest {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UserRepository userRepository;

    @BeforeEach
    void setUp() {
        if (userRepository.findByEmail("student@example.com").isEmpty()) {
            User student = new User("John Student", "student@example.com", "pass", Role.STUDENT);
            userRepository.save(student);
        }
    }

    @Test
    void testLandingPageRendersSuccessfully() throws Exception {
        mockMvc.perform(get("/"))
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("Exam Question Re-evaluation Portal")));
    }

    @Test
    @WithMockUser(username = "student@example.com", roles = {"STUDENT"})
    void testStudentDashboardRendersSuccessfully() throws Exception {
        mockMvc.perform(get("/student/dashboard"))
                .andExpect(status().isOk());
    }

    @Autowired
    private com.example.examreview.repository.ExamRepository examRepository;

    @Autowired
    private com.example.examreview.repository.QuestionRepository questionRepository;

    @Autowired
    private com.example.examreview.repository.StudentResultRepository studentResultRepository;

    @Autowired
    private com.example.examreview.repository.RecheckRequestRepository recheckRequestRepository;

    @Test
    @WithMockUser(username = "student@example.com", roles = {"STUDENT"})
    void testStudentDashboardWithDataRendersSuccessfully() throws Exception {
        User student = userRepository.findByEmail("student@example.com").orElseThrow();
        com.example.examreview.entity.Exam exam = new com.example.examreview.entity.Exam("Midterm", "CS", java.time.LocalDate.now(), java.time.LocalDate.now());
        examRepository.save(exam);

        com.example.examreview.entity.Question question = new com.example.examreview.entity.Question(exam, 1, "Desc", 10.0);
        questionRepository.save(question);

        com.example.examreview.entity.StudentResult result = new com.example.examreview.entity.StudentResult(student, exam, 8.0);
        studentResultRepository.save(result);

        com.example.examreview.entity.RecheckRequest request = new com.example.examreview.entity.RecheckRequest(student, exam, question, "Reason");
        recheckRequestRepository.save(request);

        mockMvc.perform(get("/student/dashboard"))
                .andExpect(status().isOk());
    }

    @Test
    @WithMockUser(username = "faculty@example.com", roles = {"FACULTY"})
    void testFacultyReviewPageRendersSuccessfully() throws Exception {
        User faculty = userRepository.findByEmail("faculty@example.com").orElseGet(() -> {
            User f = new User("Jane Faculty", "faculty@example.com", "pass", Role.FACULTY);
            return userRepository.save(f);
        });
        User student = userRepository.findByEmail("student@example.com").orElseThrow();
        com.example.examreview.entity.Exam exam = new com.example.examreview.entity.Exam("Midterm 2", "CS", java.time.LocalDate.now(), java.time.LocalDate.now());
        examRepository.save(exam);

        com.example.examreview.entity.Question question = new com.example.examreview.entity.Question(exam, 1, "Desc", 10.0);
        questionRepository.save(question);

        com.example.examreview.entity.RecheckRequest request = new com.example.examreview.entity.RecheckRequest(student, exam, question, "Reason");
        recheckRequestRepository.save(request);

        mockMvc.perform(get("/faculty/requests/" + request.getId()))
                .andExpect(status().isOk());
    }

    @Test
    void testRegisterPageRendersSuccessfully() throws Exception {
        mockMvc.perform(get("/register"))
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("Create Account")));
    }

    @Test
    void testSuccessfulStudentRegistration() throws Exception {
        String newEmail = "newstudent_" + System.currentTimeMillis() + "@example.com";
        mockMvc.perform(post("/register")
                        .with(csrf())
                        .param("name", "New Student")
                        .param("email", newEmail)
                        .param("password", "secure123")
                        .param("confirmPassword", "secure123"))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/login?registered=true"));
    }

    @Test
    void testDuplicateEmailRegistrationFails() throws Exception {
        mockMvc.perform(post("/register")
                        .with(csrf())
                        .param("name", "Duplicate Person")
                        .param("email", "student@example.com")
                        .param("password", "secure123")
                        .param("confirmPassword", "secure123"))
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("already exists")));
    }

    @Test
    void testPasswordMismatchRegistrationFails() throws Exception {
        mockMvc.perform(post("/register")
                        .with(csrf())
                        .param("name", "Mismatch Student")
                        .param("email", "mismatch@example.com")
                        .param("password", "secure123")
                        .param("confirmPassword", "differentpass"))
                .andExpect(status().isOk())
                .andExpect(content().string(containsString("do not match")));
    }
}
