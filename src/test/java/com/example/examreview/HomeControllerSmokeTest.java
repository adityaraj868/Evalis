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
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.content;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

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
}
