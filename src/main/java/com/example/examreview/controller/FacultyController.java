package com.example.examreview.controller;

import com.example.examreview.entity.*;
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

    public FacultyController(UserService userService,
                             ExamService examService,
                             RecheckRequestService recheckRequestService,
                             ReviewService reviewService,
                             MarksService marksService) {
        this.userService = userService;
        this.examService = examService;
        this.recheckRequestService = recheckRequestService;
        this.reviewService = reviewService;
        this.marksService = marksService;
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
        User faculty = userService.getCurrentUser();
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
    public String reviewRequest(@PathVariable("id") Long id, Model model, RedirectAttributes redirectAttributes) {
        Optional<RecheckRequest> requestOpt = recheckRequestService.getRequestById(id);
        if (requestOpt.isEmpty()) {
            redirectAttributes.addFlashAttribute("errorMessage", "Request not found.");
            return "redirect:/faculty/requests";
        }

        RecheckRequest request = requestOpt.get();
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
        User faculty = userService.getCurrentUser();
        try {
            reviewService.processReview(id, faculty, decision, comments, revisedMarks);
            redirectAttributes.addFlashAttribute("successMessage", "Review decision recorded successfully!");
            return "redirect:/faculty/requests/" + id;
        } catch (IllegalArgumentException | IllegalStateException ex) {
            redirectAttributes.addFlashAttribute("errorMessage", ex.getMessage());
            return "redirect:/faculty/requests/" + id;
        }
    }

    @GetMapping("/analytics")
    public String analytics(@RequestParam(value = "examId", required = false) Long examId,
                            @RequestParam(value = "threshold", defaultValue = "30") int threshold,
                            Model model) {
        List<Exam> exams = examService.getAllExams();
        Exam selectedExam = null;

        if (examId != null) {
            selectedExam = examService.getExamById(examId).orElse(null);
        } else if (!exams.isEmpty()) {
            selectedExam = exams.get(0);
        }

        List<QuestionStat> questionStats = new ArrayList<>();
        if (selectedExam != null) {
            List<Question> questions = examService.getQuestionsForExam(selectedExam.getId());
            Map<Long, Long> countsMap = recheckRequestService.getQuestionRequestCounts(selectedExam.getId());
            long totalStudents = userService.findAllStudents().size();
            long totalExamStudents = totalStudents > 0 ? totalStudents : 1; // Cohort size

            for (Question q : questions) {
                long count = countsMap.getOrDefault(q.getId(), 0L);
                double percentage = ((double) count / totalExamStudents) * 100.0;
                boolean isFlagged = percentage >= threshold;
                questionStats.add(new QuestionStat(q, count, percentage, isFlagged));
            }
        }

        model.addAttribute("exams", exams);
        model.addAttribute("selectedExam", selectedExam);
        model.addAttribute("threshold", threshold);
        model.addAttribute("stats", questionStats);

        return "faculty/analytics";
    }

    // Helper DTO for analytics view
    public static class QuestionStat {
        private final Question question;
        private final long requestCount;
        private final double percentage;
        private final boolean flagged;

        public QuestionStat(Question question, long requestCount, double percentage, boolean flagged) {
            this.question = question;
            this.requestCount = requestCount;
            this.percentage = percentage;
            this.flagged = flagged;
        }

        public Question getQuestion() { return question; }
        public long getRequestCount() { return requestCount; }
        public double getPercentage() { return percentage; }
        public boolean isFlagged() { return flagged; }
    }
}
