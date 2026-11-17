package com.example.examreview.security;

import jakarta.servlet.ServletException;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.web.authentication.AuthenticationSuccessHandler;
import org.springframework.stereotype.Component;

import java.io.IOException;

@Component
public class RoleBasedAuthenticationSuccessHandler implements AuthenticationSuccessHandler {

    @Override
    public void onAuthenticationSuccess(HttpServletRequest request,
                                        HttpServletResponse response,
                                        Authentication authentication) throws IOException, ServletException {
        for (GrantedAuthority authority : authentication.getAuthorities()) {
            String role = authority.getAuthority();
            if ("ROLE_STUDENT".equals(role)) {
                response.sendRedirect("/student/dashboard");
                return;
            } else if ("ROLE_FACULTY".equals(role)) {
                response.sendRedirect("/faculty/dashboard");
                return;
            } else if ("ROLE_ADMIN".equals(role)) {
                response.sendRedirect("/admin/dashboard");
                return;
            }
        }
        response.sendRedirect("/");
    }
}
