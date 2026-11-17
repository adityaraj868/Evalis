package com.example.examreview.controller;

import com.example.examreview.entity.*;
import com.example.examreview.exception.ResourceNotFoundException;
import com.example.examreview.service.*;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.servlet.mvc.support.RedirectAttributes;

import java.time.LocalDate;
import java.time.LocalDateTime;
import java.util.*;

@Controller
@RequestMapping("/faculty")
public class FacultyController {

    private final UserService userService;
    private final ExamService examService;
    private final RecheckRequestService recheckRequestService;
    private final ReviewService reviewService;
    private final MarksService marksService;
    private final AnalyticsService analyticsService;

    public FacultyController(UserService userService,
                             ExamService examService,
                             RecheckRequestService recheckRequestService,
                             ReviewService reviewService,
                             MarksService marksService,
                             AnalyticsService analyticsService) {
        this.userService = userService;
        this.examService = examService;
        this.recheckRequestService = recheckRequestService;
        this.reviewService = reviewService;
        this.marksService = marksService;
        this.analyticsService = analyticsService;
    }

    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        List<Exam> exams = examService.getAllExams();
        List<RecheckRequest> allRequests = recheckRequestService.getAllRequests();

        long pendingRequests = allRequests.stream()
                .filter(r -> r.getStatus() == RequestStatus.SUBMITTED || r.getStatus() == RequestStatus.UNDER_REVIEW)
                .count();
        long approvedRequests = allRequests.stream()
                .filter(r -> r.getStatus() == RequestStatus.APPROVED)
                .count();
        long rejectedRequests = allRequests.stream()
                .filter(r -> r.getStatus() == RequestStatus.REJECTED)
                .count();

        model.addAttribute("exams", exams);
        model.addAttribute("recentRequests", allRequests);
        model.addAttribute("pendingCount", pendingRequests);
        model.addAttribute("approvedCount", approvedRequests);
        model.addAttribute("rejectedCount", rejectedRequests);
        model.addAttribute("activeExamsCount", exams.stream().filter(e -> e.getStatus() == ExamStatus.RE_EVALUATION_OPEN).count());

