package com.example.examreview.controller;

import com.example.examreview.entity.*;
import com.example.examreview.exception.ResourceNotFoundException;
import com.example.examreview.exception.UnauthorizedAccessException;
import com.example.examreview.service.ExamService;
import com.example.examreview.service.MarksService;
import com.example.examreview.service.RecheckRequestService;
import com.example.examreview.service.UserService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.util.*;

@Controller
@RequestMapping("/student")
public class StudentController {

    private final UserService userService;
    private final ExamService examService;
    private final MarksService marksService;
    private final RecheckRequestService recheckRequestService;

    public StudentController(UserService userService,
                             ExamService examService,
                             MarksService marksService,
                             RecheckRequestService recheckRequestService) {
        this.userService = userService;
        this.examService = examService;
        this.marksService = marksService;
        this.recheckRequestService = recheckRequestService;
    }

    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        User student = userService.getRequiredCurrentUser();
        List<StudentResult> results = marksService.getStudentResults(student.getId());
        List<RecheckRequest> requests = recheckRequestService.getStudentRequests(student.getId());

        model.addAttribute("student", student);
        model.addAttribute("results", results);
        model.addAttribute("requests", requests);
        model.addAttribute("pendingCount", requests.stream().filter(r -> r.getStatus() == RequestStatus.SUBMITTED || r.getStatus() == RequestStatus.UNDER_REVIEW).count());
        model.addAttribute("approvedCount", requests.stream().filter(r -> r.getStatus() == RequestStatus.APPROVED).count());
        model.addAttribute("rejectedCount", requests.stream().filter(r -> r.getStatus() == RequestStatus.REJECTED).count());

        return "student/dashboard";
    }

    @GetMapping("/exams")
    public String exams(Model model) {
        User student = userService.getRequiredCurrentUser();
        List<StudentResult> results = marksService.getStudentResults(student.getId());
        model.addAttribute("results", results);
        return "student/exams";
    }

    @GetMapping("/exams/{id}")
    public String examDetail(@PathVariable("id") Long examId, Model model, RedirectAttributes redirectAttributes) {
        User student = userService.getRequiredCurrentUser();
        Optional<Exam> examOpt = examService.getExamById(examId);
        if (examOpt.isEmpty()) {
            throw new ResourceNotFoundException("Examination not found with ID: " + examId);
        }
        Exam exam = examOpt.get();

        Optional<StudentResult> resultOpt = marksService.getStudentResult(student.getId(), examId);
        if (resultOpt.isEmpty()) {
            throw new UnauthorizedAccessException("You are not enrolled or have no marks record for this examination.");
        }

        List<Question> questions = examService.getQuestionsForExam(examId);
        List<QuestionMark> marksList = marksService.getQuestionMarksForExam(student.getId(), examId);

        Map<Long, Double> questionMarksMap = new HashMap<>();
        for (QuestionMark qm : marksList) {
            questionMarksMap.put(qm.getQuestion().getId(), qm.getMarksObtained());
        }

        // Map which questions already have a recheck request
        Map<Long, Boolean> existingRequestsMap = new HashMap<>();
        for (Question q : questions) {
            existingRequestsMap.put(q.getId(), recheckRequestService.hasExistingRequest(student.getId(), examId, q.getId()));
        }

        model.addAttribute("exam", exam);
        model.addAttribute("result", resultOpt.get());
        model.addAttribute("questions", questions);
        model.addAttribute("questionMarksMap", questionMarksMap);
        model.addAttribute("existingRequestsMap", existingRequestsMap);
        model.addAttribute("isReevalOpen", exam.getStatus() == ExamStatus.RE_EVALUATION_OPEN);

        return "student/exam-detail";
    }

    @GetMapping("/requests/new")
    public String newRequestForm(@RequestParam("examId") Long examId,
                                 @RequestParam("questionId") Long questionId,
                                 Model model,
                                 RedirectAttributes redirectAttributes) {
        User student = userService.getRequiredCurrentUser();

        Optional<Exam> examOpt = examService.getExamById(examId);
        Optional<Question> questionOpt = examService.getQuestionById(questionId);

        if (examOpt.isEmpty() || questionOpt.isEmpty()) {
            throw new ResourceNotFoundException("Invalid exam or question selected.");
        }

        Exam exam = examOpt.get();
        Question question = questionOpt.get();

        if (recheckRequestService.hasExistingRequest(student.getId(), examId, questionId)) {
            redirectAttributes.addFlashAttribute("errorMessage", "A re-evaluation request already exists for this question.");
            return "redirect:/student/exams/" + examId;
        }

        Optional<QuestionMark> markOpt = marksService.getQuestionMark(student.getId(), questionId);

        model.addAttribute("exam", exam);
        model.addAttribute("question", question);
        model.addAttribute("currentMark", markOpt.map(QuestionMark::getMarksObtained).orElse(0.0));

        return "student/request-form";
    }

    @PostMapping("/requests")
    public String submitRequest(@RequestParam("examId") Long examId,
                                @RequestParam("questionId") Long questionId,
                                @RequestParam("reason") String reason,
                                RedirectAttributes redirectAttributes) {
        User student = userService.getRequiredCurrentUser();
        try {
            RecheckRequest request = recheckRequestService.submitRequest(student, examId, questionId, reason);
            redirectAttributes.addFlashAttribute("successMessage", "Re-evaluation request submitted successfully!");
            return "redirect:/student/requests/" + request.getId();
        } catch (RuntimeException ex) {
            redirectAttributes.addFlashAttribute("errorMessage", ex.getMessage());
            return "redirect:/student/exams/" + examId;
        }
    }

    @GetMapping("/requests")
    public String requests(Model model) {
        User student = userService.getRequiredCurrentUser();
        List<RecheckRequest> requests = recheckRequestService.getStudentRequests(student.getId());
        model.addAttribute("requests", requests);
        return "student/requests";
    }

    @GetMapping("/requests/{id}")
    public String requestDetail(@PathVariable("id") Long id, Model model) {
        User student = userService.getRequiredCurrentUser();
        Optional<RecheckRequest> requestOpt = recheckRequestService.getRequestById(id);

        if (requestOpt.isEmpty()) {
            throw new ResourceNotFoundException("Re-evaluation request not found with ID: " + id);
        }

        RecheckRequest request = requestOpt.get();
        if (!request.getStudent().getId().equals(student.getId())) {
            throw new UnauthorizedAccessException("You are not authorized to view another student's re-evaluation request.");
        }

        Optional<QuestionMark> markOpt = marksService.getQuestionMark(student.getId(), request.getQuestion().getId());

        model.addAttribute("req", request);
        model.addAttribute("currentMark", markOpt.map(QuestionMark::getMarksObtained).orElse(0.0));
        model.addAttribute("reviews", request.getReviews());

        return "student/request-detail";
    }
}
