package com.example.examreview.controller;

import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.GetMapping;

@Controller
public class HomeController {

    @GetMapping("/")
    public String index(Authentication authentication) {
        if (authentication != null && authentication.isAuthenticated() && !"anonymousUser".equals(authentication.getPrincipal())) {
            boolean isStudent = authentication.getAuthorities().stream().anyMatch(a -> a.getAuthority().equals("ROLE_STUDENT"));
            if (isStudent) return "redirect:/student/dashboard";

            boolean isFaculty = authentication.getAuthorities().stream().anyMatch(a -> a.getAuthority().equals("ROLE_FACULTY"));
            if (isFaculty) return "redirect:/faculty/dashboard";

            boolean isAdmin = authentication.getAuthorities().stream().anyMatch(a -> a.getAuthority().equals("ROLE_ADMIN"));
            if (isAdmin) return "redirect:/admin/dashboard";
        }
        return "index";
    }

    @GetMapping("/login")
    public String login(Authentication authentication) {
        if (authentication != null && authentication.isAuthenticated() && !"anonymousUser".equals(authentication.getPrincipal())) {
            return "redirect:/";
        }
        return "auth/login";
    }

    @GetMapping("/403")
    public String accessDenied() {
        return "error/403";
    }
}