        return "faculty/dashboard";
    }

    @GetMapping("/exams")
    public String exams(Model model) {
        List<Exam> exams = examService.getAllExams();
        model.addAttribute("exams", exams);
        return "faculty/exams";
    }

    @GetMapping("/exams/new")
    public String newExamForm(Model model) {
        return "faculty/exam-new";
    }

    @PostMapping("/exams/new")
    public String createExam(@RequestParam("name") String name,
                             @RequestParam("subject") String subject,
                             @RequestParam(value = "startDate", required = false) String startDateStr,
                             @RequestParam(value = "endDate", required = false) String endDateStr,
                             @RequestParam("questionTexts") List<String> questionTexts,
                             @RequestParam("maxMarks") List<Double> maxMarksList,
                             RedirectAttributes redirectAttributes) {
        User faculty = userService.getCurrentUser();

        LocalDate startDate = (startDateStr != null && !startDateStr.isBlank()) ? LocalDate.parse(startDateStr) : LocalDate.now();
        LocalDate endDate = (endDateStr != null && !endDateStr.isBlank()) ? LocalDate.parse(endDateStr) : LocalDate.now().plusDays(14);

        Exam exam = new Exam(name, subject, startDate, endDate);
        exam.setStatus(ExamStatus.PUBLISHED);

        List<Question> questions = new ArrayList<>();
        for (int i = 0; i < questionTexts.size(); i++) {
            String text = questionTexts.get(i).trim();
            if (!text.isEmpty()) {
                Double maxM = (maxMarksList != null && maxMarksList.size() > i) ? maxMarksList.get(i) : 10.0;
                questions.add(new Question(exam, i + 1, text, maxM));
            }
        }

        examService.createExam(exam, questions, faculty);
        redirectAttributes.addFlashAttribute("successMessage", "Examination created successfully with " + questions.size() + " questions!");
        return "redirect:/faculty/exams";
    }

    @PostMapping("/exams/{id}/status")
    public String updateExamStatus(@PathVariable("id") Long examId,
                                   @RequestParam("status") ExamStatus status,
                                   RedirectAttributes redirectAttributes) {
        User faculty = userService.getRequiredCurrentUser();
        try {
            if (status == ExamStatus.RE_EVALUATION_OPEN) {
                examService.openReevaluation(examId, LocalDateTime.now(), LocalDateTime.now().plusDays(7), faculty);
                redirectAttributes.addFlashAttribute("successMessage", "Re-evaluation window is now OPEN for this exam.");
            } else if (status == ExamStatus.RE_EVALUATION_CLOSED) {
                examService.closeReevaluation(examId, faculty);
                redirectAttributes.addFlashAttribute("successMessage", "Re-evaluation window has been CLOSED.");
            } else {
                examService.updateStatus(examId, status, faculty);
                redirectAttributes.addFlashAttribute("successMessage", "Exam status updated to " + status);
            }
        } catch (Exception ex) {
            redirectAttributes.addFlashAttribute("errorMessage", ex.getMessage());
        }
        return "redirect:/faculty/exams";
    }

    @GetMapping("/exams/{id}/edit")
    public String editExamForm(@PathVariable("id") Long examId, Model model) {
        Exam exam = examService.getRequiredExamById(examId);
        List<Question> questions = examService.getQuestionsForExam(examId);
        model.addAttribute("exam", exam);
        model.addAttribute("questions", questions);
        return "faculty/exam-edit";
    }

    @PostMapping("/exams/{id}/edit")
    public String updateExam(@PathVariable("id") Long examId,
                             @RequestParam("name") String name,
                             @RequestParam("subject") String subject,
                             @RequestParam(value = "startDate", required = false) String startDateStr,
                             @RequestParam(value = "endDate", required = false) String endDateStr,
                             RedirectAttributes redirectAttributes) {
        User faculty = userService.getRequiredCurrentUser();
        try {
            LocalDate startDate = (startDateStr != null && !startDateStr.isBlank()) ? LocalDate.parse(startDateStr) : null;
            LocalDate endDate = (endDateStr != null && !endDateStr.isBlank()) ? LocalDate.parse(endDateStr) : null;
            examService.updateExam(examId, name, subject, startDate, endDate, faculty);
            redirectAttributes.addFlashAttribute("successMessage", "Examination details updated successfully!");
        } catch (Exception ex) {
            redirectAttributes.addFlashAttribute("errorMessage", ex.getMessage());
        }
        return "redirect:/faculty/exams/" + examId + "/edit";
    }

    @PostMapping("/exams/{id}/publish")
    public String publishExam(@PathVariable("id") Long examId, RedirectAttributes redirectAttributes) {
        User faculty = userService.getRequiredCurrentUser();
        try {
            examService.publishExam(examId, faculty);
            redirectAttributes.addFlashAttribute("successMessage", "Examination published successfully!");
        } catch (Exception ex) {
            redirectAttributes.addFlashAttribute("errorMessage", ex.getMessage());
        }
        return "redirect:/faculty/exams";
    }

    @PostMapping("/exams/{id}/questions")
    public String addQuestion(@PathVariable("id") Long examId,
                              @RequestParam("questionText") String questionText,
                              @RequestParam("maxMarks") Double maxMarks,
                              RedirectAttributes redirectAttributes) {
        User faculty = userService.getRequiredCurrentUser();
        try {
            examService.addQuestionToExam(examId, null, questionText, maxMarks, faculty);
            redirectAttributes.addFlashAttribute("successMessage", "Question added successfully!");
        } catch (Exception ex) {
            redirectAttributes.addFlashAttribute("errorMessage", ex.getMessage());
        }
        return "redirect:/faculty/exams/" + examId + "/edit";
    }

    @GetMapping("/exams/{id}/marks")
    public String examMarks(@PathVariable("id") Long examId, Model model) {
        Exam exam = examService.getRequiredExamById(examId);
        List<User> students = userService.findAllStudents();
        List<StudentResult> results = marksService.getExamResults(examId);

        Map<Long, StudentResult> resultsMap = new HashMap<>();
        for (StudentResult r : results) {
            resultsMap.put(r.getStudent().getId(), r);
        }

        model.addAttribute("exam", exam);
        model.addAttribute("students", students);
        model.addAttribute("resultsMap", resultsMap);

        return "faculty/exam-marks";
    }

    @GetMapping("/exams/{id}/marks/student/{studentId}")
    public String studentMarksEdit(@PathVariable("id") Long examId,
                                   @PathVariable("studentId") Long studentId,
                                   Model model) {
        Exam exam = examService.getRequiredExamById(examId);
        User student = userService.findById(studentId)
                .orElseThrow(() -> new ResourceNotFoundException("Student not found with ID: " + studentId));

        List<Question> questions = examService.getQuestionsForExam(examId);
        List<QuestionMark> marksList = marksService.getQuestionMarksForExam(studentId, examId);

        Map<Long, Double> currentMarksMap = new HashMap<>();
        for (QuestionMark qm : marksList) {
            currentMarksMap.put(qm.getQuestion().getId(), qm.getMarksObtained());
        }

        model.addAttribute("exam", exam);
        model.addAttribute("student", student);
        model.addAttribute("questions", questions);
        model.addAttribute("currentMarksMap", currentMarksMap);

        return "faculty/student-marks-edit";
    }

    @PostMapping("/exams/{id}/marks/student/{studentId}")
    public String saveStudentMarks(@PathVariable("id") Long examId,
                                   @PathVariable("studentId") Long studentId,
                                   @RequestParam Map<String, String> allParams,
                                   RedirectAttributes redirectAttributes) {
        User faculty = userService.getRequiredCurrentUser();
        try {
            Map<Long, Double> questionMarks = new HashMap<>();
            for (Map.Entry<String, String> entry : allParams.entrySet()) {
                String key = entry.getKey();
                if (key.startsWith("questionMarks[") && key.endsWith("]")) {
                    String qIdStr = key.substring("questionMarks[".length(), key.length() - 1);
                    Long qId = Long.parseLong(qIdStr);
                    Double mark = Double.parseDouble(entry.getValue());
                    questionMarks.put(qId, mark);
                }
            }

            marksService.recordExamMarksForStudent(examId, studentId, questionMarks, faculty);
            redirectAttributes.addFlashAttribute("successMessage", "Student marks updated successfully!");
        } catch (Exception ex) {
            redirectAttributes.addFlashAttribute("errorMessage", ex.getMessage());
        }
        return "redirect:/faculty/exams/" + examId + "/marks";
    }

    @GetMapping("/requests")
    public String requests(@RequestParam(value = "examId", required = false) Long examId,
                           Model model) {
        List<Exam> exams = examService.getAllExams();
        List<RecheckRequest> requests;

        if (examId != null) {
            requests = recheckRequestService.getExamRequests(examId);
        } else {
            requests = recheckRequestService.getAllRequests();
        }

        model.addAttribute("exams", exams);
        model.addAttribute("selectedExamId", examId);
        model.addAttribute("requests", requests);

        return "faculty/requests";
    }

    @GetMapping("/requests/{id}")
    public String reviewRequest(@PathVariable("id") Long id, Model model) {
        User faculty = userService.getRequiredCurrentUser();
        RecheckRequest request = recheckRequestService.getRequestById(id)
                .orElseThrow(() -> new ResourceNotFoundException("Request not found with ID: " + id));

        // Automatically transition SUBMITTED to UNDER_REVIEW upon faculty opening
        if (request.getStatus() == RequestStatus.SUBMITTED) {
            request = recheckRequestService.markUnderReview(id, faculty);
        }

        Optional<QuestionMark> markOpt = marksService.getQuestionMark(request.getStudent().getId(), request.getQuestion().getId());

        model.addAttribute("req", request);
        model.addAttribute("currentMark", markOpt.map(QuestionMark::getMarksObtained).orElse(0.0));
        model.addAttribute("reviews", reviewService.getReviewsForRequest(id));

        return "faculty/request-review";
    }

    @PostMapping("/requests/{id}/review")
    public String submitReview(@PathVariable("id") Long id,
                               @RequestParam("decision") ReviewDecision decision,
                               @RequestParam(value = "revisedMarks", required = false) Double revisedMarks,
                               @RequestParam(value = "comments", required = false) String comments,
                               RedirectAttributes redirectAttributes) {
        User faculty = userService.getRequiredCurrentUser();
        try {
            reviewService.processReview(id, faculty, decision, comments, revisedMarks);
            redirectAttributes.addFlashAttribute("successMessage", "Review decision recorded successfully!");
            return "redirect:/faculty/requests/" + id;
        } catch (RuntimeException ex) {
            redirectAttributes.addFlashAttribute("errorMessage", ex.getMessage());
            return "redirect:/faculty/requests/" + id;
        }
    }

    @GetMapping("/analytics")
    public String analytics(@RequestParam(value = "examId", required = false) Long examId,
                            @RequestParam(value = "threshold", defaultValue = "30") int threshold,
                            Model model) {
        User faculty = userService.getRequiredCurrentUser();
        List<Exam> exams = examService.getAllExams();
        Exam selectedExam = null;

        if (examId != null) {
            selectedExam = examService.getExamById(examId).orElse(null);
        } else if (!exams.isEmpty()) {
            selectedExam = exams.get(0);
        }

        List<com.example.examreview.dto.QuestionAnalyticsDto> questionStats = new ArrayList<>();
        if (selectedExam != null) {
            com.example.examreview.dto.ExamAnalyticsDto analyticsDto = analyticsService.getExamAnalytics(selectedExam.getId(), threshold, faculty);
            questionStats = analyticsDto.getQuestionStats();
        }

        model.addAttribute("exams", exams);
        model.addAttribute("selectedExam", selectedExam);
        model.addAttribute("threshold", threshold);
        model.addAttribute("stats", questionStats);

        return "faculty/analytics";
    }
}
