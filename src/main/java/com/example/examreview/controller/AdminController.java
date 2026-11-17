package com.example.examreview.controller;

import com.example.examreview.entity.AuditLog;
import com.example.examreview.entity.User;
import com.example.examreview.service.AuditService;
import com.example.examreview.service.ExamService;
import com.example.examreview.service.RecheckRequestService;
import com.example.examreview.service.UserService;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;

@Controller
@RequestMapping("/admin")
public class AdminController {

    private final UserService userService;
    private final ExamService examService;
    private final RecheckRequestService recheckRequestService;
    private final AuditService auditService;

    public AdminController(UserService userService,
                           ExamService examService,
                           RecheckRequestService recheckRequestService,
                           AuditService auditService) {
        this.userService = userService;
        this.examService = examService;
        this.recheckRequestService = recheckRequestService;
        this.auditService = auditService;
    }

    @GetMapping("/dashboard")
    public String dashboard(Model model) {
        List<User> students = userService.findAllStudents();
        List<User> faculty = userService.findAllFaculty();
        long examCount = examService.getAllExams().size();
        long requestCount = recheckRequestService.getAllRequests().size();
        List<AuditLog> recentLogs = auditService.getAllLogs();

        model.addAttribute("studentCount", students.size());
        model.addAttribute("facultyCount", faculty.size());
        model.addAttribute("examCount", examCount);
        model.addAttribute("requestCount", requestCount);
        model.addAttribute("recentLogs", recentLogs.stream().limit(8).toList());

        return "admin/dashboard";
    }

    @GetMapping("/students")
    public String students(Model model) {
        List<User> students = userService.findAllStudents();
        model.addAttribute("students", students);
        return "admin/students";
    }

    @GetMapping("/audit-logs")
    public String auditLogs(@RequestParam(value = "action", required = false) String action,
                            @RequestParam(value = "resourceType", required = false) String resourceType,
                            @RequestParam(value = "userId", required = false) Long userId,
                            Model model) {
        List<AuditLog> logs = auditService.filterLogs(action, resourceType, userId);
        model.addAttribute("logs", logs);
        model.addAttribute("selectedAction", action);
        model.addAttribute("selectedResource", resourceType);
        model.addAttribute("selectedUserId", userId);
        model.addAttribute("users", userService.findAllUsers());
        return "admin/audit-logs";
    }
}
