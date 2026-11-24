package com.example.examreview.controller;

import com.example.examreview.dto.RegisterFormDto;
import com.example.examreview.exception.ValidationException;
import com.example.examreview.service.UserService;
import jakarta.validation.Valid;
import org.springframework.security.core.Authentication;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;

@Controller
public class HomeController {

    private final UserService userService;

    public HomeController(UserService userService) {
        this.userService = userService;
    }

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

    @GetMapping("/register")
    public String register(Authentication authentication, Model model) {
        if (authentication != null && authentication.isAuthenticated() && !"anonymousUser".equals(authentication.getPrincipal())) {
            return "redirect:/";
        }
        model.addAttribute("registerForm", new RegisterFormDto());
        return "auth/register";
    }

    @PostMapping("/register")
    public String handleRegister(@Valid @ModelAttribute("registerForm") RegisterFormDto form,
                                 BindingResult bindingResult,
                                 Model model) {
        if (bindingResult.hasErrors()) {
            return "auth/register";
        }

        try {
            userService.registerStudent(form);
            return "redirect:/login?registered=true";
        } catch (ValidationException ex) {
            model.addAttribute("errorMessage", ex.getMessage());
            return "auth/register";
        }
    }

    @GetMapping("/403")
    public String accessDenied() {
        return "error/403";
    }
}
