import zipfile
import html
import os
import shutil

TEMPLATE_PATH = '/home/epsilon/clg/Enterprise/report_for_sub/Java Project Report Format.docx'
OUTPUT_DOCX = '/home/epsilon/clg/Enterprise/report_for_sub/Exam_Review_System_Project_Report.docx'
OUTPUT_MD = '/home/epsilon/clg/Enterprise/report_for_sub/PROJECT_REPORT.md'

def esc(text):
    return html.escape(str(text))

def para(text="", bold=False, italic=False, size=24, align="both", before=60, after=60, color=None):
    b_tag = "<w:b/>" if bold else ""
    i_tag = "<w:i/>" if italic else ""
    c_tag = f'<w:color w:val="{color}"/>' if color else ""
    jc_tag = f'<w:jc w:val="{align}"/>' if align else ""
    
    return f"""<w:p>
  <w:pPr>
    <w:spacing w:before="{before}" w:after="{after}" w:line="276" w:lineRule="auto"/>
    {jc_tag}
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      {b_tag}
      {i_tag}
      {c_tag}
      <w:sz w:val="{size}"/>
      <w:szCs w:val="{size}"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      {b_tag}
      {i_tag}
      {c_tag}
      <w:sz w:val="{size}"/>
      <w:szCs w:val="{size}"/>
    </w:rPr>
    <w:t xml:space="preserve">{esc(text)}</w:t>
  </w:r>
</w:p>"""

def heading1(text):
    return f"""<w:p>
  <w:pPr>
    <w:pStyle w:val="Heading1"/>
    <w:spacing w:before="360" w:after="160"/>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:b/>
      <w:color w:val="1A365D"/>
      <w:sz w:val="34"/>
      <w:szCs w:val="34"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:b/>
      <w:color w:val="1A365D"/>
      <w:sz w:val="34"/>
      <w:szCs w:val="34"/>
    </w:rPr>
    <w:t>{esc(text)}</w:t>
  </w:r>
</w:p>"""

def heading2(text):
    return f"""<w:p>
  <w:pPr>
    <w:pStyle w:val="Heading2"/>
    <w:spacing w:before="260" w:after="120"/>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:b/>
      <w:color w:val="2B6CB0"/>
      <w:sz w:val="28"/>
      <w:szCs w:val="28"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:b/>
      <w:color w:val="2B6CB0"/>
      <w:sz w:val="28"/>
      <w:szCs w:val="28"/>
    </w:rPr>
    <w:t>{esc(text)}</w:t>
  </w:r>
</w:p>"""

def heading3(text):
    return f"""<w:p>
  <w:pPr>
    <w:pStyle w:val="Heading3"/>
    <w:spacing w:before="180" w:after="80"/>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:b/>
      <w:color w:val="2D3748"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:b/>
      <w:color w:val="2D3748"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
    <w:t>{esc(text)}</w:t>
  </w:r>
</w:p>"""

def bullet(bold_prefix, text):
    return f"""<w:p>
  <w:pPr>
    <w:spacing w:before="40" w:after="40" w:line="276" w:lineRule="auto"/>
    <w:ind w:left="720" w:hanging="360"/>
    <w:jc w:val="both"/>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Symbol" w:hAnsi="Symbol"/>
      <w:sz w:val="20"/>
    </w:rPr>
    <w:t xml:space="preserve">&#183;  </w:t>
  </w:r>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:b/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
    <w:t xml:space="preserve">{esc(bold_prefix)}: </w:t>
  </w:r>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
    <w:t xml:space="preserve">{esc(text)}</w:t>
  </w:r>
</w:p>"""

def placeholder_box(fig_number, title, what_to_paste, where_from):
    return f"""<w:tbl>
  <w:tblPr>
    <w:tblW w:w="9200" w:type="dxa"/>
    <w:jc w:val="center"/>
    <w:tblBorders>
      <w:top w:val="single" w:sz="12" w:space="0" w:color="2B6CB0"/>
      <w:left w:val="single" w:sz="12" w:space="0" w:color="2B6CB0"/>
      <w:bottom w:val="single" w:sz="12" w:space="0" w:color="2B6CB0"/>
      <w:right w:val="single" w:sz="12" w:space="0" w:color="2B6CB0"/>
      <w:insideH w:val="none"/>
      <w:insideV w:val="none"/>
    </w:tblBorders>
    <w:tblCellMar>
      <w:top w:w="160" w:type="dxa"/>
      <w:left w:w="240" w:type="dxa"/>
      <w:bottom w:w="160" w:type="dxa"/>
      <w:right w:w="240" w:type="dxa"/>
    </w:tblCellMar>
  </w:tblPr>
  <w:tr>
    <w:tc>
      <w:tcPr>
        <w:tcW w:w="9200" w:type="dxa"/>
        <w:shd w:val="clear" w:color="auto" w:fill="EDF2F7"/>
      </w:tcPr>
      <w:p>
        <w:pPr>
          <w:jc w:val="center"/>
          <w:spacing w:before="120" w:after="80"/>
        </w:pPr>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
            <w:b/>
            <w:color w:val="2B6CB0"/>
            <w:sz w:val="24"/>
          </w:rPr>
          <w:t>[IMAGE PLACEHOLDER - {esc(fig_number)}: {esc(title)}]</w:t>
        </w:r>
      </w:p>
      <w:p>
        <w:pPr>
          <w:jc w:val="left"/>
          <w:spacing w:before="40" w:after="40"/>
        </w:pPr>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
            <w:b/>
            <w:sz w:val="20"/>
          </w:rPr>
          <w:t xml:space="preserve">What to paste: </w:t>
        </w:r>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
            <w:sz w:val="20"/>
          </w:rPr>
          <w:t>{esc(what_to_paste)}</w:t>
        </w:r>
      </w:p>
      <w:p>
        <w:pPr>
          <w:jc w:val="left"/>
          <w:spacing w:before="40" w:after="120"/>
        </w:pPr>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
            <w:b/>
            <w:sz w:val="20"/>
          </w:rPr>
          <w:t xml:space="preserve">Source / Web URL: </w:t>
        </w:r>
        <w:r>
          <w:rPr>
            <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
            <w:color w:val="2C5282"/>
            <w:i/>
            <w:sz w:val="20"/>
          </w:rPr>
          <w:t>{esc(where_from)}</w:t>
        </w:r>
      </w:p>
    </w:tc>
  </w:tr>
</w:tbl>
<w:p><w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="160"/></w:pPr>
  <w:r><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/><w:i/><w:sz w:val="20"/><w:color w:val="4A5568"/></w:rPr>
  <w:t>Figure {esc(fig_number)}: {esc(title)}</w:t></w:r>
</w:p>"""

def code_block(code_str):
    lines = code_str.strip().split("\n")
    p_tags = []
    for line in lines:
        p_tags.append(f"""<w:p>
  <w:pPr>
    <w:spacing w:before="10" w:after="10" w:line="240" w:lineRule="auto"/>
    <w:ind w:left="360" w:right="360"/>
    <w:shd w:val="clear" w:color="auto" w:fill="F7FAFC"/>
    <w:rPr>
      <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>
      <w:sz w:val="18"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/>
      <w:color w:val="2D3748"/>
      <w:sz w:val="18"/>
    </w:rPr>
    <w:t xml:space="preserve">{esc(line)}</w:t>
  </w:r>
</w:p>""")
    return "\n".join(p_tags)

def table(headers, rows, widths=None):
    if not widths:
        w_val = 9200 // len(headers)
        widths = [w_val] * len(headers)
    
    xml = ["""<w:tbl>
  <w:tblPr>
    <w:tblW w:w="9200" w:type="dxa"/>
    <w:jc w:val="center"/>
    <w:tblBorders>
      <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E0"/>
      <w:left w:val="single" w:sz="6" w:space="0" w:color="CBD5E0"/>
      <w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E0"/>
      <w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E0"/>
      <w:insideH w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
      <w:insideV w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
    </w:tblBorders>
    <w:tblCellMar>
      <w:top w:w="120" w:type="dxa"/>
      <w:left w:w="160" w:type="dxa"/>
      <w:bottom w:w="120" w:type="dxa"/>
      <w:right w:w="160" w:type="dxa"/>
    </w:tblCellMar>
  </w:tblPr>"""]
    
    # Header row
    xml.append("<w:tr><w:trPr><w:tblHeader/></w:trPr>")
    for idx, h in enumerate(headers):
        xml.append(f"""<w:tc>
  <w:tcPr>
    <w:tcW w:w="{widths[idx]}" w:type="dxa"/>
    <w:shd w:val="clear" w:color="auto" w:fill="2B6CB0"/>
  </w:tcPr>
  <w:p>
    <w:pPr><w:jc w:val="center"/><w:spacing w:before="60" w:after="60"/></w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:b/>
        <w:color w:val="FFFFFF"/>
        <w:sz w:val="20"/>
      </w:rPr>
      <w:t>{esc(h)}</w:t>
    </w:r>
  </w:p>
</w:tc>""")
    xml.append("</w:tr>")
    
    # Body rows
    for r_idx, row in enumerate(rows):
        bg = "FFFFFF" if r_idx % 2 == 0 else "F7FAFC"
        xml.append("<w:tr>")
        for idx, cell in enumerate(row):
            xml.append(f"""<w:tc>
  <w:tcPr>
    <w:tcW w:w="{widths[idx]}" w:type="dxa"/>
    <w:shd w:val="clear" w:color="auto" w:fill="{bg}"/>
  </w:tcPr>
  <w:p>
    <w:pPr><w:spacing w:before="40" w:after="40"/></w:pPr>
    <w:r>
      <w:rPr>
        <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
        <w:sz w:val="20"/>
      </w:rPr>
      <w:t>{esc(cell)}</w:t>
    </w:r>
  </w:p>
</w:tc>""")
        xml.append("</w:tr>")
    
    xml.append('</w:tbl><w:p><w:pPr><w:spacing w:before="60" w:after="120"/></w:pPr></w:p>')
    return "\n".join(xml)

def page_break():
    return '<w:p><w:r><w:br w:type="page"/></w:r></w:p>'

def build_report_content():
    c = []
    
    # ABSTRACT
    c.append(page_break())
    c.append(heading1("Abstract"))
    c.append(para("In modern higher education institutions, the traditional examination re-evaluation process is predominantly paper-based, cumbersome, and inherently opaque. Students are frequently mandated to apply for an entire examination re-check rather than querying specific disputed evaluation criteria or questions. Consequently, evaluators endure severe repetitive manual workloads, administrative staff face logistics overheads, and students remain uninformed regarding the exact progress and rationale of their re-evaluation requests. Furthermore, institutions miss critical systemic insights—such as recurring evaluation discrepancies or inherently flawed examination questions that trigger disproportionate dispute volumes."))
    c.append(para("This project presents the Exam Question Re-evaluation and Review Management System, an enterprise-grade, web-based software application engineered to modernize and streamline the academic re-evaluation lifecycle. Developed using Java 21, Spring Boot 3.4.3, Spring Security 6, Spring Data JPA, Hibernate ORM, and Thymeleaf, the system delivers a secure, role-segregated environment for Students, Faculty, and Administrators. Students can inspect granular question-level scores, submit targeted re-evaluation claims with technical justifications within active submission windows, and monitor real-time decision transitions. Concurrency controls and database-level unique constraints strictly eliminate duplicate submissions. Faculty evaluators access a dedicated workspace to inspect disputes grouped by question, verify original student marks against question limits, record amended scores, and input official review remarks. System administrators maintain governance via a tamper-proof audit trail capturing all critical assessment events."))
    c.append(para("By replacing subjective, opaque paperwork with a transparent, role-governed, and data-driven digital workflow, the platform significantly accelerates dispute turnaround, enforces academic integrity, and equips institutional departments with question-level analytics for curriculum enhancement."))

    # TABLE OF CONTENTS
    c.append(page_break())
    c.append(heading1("Table of Contents"))
    toc_headers = ["S. No.", "Chapter / Section Name", "Page No."]
    toc_rows = [
        ["1", "Cover Page", "1"],
        ["2", "Abstract", "2"],
        ["3", "Table of Contents", "3"],
        ["4", "Chapter 1: Introduction", "4"],
        ["", "1.1 Introduction to the Project", "4"],
        ["", "1.2 Problem Statement", "5"],
        ["", "1.3 Objectives of the Project", "5"],
        ["", "1.4 Scope of the Project", "6"],
        ["5", "Chapter 2: System Design", "7"],
        ["", "2.1 System Architecture", "7"],
        ["", "2.2 Use Case Diagram", "9"],
        ["", "2.3 Class Diagram", "11"],
        ["", "2.4 Activity Diagram", "13"],
        ["", "2.5 Database Design / ER Diagram", "15"],
        ["", "2.6 Module Description", "18"],
        ["6", "Chapter 3: Implementation", "21"],
        ["", "3.1 Technologies and Tools Used", "21"],
        ["", "3.2 Project Structure / Package Structure", "22"],
        ["", "3.3 Description of Classes and Interfaces", "24"],
        ["", "3.4 Implementation of Major Modules", "27"],
        ["", "3.5 Exception Handling", "29"],
        ["", "3.6 Collection Framework Usage", "31"],
        ["", "3.7 Database Connectivity", "32"],
        ["", "3.8 Important Code Snippets", "33"],
        ["7", "Chapter 4: Results and Screenshots", "37"],
        ["", "4.1 Main Application Screen", "37"],
        ["", "4.2 Functional Screenshots", "38"],
        ["", "4.3 Input and Output Demonstrations", "44"],
        ["", "4.4 Error Handling Demonstrations", "46"],
        ["8", "References", "48"]
    ]
    c.append(table(toc_headers, toc_rows, [1200, 6800, 1200]))

    # CHAPTER 1: INTRODUCTION
    c.append(page_break())
    c.append(heading1("Chapter 1: Introduction"))
    
    c.append(heading2("1.1 Introduction to the Project"))
    c.append(para("Assessment and evaluation represent the cornerstone of academic measurement in higher education. At the conclusion of semester examinations, institutional examination cells publish final mark sheets and provide a window for students dissatisfied with their awarded marks to request re-evaluation or paper re-checking. In traditional university setups, this process is governed through physical forms, bank challans, manual paper retrieval from archives, and ad-hoc reassignment to faculty evaluators. This conventional process suffers from substantial friction, extreme latency, and lack of accountability."))
    c.append(para("The Exam Question Re-evaluation and Review Management System is an enterprise software solution designed to transition academic dispute resolution into the modern digital era. Implemented on top of the robust Spring Boot framework, the application organizes the examination lifecycle into clear, structured stages: examination scheduling, question-wise marks entry, controlled re-evaluation window opening, granular question-level dispute lodging, faculty review workflows, and automated grade recalculations."))
    c.append(para("Unlike legacy systems that treat an exam paper as a monolithic entity, our platform treats each question as a distinct evaluation unit. This empowers students to pinpoint exact discrepancies while giving educators focused worklists and aggregate analytics on evaluation consistency."))

    c.append(heading2("1.2 Problem Statement"))
    c.append(para("The traditional examination re-evaluation process across academic institutions exhibits several fundamental vulnerabilities:"))
    c.append(bullet("Lack of Evaluation Granularity", "Students are forced to pay for and request re-evaluation of an entire subject, even when their dispute concerns a single question's marking criteria. This creates wasteful overhead for both students and evaluators."))
    c.append(bullet("Operational Opacity", "Once a physical re-evaluation form is submitted, students have no visibility into the workflow. They cannot determine whether the paper has been retrieved, who is reviewing it, or why marks were maintained or amended."))
    c.append(bullet("Concurrency & Duplicate Lodging Vulnerabilities", "Physical or naive web forms frequently allow duplicate submissions for the same question or examination, causing conflicting reviews and corrupted academic records."))
    c.append(bullet("High Administrative Latency", "Physical transit of examination answer scripts between administrative vaults and evaluators takes weeks, delaying final semester grade card publication."))
    c.append(bullet("Absence of Diagnostic Feedback", "Conventional systems fail to provide institutional leadership with aggregate metrics. If 70% of an entire student cohort files re-evaluations for a single question due to an ambiguous problem statement or key error, the department remains blind to the anomaly."))

    c.append(heading2("1.3 Objectives of the Project"))
    c.append(para("The primary engineering objectives of this enterprise project are:"))
    c.append(bullet("Role-Based Security & Governance", "Implement strict role-based access control (RBAC) separating Student, Faculty, and Administrator capabilities using Spring Security 6 and BCrypt password hashing."))
    c.append(bullet("Granular Dispute Management", "Enable students to inspect individual question marks against maximum score ceilings and file targeted re-evaluation claims with technical reasoning."))
    c.append(bullet("Concurrency & Duplicate Prevention", "Enforce multi-layered duplicate submission guards through service validation and database unique constraints (ADR-003: UNIQUE(student_id, exam_id, question_id))."))
    c.append(bullet("Structured Faculty Review Pipeline", "Provide faculty members with a centralized review inbox, dispute reasoning analysis, mark revision controls, and formal remark logging."))
    c.append(bullet("Real-Time Status Tracking", "Deliver end-to-end lifecycle tracking (SUBMITTED -> UNDER_REVIEW -> APPROVED / REJECTED -> COMPLETED) for students."))
    c.append(bullet("Educational Analytics", "Provide faculty with question-level dispute frequency aggregations to flag pedagogical and exam design anomalies."))
    c.append(bullet("Traceable Audit Trail", "Maintain an immutable, timestamped audit log of all administrative actions, exam publications, and grade alterations."))

    c.append(heading2("1.4 Scope of the Project"))
    c.append(para("The operational boundary of the project is structured as follows:"))
    c.append(bullet("In-Scope Functional Features", "User authentication, student question-wise marks breakdown, re-evaluation window enforcement, dispute filing, duplicate request rejection, faculty review decisioning, automated mark rollups, dispute analytics, and audit logging."))
    c.append(bullet("Optional / Advanced Features", "Automated question dispute threshold alerts, email notification hooks, and supporting document attachments."))
    c.append(bullet("Out-of-Scope Boundaries", "Conducting online computer-based examinations, automated AI auto-grading of subjective answers, optical character recognition (OCR) of handwritten answer sheets, and payment gateway banking integrations."))

    # CHAPTER 2: SYSTEM DESIGN
    c.append(page_break())
    c.append(heading1("Chapter 2: System Design"))

    c.append(heading2("2.1 System Architecture"))
    c.append(para("The Exam Review System is designed adhering to the Modular Monolith pattern (ADR-001) using a standard enterprise multi-tier architecture. This architecture ensures high cohesion within domain modules, loose coupling between components, testability, and straightforward operational deployment."))
    c.append(para("The application layers comprise:"))
    c.append(bullet("Client Presentation Tier", "Server-side HTML5 views rendered via Thymeleaf templates, styled with a modern design system (theme.css and main.css) featuring responsive navigation, status badges, and accessible data tables."))
    c.append(bullet("Security & Web Controller Tier", "Spring Security 6 filter chain enforcing authenticated sessions, CSRF token validation, and URL-pattern authorization. Spring MVC Controllers (StudentController, FacultyController, AdminController, HomeController) handle HTTP GET/POST requests, validate input binding, and orchestrate view model population."))
    c.append(bullet("Business Service Tier", "Spring Services encapsulating transactional domain business logic, boundary validation, status state transitions, and audit generation (ExamService, MarksService, RecheckRequestService, ReviewService, AuditService, UserService)."))
    c.append(bullet("Data Access / Persistence Tier", "Spring Data JPA repositories executing optimized queries. Relationships utilize @EntityGraph join-fetching and Open-in-View configuration to ensure high performance and eliminate Hibernate lazy initialization hazards."))
    c.append(bullet("Database Storage Tier", "Relational database maintaining ACID guarantees. Configured for MySQL 8 in production and H2 in-memory storage for development and automated testing suites."))
    
    c.append(placeholder_box("2.1", "Multi-Tier Enterprise System Architecture", 
                             "Paste architecture diagram showing Client Browser -> Spring Security Filter Chain -> Controllers (Student/Faculty/Admin) -> Service Layer -> Spring Data JPA -> MySQL Database.",
                             "Docs / Design Architecture Diagram or Application Flowchart"))

    c.append(heading2("2.2 Use Case Diagram"))
    c.append(para("The system serves three primary human actors: Student, Faculty Member, and System Administrator. Each actor possesses discrete responsibilities and permitted actions."))
    
    c.append(placeholder_box("2.2", "System Use Case Diagram",
                             "Paste UML Use Case diagram showing Student, Faculty, and Admin actors connected to their respective use cases (View Marks, Lodge Re-eval, Review Request, Publish Exam, View Analytics, View Audit Logs).",
                             "Docs / UML Use Case Diagram"))

    uc_headers = ["Actor", "Primary Use Cases", "Security Permissions"]
    uc_rows = [
        ["Student", "View enrolled exam marks, view question breakdown, submit re-evaluation request, track request status, view revised grades", "ROLE_STUDENT access to /student/** endpoints"],
        ["Faculty", "Create & publish examinations, enter question-wise marks, inspect re-evaluation requests, review & amend marks, view dispute analytics", "ROLE_FACULTY access to /faculty/** endpoints"],
        ["Administrator", "Manage user registry (students & faculty), oversee institutional exams, inspect system compliance audit logs", "ROLE_ADMIN access to /admin/** endpoints"]
    ]
    c.append(table(uc_headers, uc_rows, [2000, 4800, 2400]))

    c.append(heading2("2.3 Class Diagram"))
    c.append(para("The object-oriented domain model represents all core entities, their bidirectional relationships, and encapsulated business states."))
    
    c.append(placeholder_box("2.3", "UML Class Diagram of Domain Model",
                             "Paste UML Class Diagram showing User, Role, Exam, Question, StudentResult, QuestionMark, RecheckRequest, Review, and AuditLog with attributes, methods, and multiplicities.",
                             "Docs / UML Class Diagram"))

    c.append(para("Key entities in the domain model include:"))
    c.append(bullet("User", "Represents an authenticated principal (email, passwordHash, role, name)."))
    c.append(bullet("Exam", "Represents an academic assessment (name, subject, examDate, reevaluationStart, reevaluationEnd, status)."))
    c.append(bullet("Question", "Represents an exam question item (exam, questionNumber, description, maxMarks)."))
    c.append(bullet("QuestionMark", "Stores granular marks obtained by a student for a specific question (student, question, marksObtained)."))
    c.append(bullet("StudentResult", "Maintains total exam marks aggregated for a student (student, exam, totalMarks)."))
    c.append(bullet("RecheckRequest", "Tracks the re-evaluation claim (student, exam, question, reason, status)."))
    c.append(bullet("Review", "Stores faculty evaluation decisions and amended marks (request, reviewer, decision, previousMarks, revisedMarks, remarks)."))
    c.append(bullet("AuditLog", "Stores immutable administrative records (performedBy, action, details, timestamp)."))

    c.append(heading2("2.4 Activity Diagram"))
    c.append(para("The activity diagram highlights the end-to-end lifecycle of an academic re-evaluation request, from student eligibility verification through faculty reassessment and mark updates."))

    c.append(placeholder_box("2.4", "Activity Diagram - Re-evaluation Request and Review Lifecycle",
                             "Paste UML Activity Diagram illustrating: Student selects question -> System checks window & duplicate -> Request created (SUBMITTED) -> Faculty opens request -> Status (UNDER_REVIEW) -> Faculty approves/rejects -> Marks updated -> Status (APPROVED/REJECTED) -> Audit logged.",
                             "Docs / UML Activity Diagram"))

    c.append(heading2("2.5 Database Design / ER Diagram"))
    c.append(para("The relational database schema is normalized to 3NF, guaranteeing referential integrity and enforcing critical business rules directly through database constraints."))

    c.append(placeholder_box("2.5", "Entity-Relationship (ER) Diagram",
                             "Paste ER diagram depicting relational schema tables (users, exams, questions, student_results, question_marks, recheck_requests, reviews, audit_logs) with primary/foreign keys.",
                             "Docs / ER Diagram"))

    c.append(para("The detailed Data Dictionary is summarized below:"))
    db_headers = ["Table Name", "Primary Key", "Foreign Keys", "Key Constraints / Indices"]
    db_rows = [
        ["users", "id (BIGINT)", "None", "UNIQUE(email), INDEX(role)"],
        ["exams", "id (BIGINT)", "None", "INDEX(status)"],
        ["questions", "id (BIGINT)", "exam_id -> exams.id", "UNIQUE(exam_id, question_number)"],
        ["student_results", "id (BIGINT)", "student_id -> users.id, exam_id -> exams.id", "UNIQUE(student_id, exam_id)"],
        ["question_marks", "id (BIGINT)", "student_id -> users.id, question_id -> questions.id", "UNIQUE(student_id, question_id)"],
        ["recheck_requests", "id (BIGINT)", "student_id -> users.id, exam_id -> exams.id, question_id -> questions.id", "ADR-003: UNIQUE(student_id, exam_id, question_id), INDEX(status)"],
        ["reviews", "id (BIGINT)", "request_id -> recheck_requests.id, reviewer_id -> users.id", "INDEX(reviewed_at)"],
        ["audit_logs", "id (BIGINT)", "user_id -> users.id", "INDEX(timestamp)"]
    ]
    c.append(table(db_headers, db_rows, [1800, 1600, 2600, 3200]))

    c.append(heading2("2.6 Module Description"))
    c.append(para("The application is divided into eight cohesive modules:"))
    c.append(bullet("Module 1 - Authentication & Security", "Implements Spring Security filter chains, BCrypt hashing, role authentication, custom user details loading, and session fixation defense."))
    c.append(bullet("Module 2 - Exam Management", "Allows faculty to create exams, define question descriptions, set maximum marks, and control lifecycle state transitions."))
    c.append(bullet("Module 3 - Marks Entry & Calculation", "Manages question-wise mark recording, validates against maximum question marks, and automatically computes cumulative student totals."))
    c.append(bullet("Module 4 - Re-evaluation Request Submission", "Validates student enrollment, checks active re-evaluation time windows, requires student justification, and prevents duplicate submissions."))
    c.append(bullet("Module 5 - Request Lifecycle Tracking", "Provides real-time visibility for students on all filed claims, displaying current review state and faculty decision feedback."))
    c.append(bullet("Module 6 - Faculty Review & Mark Revision", "Provides faculty with request queues, question-specific review tools, mark adjustment inputs, and automated recalculation of overall student scores."))
    c.append(bullet("Module 7 - Dispute Analytics & Hotspots", "Aggregates recheck requests across questions for each examination to identify pedagogical anomalies or difficult questions."))
    c.append(bullet("Module 8 - Audit & Compliance", "Generates immutable records of exam publications, grade alterations, and review decisions for institutional transparency."))

    # CHAPTER 3: IMPLEMENTATION
    c.append(page_break())
    c.append(heading1("Chapter 3: Implementation"))

    c.append(heading2("3.1 Technologies and Tools Used"))
    tech_headers = ["Technology / Tool", "Version", "Role in Project"]
    tech_rows = [
        ["Java Development Kit (JDK)", "Java 21 (LTS)", "Core programming language leveraging records, pattern matching, and enhanced switch syntax"],
        ["Spring Boot", "3.4.3", "Application framework providing auto-configuration, dependency injection, and embedded web server"],
        ["Spring Security", "6.4.3", "Authentication, role-based authorization, password encryption, and CSRF protection"],
        ["Spring Data JPA / Hibernate", "6.6.8", "Object-relational mapping (ORM), query generation, and transaction management"],
        ["Thymeleaf", "3.1.3", "Server-side template engine integrated with Spring Security extras for dynamic UI rendering"],
        ["MySQL Database", "8.0+", "Production relational database ensuring ACID guarantees and constraint enforcement"],
        ["H2 Database", "2.3.232", "High-speed in-memory database used for automated JUnit 5 test execution"],
        ["Apache Maven", "3.9+", "Build automation, project dependency management, and lifecycle packaging tool"],
        ["JUnit 5 & MockMvc", "Jupiter", "Unit, repository constraint, and web MVC controller integration testing"]
    ]
    c.append(table(tech_headers, tech_rows, [2200, 1600, 5400]))

    c.append(heading2("3.2 Project Structure / Package Structure"))
    c.append(para("The project codebase is organized under com.example.examreview following standard Spring enterprise conventions:"))
    pkg_structure = """com.example.examreview
├── ExamReviewApplication.java          (Main Spring Boot Application Entry Point)
├── config/
│   ├── SecurityConfig.java            (Spring Security filter chains & authorization rules)
│   └── DataInitializer.java          (Bootstrap seeder for demo users, exams, and marks)
├── controller/
│   ├── HomeController.java            (Public landing page and role-based redirects)
│   ├── StudentController.java         (Student dashboard, exam results, re-evaluation lodging)
│   ├── FacultyController.java         (Faculty exam management, review inbox, analytics)
│   └── AdminController.java           (User registry and compliance audit log inspection)
├── entity/
│   ├── Role.java, ExamStatus.java, RequestStatus.java, ReviewDecision.java (Enums)
│   ├── User.java, Exam.java, Question.java, QuestionMark.java (Core Domain Entities)
│   └── StudentResult.java, RecheckRequest.java, Review.java, AuditLog.java
├── repository/
│   ├── UserRepository.java, ExamRepository.java, QuestionRepository.java
│   ├── QuestionMarkRepository.java, StudentResultRepository.java
│   └── RecheckRequestRepository.java, ReviewRepository.java, AuditLogRepository.java
├── security/
│   ├── CustomUserDetailsService.java (Binds User entity to Spring Security Principal)
│   └── RoleBasedAuthenticationSuccessHandler.java (Directs users based on Role)
└── service/
    ├── UserService.java, ExamService.java, MarksService.java
    ├── RecheckRequestService.java, ReviewService.java, and AuditService.java"""
    c.append(code_block(pkg_structure))

    c.append(heading2("3.3 Description of Classes and Interfaces"))
    c.append(para("The implementation consists of clean, single-responsibility classes:"))
    c.append(bullet("StudentController", "Handles student endpoints: /student/dashboard, /student/exams, /student/exams/{id}, /student/requests/new, and /student/requests/{id}."))
    c.append(bullet("FacultyController", "Handles faculty endpoints: /faculty/dashboard, /faculty/exams, /faculty/requests, /faculty/requests/{id}/review, and /faculty/analytics."))
    c.append(bullet("AdminController", "Provides administrators access to /admin/dashboard, /admin/students, and /admin/audit-logs."))
    c.append(bullet("RecheckRequestService", "Encapsulates re-evaluation business rules, verifies date bounds, checks duplicate claims, and manages transactional persistence."))
    c.append(bullet("ReviewService", "Processes faculty verdicts, updates re-evaluation status, alters question marks, recalculates total marks, and records audit entries."))

    c.append(heading2("3.4 Implementation of Major Modules"))
    c.append(para("1. Re-evaluation Period Validation: Before allowing a student to file a dispute, the system verifies that the current timestamp is within exam.reevaluationStart and exam.reevaluationEnd and that the exam is in RE_EVALUATION_OPEN status."))
    c.append(para("2. Duplicate Request Prevention: The service executes an existance query; additionally, the database enforces UNIQUE(student_id, exam_id, question_id). Any race condition throws a DataIntegrityViolationException, preventing duplicate records."))
    c.append(para("3. Mark Revision & Grade Rollup: When a faculty member approves a review, the QuestionMark entity is updated with the revised score. MarksService.recordMark() is triggered, recalculating StudentResult.totalMarks and updating the student's standing."))

    c.append(heading2("3.5 Exception Handling"))
    c.append(para("Robust exception handling is implemented across all architectural layers:"))
    c.append(bullet("LazyInitializationException Prevention", "Resolved by pairing Spring's Open-in-View configuration (spring.jpa.open-in-view: true) with @EntityGraph join-fetch annotations on repositories, eliminating proxy errors during Thymeleaf rendering."))
    c.append(bullet("DataIntegrityViolationException", "Catches duplicate submission collisions at the database level and converts them into user-friendly flash error messages."))
    c.append(bullet("IllegalArgumentException & Validation Errors", "Validates revised marks to ensure they remain within [0.0, question.maxMarks] and that recheck reasons are non-empty."))
    c.append(bullet("AccessDeniedException (403)", "Custom HTTP 403 error template handles unauthorized role navigation attempts gracefully."))

    c.append(heading2("3.6 Collection Framework Usage"))
    c.append(para("The Java Collections Framework is extensively leveraged throughout the service and controller tiers:"))
    c.append(bullet("java.util.List", "Used for maintaining ordered collections of Question entities, StudentResult lists, and chronological RecheckRequest items."))
    c.append(bullet("java.util.Map", "Employed in FacultyController to map Question IDs to request frequency counts (Map<Long, Long>) for the analytics dashboard."))
    c.append(bullet("Java Streams API", "Streams are utilized for declarative filtering (e.g., counting requests by RequestStatus.SUBMITTED, RequestStatus.APPROVED) and mapping entities."))

    c.append(heading2("3.7 Database Connectivity"))
    c.append(para("The application utilizes HikariCP, the high-performance JDBC connection pool. The datasource configuration in application.yml dynamically adapts based on the active Spring profile:"))
    c.append(bullet("Development Profile (dev)", "Connects to an embedded H2 database (jdbc:h2:mem:examreviewdb;MODE=MySQL) enabling rapid prototyping without external database setup."))
    c.append(bullet("Production Profile (prod)", "Connects to a MySQL 8 server (jdbc:mysql://localhost:3306/exam_review_db) with connection pooling, character encoding, and timezone configurations."))

    c.append(heading2("3.8 Important Code Snippets"))
    c.append(para("Snippet 1: Enforcing Duplicate Prevention in RecheckRequestService.java"))
    snip1 = """@Transactional
public RecheckRequest submitRequest(User student, Long examId, Long questionId, String reason) {
    Exam exam = examRepository.findById(examId)
            .orElseThrow(() -> new IllegalArgumentException("Examination not found."));
    Question question = questionRepository.findById(questionId)
            .orElseThrow(() -> new IllegalArgumentException("Question not found."));

    if (exam.getStatus() != ExamStatus.RE_EVALUATION_OPEN) {
        throw new IllegalStateException("Re-evaluation window is not open for this exam.");
    }
    if (recheckRequestRepository.existsByStudentIdAndExamIdAndQuestionId(student.getId(), examId, questionId)) {
        throw new IllegalStateException("A re-evaluation request already exists for this question.");
    }

    RecheckRequest request = new RecheckRequest(student, exam, question, reason.trim());
    return recheckRequestRepository.saveAndFlush(request);
}"""
    c.append(code_block(snip1))

    c.append(para("Snippet 2: Faculty Review & Mark Amendment in ReviewService.java"))
    snip2 = """@Transactional
public Review submitReview(Long requestId, User faculty, ReviewDecision decision, 
                           Double revisedMarks, String remarks) {
    RecheckRequest request = recheckRequestRepository.findById(requestId)
            .orElseThrow(() -> new IllegalArgumentException("Request not found."));

    QuestionMark qMark = marksService.getQuestionMark(request.getStudent().getId(), 
                                                     request.getQuestion().getId()).orElseThrow();
    Double previousMarks = qMark.getMarksObtained();

    if (decision == ReviewDecision.APPROVED && revisedMarks != null) {
        if (revisedMarks < 0 || revisedMarks > request.getQuestion().getMaxMarks()) {
            throw new IllegalArgumentException("Marks must be between 0 and " + request.getQuestion().getMaxMarks());
        }
        marksService.recordMark(request.getStudent(), request.getQuestion(), revisedMarks);
        request.setStatus(RequestStatus.APPROVED);
    } else {
        request.setStatus(RequestStatus.REJECTED);
    }

    Review review = new Review(request, faculty, decision, previousMarks, revisedMarks, remarks);
    reviewRepository.save(review);
    return review;
}"""
    c.append(code_block(snip2))

    c.append(para("Snippet 3: High-Performance EntityGraph Repository in RecheckRequestRepository.java"))
    snip3 = """@Repository
public interface RecheckRequestRepository extends JpaRepository<RecheckRequest, Long> {
    @EntityGraph(attributePaths = {"student", "exam", "question"})
    List<RecheckRequest> findByStudentIdOrderByCreatedAtDesc(Long studentId);

    @EntityGraph(attributePaths = {"student", "exam", "question"})
    List<RecheckRequest> findByExamIdOrderByCreatedAtDesc(Long examId);

    @Query("SELECT r.question.id, COUNT(r) FROM RecheckRequest r WHERE r.exam.id = :examId GROUP BY r.question.id")
    List<Object[]> countRequestsByQuestionForExam(@Param("examId") Long examId);
}"""
    c.append(code_block(snip3))

    # CHAPTER 4: RESULTS AND SCREENSHOTS
    c.append(page_break())
    c.append(heading1("Chapter 4: Results and Screenshots"))

    c.append(heading2("4.1 Main Application Screen"))
    c.append(para("The landing page provides authentication entry points for Students, Faculty, and Administrators, displaying system overview information and quick demo login credentials."))
    c.append(placeholder_box("4.1", "Main Application Landing & Sign In Screen",
                             "Capture the public Sign In page showing the login card, email/password fields, and Quick Demo Credentials box.",
                             "http://localhost:8080/login"))

    c.append(heading2("4.2 Functional Screenshots"))
    c.append(para("Figure 4.2 illustrates the student workspace, summarizing enrolled examinations, pending reviews, and approved/rejected status counters."))
    c.append(placeholder_box("4.2", "Student Dashboard Interface",
                             "Capture student dashboard displaying summary stat cards (Exams Enrolled, Pending Requests, Approved, Rejected) and the examinations table.",
                             "http://localhost:8080/student/dashboard (Logged in as student@example.com)"))

    c.append(para("Figure 4.3 depicts the granular question-wise breakdown of an examination, detailing student marks against maximum marks with action buttons to lodge re-evaluations."))
    c.append(placeholder_box("4.3", "Examination Question Breakdown and Marks Table",
                             "Capture student exam detail view showing each question number, description, maximum marks, marks obtained, and the 'Request Re-evaluation' action buttons.",
                             "http://localhost:8080/student/exams/1"))

    c.append(para("Figure 4.4 displays the re-evaluation submission modal/form, requiring the student to enter detailed justification for challenging a specific question's score."))
    c.append(placeholder_box("4.4", "Question Re-evaluation Request Submission Form",
                             "Capture re-evaluation form with preselected Exam, Question number, current marks, and the student Reason text area.",
                             "http://localhost:8080/student/exams/1/recheck/4"))

    c.append(para("Figure 4.5 shows the student re-evaluation tracking workspace, listing submitted requests, current lifecycle badges, and links to detailed review findings."))
    c.append(placeholder_box("4.5", "Student Re-evaluation Request Tracking Lifecycle",
                             "Capture 'My Re-evaluation Requests' page showing the table of filed claims with dates, question numbers, and colored status badges.",
                             "http://localhost:8080/student/requests"))

    c.append(para("Figure 4.6 presents the faculty portal dashboard, showing active examinations, re-evaluation request counters, and access to the review worklist."))
    c.append(placeholder_box("4.6", "Faculty Dashboard & Evaluation Worklist",
                             "Capture faculty dashboard displaying active re-evaluations count, pending review cards, and quick actions to manage exams.",
                             "http://localhost:8080/faculty/dashboard (Logged in as faculty@example.com)"))

    c.append(para("Figure 4.7 showcases the question-level dispute analytics view, highlighting dispute frequency bars across exam questions to detect problem questions."))
    c.append(placeholder_box("4.7", "Question Analytics & Dispute Heatmap Interface",
                             "Capture faculty analytics page displaying question dispute counts (e.g. Q4 showing high request volume) and dispute percentages.",
                             "http://localhost:8080/faculty/analytics"))

    c.append(para("Figure 4.8 depicts the faculty review workspace, showing student reasoning, previous marks, revised marks input, and official faculty remarks."))
    c.append(placeholder_box("4.8", "Faculty Review & Marks Amendment Interface",
                             "Capture review modal or form showing student's justification, radio buttons for Approve/Reject, revised marks input field, and remarks box.",
                             "http://localhost:8080/faculty/requests/1/review"))

    c.append(para("Figure 4.9 shows the administrator student registry, listing enrolled students and their academic profiles."))
    c.append(placeholder_box("4.9", "Administrator Student Registry",
                             "Capture admin students list showing registered student names, email addresses, and roles.",
                             "http://localhost:8080/admin/students (Logged in as admin@example.com)"))

    c.append(para("Figure 4.10 displays the system audit logs, documenting immutable administrative actions, exam publications, and grade alterations."))
    c.append(placeholder_box("4.10", "System Compliance Audit Log Interface",
                             "Capture admin audit logs page showing timestamped audit events (SYSTEM_INIT, EXAM_PUBLISHED, REQUEST_SUBMITTED, REVIEW_COMPLETED).",
                             "http://localhost:8080/admin/audit-logs"))

    c.append(heading2("4.3 Input and Output Demonstrations"))
    c.append(para("The following test scenario demonstrates the system's end-to-end functionality:"))
    c.append(bullet("Input Step 1", "Student logs in and inspects 'Data Structures Mid-Semester Examination' containing scores: Q1: 8/10, Q2: 3/10, Q3: 9/10, Q4: 2/10, Q5: 10/10 (Total: 32/50)."))
    c.append(bullet("Input Step 2", "Student selects Question 4 and submits recheck reason: 'The relaxation condition in Dijkstra algorithm step was correctly implemented using priority queues.'"))
    c.append(bullet("Output Step 1", "System validates request window, verifies no duplicate exists, stores request in SUBMITTED state, and displays confirmation alert."))
    c.append(bullet("Input Step 3", "Faculty logs into /faculty/requests, opens the Q4 request, verifies student code, marks decision as APPROVED, enters revised marks '7.0', and inputs remarks 'Correction acknowledged.'"))
    c.append(bullet("Output Step 2", "System marks request APPROVED, updates Q4 marks from 2.0 to 7.0, recalculates student total from 32.0 to 37.0, and writes an audit log entry."))

    c.append(heading2("4.4 Error Handling Demonstrations"))
    c.append(para("The system incorporates multi-layered defensive validation. Screenshots of error prevention mechanisms are detailed below:"))
    c.append(placeholder_box("4.11", "Duplicate Re-evaluation Request Prevention Alert",
                             "Capture student screen when attempting to submit a duplicate re-evaluation for the same question, displaying error alert: 'A re-evaluation request already exists for this question.'",
                             "http://localhost:8080/student/exams/1/recheck/4 (Second submission attempt)"))

    c.append(placeholder_box("4.12", "Access Denied (403 Forbidden) Security Protection",
                             "Capture HTTP 403 Forbidden access-denied page when a student attempts to navigate directly to /faculty/dashboard or /admin/dashboard.",
                             "http://localhost:8080/faculty/dashboard (While logged in as student)"))

    c.append(placeholder_box("4.13", "Form Input Validation Feedback",
                             "Capture validation error messages when submitting out-of-range marks (e.g. entering 15 on a 10-mark question) or submitting an empty dispute reason.",
                             "http://localhost:8080/faculty/requests/1/review"))

    # REFERENCES
    c.append(page_break())
    c.append(heading1("References"))
    refs = [
        "Walls, C. (2022). Spring in Action (6th ed.). Manning Publications.",
        "Bauer, C., King, G., & Gregory, G. (2015). Java Persistence with Hibernate (2nd ed.). Manning Publications.",
        "Thyam, S. (2023). Pro Spring Security: Securing Spring Boot Applications. Apress.",
        "Oracle Corporation. (2023). Java Platform, Standard Edition Documentation (JDK 21 LTS). https://docs.oracle.com/en/java/javase/21/",
        "Spring Framework Team. (2025). Spring Boot Reference Documentation (v3.4.x). https://docs.spring.io/spring-boot/docs/current/reference/html/",
        "Thymeleaf Standard Documentation. (2024). Using Thymeleaf (v3.1.x). https://www.thymeleaf.org/doc/tutorials/3.1/usingthymeleaf.html",
        "Sommerville, I. (2016). Software Engineering (10th ed.). Pearson Education.",
        "Martin, R. C. (2018). Clean Architecture: A Craftsman's Guide to Software Structure and Design. Prentice Hall."
    ]
    for r_idx, r in enumerate(refs):
        c.append(bullet(f"[{r_idx+1}]", r))
        
    return "\n".join(c)

def generate_markdown_version():
    md = """# UCS553: Enterprise Web Application
## Mini Project Report
# Exam Question Re-evaluation and Review Management System

**Department of Computer Science & Engineering**  
**Thapar Institute of Engineering & Technology, Patiala**  
*November 2026*

---

## Abstract
In modern higher education institutions, the traditional examination re-evaluation process is predominantly paper-based, cumbersome, and inherently opaque. Students are frequently mandated to apply for an entire examination re-check rather than querying specific disputed evaluation criteria or questions. Consequently, evaluators endure severe repetitive manual workloads, administrative staff face logistics overheads, and students remain uninformed regarding the exact progress and rationale of their re-evaluation requests.

This project presents the **Exam Question Re-evaluation and Review Management System**, an enterprise-grade, web-based software application engineered to modernize and streamline the academic re-evaluation lifecycle. Developed using **Java 21, Spring Boot 3.4.3, Spring Security 6, Spring Data JPA, Hibernate ORM, and Thymeleaf**, the system delivers a secure, role-segregated environment for Students, Faculty, and Administrators.

---

## Table of Contents
1. **Chapter 1: Introduction**
   - 1.1 Introduction to the Project
   - 1.2 Problem Statement
   - 1.3 Objectives of the Project
   - 1.4 Scope of the Project
2. **Chapter 2: System Design**
   - 2.1 System Architecture
   - 2.2 Use Case Diagram
   - 2.3 Class Diagram
   - 2.4 Activity Diagram
   - 2.5 Database Design / ER Diagram
   - 2.6 Module Description
3. **Chapter 3: Implementation**
   - 3.1 Technologies and Tools Used
   - 3.2 Project Structure / Package Structure
   - 3.3 Description of Classes and Interfaces
   - 3.4 Implementation of Major Modules
   - 3.5 Exception Handling
   - 3.6 Collection Framework Usage
   - 3.7 Database Connectivity
   - 3.8 Important Code Snippets
4. **Chapter 4: Results and Screenshots**
   - 4.1 Main Application Screen
   - 4.2 Functional Screenshots
   - 4.3 Input and Output Demonstrations
   - 4.4 Error Handling Demonstrations
5. **References**

---

## Chapter 1: Introduction

### 1.1 Introduction to the Project
Assessment and evaluation represent the cornerstone of academic measurement in higher education. At the conclusion of semester examinations, institutional examination cells publish final mark sheets and provide a window for students dissatisfied with their awarded marks to request re-evaluation or paper re-checking. In traditional university setups, this process is governed through physical forms, bank challans, manual paper retrieval from archives, and ad-hoc reassignment to faculty evaluators. This conventional process suffers from substantial friction, extreme latency, and lack of accountability.

The Exam Question Re-evaluation and Review Management System is an enterprise software solution designed to transition academic dispute resolution into the modern digital era. Implemented on top of the robust Spring Boot framework, the application organizes the examination lifecycle into clear, structured stages: examination scheduling, question-wise marks entry, controlled re-evaluation window opening, granular question-level dispute lodging, faculty review workflows, and automated grade recalculations.

### 1.2 Problem Statement
The traditional examination re-evaluation process across academic institutions exhibits several fundamental vulnerabilities:
- **Lack of Evaluation Granularity**: Students are forced to pay for and request re-evaluation of an entire subject, even when their dispute concerns a single question's marking criteria.
- **Operational Opacity**: Once a physical form is submitted, students have no visibility into the workflow.
- **Concurrency & Duplicate Lodging Vulnerabilities**: Physical or naive web forms frequently allow duplicate submissions for the same question or examination.
- **High Administrative Latency**: Physical transit of answer scripts between administrative vaults and evaluators takes weeks.
- **Absence of Diagnostic Feedback**: Conventional systems fail to provide institutional leadership with aggregate metrics regarding question paper quality.

### 1.3 Objectives of the Project
- **Role-Based Security & Governance**: Implement strict RBAC separating Student, Faculty, and Administrator capabilities using Spring Security 6 and BCrypt password hashing.
- **Granular Dispute Management**: Enable students to inspect individual question marks against maximum score ceilings and file targeted re-evaluation claims with technical reasoning.
- **Concurrency & Duplicate Prevention**: Enforce multi-layered duplicate submission guards through service validation and database unique constraints (`UNIQUE(student_id, exam_id, question_id)`).
- **Structured Faculty Review Pipeline**: Provide faculty members with a centralized review inbox, dispute reasoning analysis, mark revision controls, and formal remark logging.
- **Real-Time Status Tracking**: Deliver end-to-end lifecycle tracking (`SUBMITTED` -> `UNDER_REVIEW` -> `APPROVED` / `REJECTED` -> `COMPLETED`) for students.
- **Educational Analytics**: Provide faculty with question-level dispute frequency aggregations to flag pedagogical and exam design anomalies.
- **Traceable Audit Trail**: Maintain an immutable, timestamped audit log of all administrative actions, exam publications, and grade alterations.

### 1.4 Scope of the Project
- **In-Scope Functional Features**: User authentication, student question-wise marks breakdown, re-evaluation window enforcement, dispute filing, duplicate request rejection, faculty review decisioning, automated mark rollups, dispute analytics, and audit logging.
- **Optional / Advanced Features**: Automated question dispute threshold alerts, email notification hooks, and supporting document attachments.
- **Out-of-Scope Boundaries**: Conducting online computer-based examinations, automated AI auto-grading of subjective answers, optical character recognition (OCR) of handwritten answer sheets, and payment gateway banking integrations.

---

## Chapter 2: System Design

### 2.1 System Architecture
The application is structured following the Modular Monolith pattern (ADR-001) using a standard enterprise multi-tier architecture:
- **Client Presentation Tier**: Server-side HTML5 views rendered via Thymeleaf templates, styled with modern responsive CSS.
- **Security & Controller Tier**: Spring Security filter chain enforcing authenticated sessions and URL-pattern authorization. Spring MVC Controllers handle HTTP requests and view models.
- **Business Service Tier**: Spring Services encapsulating transactional domain business logic and boundary validation.
- **Data Access Tier**: Spring Data JPA repositories executing queries with `@EntityGraph` join-fetching to prevent lazy initialization issues.
- **Database Storage Tier**: Relational database (MySQL 8 in production, H2 in dev/test) ensuring ACID guarantees.

> **[IMAGE PLACEHOLDER - Figure 2.1: Multi-Tier Enterprise System Architecture]**  
> *What to paste:* Paste architecture diagram showing Client Browser -> Spring Security Filter Chain -> Controllers (Student/Faculty/Admin) -> Service Layer -> Spring Data JPA -> MySQL Database.  
> *Source / Location:* Docs / Architecture Flowchart

### 2.2 Use Case Diagram

> **[IMAGE PLACEHOLDER - Figure 2.2: System Use Case Diagram]**  
> *What to paste:* Paste UML Use Case diagram showing Student, Faculty, and Admin actors connected to their respective use cases.  
> *Source / Location:* Docs / UML Use Case Diagram

| Actor | Primary Use Cases | Security Permissions |
| :--- | :--- | :--- |
| **Student** | View enrolled exam marks, view question breakdown, submit re-evaluation request, track request status, view revised grades | `ROLE_STUDENT` access to `/student/**` |
| **Faculty** | Create & publish examinations, enter question-wise marks, inspect re-evaluation requests, review & amend marks, view dispute analytics | `ROLE_FACULTY` access to `/faculty/**` |
| **Administrator** | Manage user registry (students & faculty), oversee institutional exams, inspect system compliance audit logs | `ROLE_ADMIN` access to `/admin/**` |

### 2.3 Class Diagram

> **[IMAGE PLACEHOLDER - Figure 2.3: UML Class Diagram of Domain Model]**  
> *What to paste:* Paste UML Class Diagram showing User, Role, Exam, Question, StudentResult, QuestionMark, RecheckRequest, Review, and AuditLog with attributes and associations.  
> *Source / Location:* Docs / UML Class Diagram

### 2.4 Activity Diagram

> **[IMAGE PLACEHOLDER - Figure 2.4: Activity Diagram - Re-evaluation Request and Review Lifecycle]**  
> *What to paste:* Paste UML Activity Diagram illustrating: Student selects question -> System checks window & duplicate -> Request created (SUBMITTED) -> Faculty opens request -> Status (UNDER_REVIEW) -> Faculty approves/rejects -> Marks updated -> Status (APPROVED/REJECTED) -> Audit logged.  
> *Source / Location:* Docs / UML Activity Diagram

### 2.5 Database Design / ER Diagram

> **[IMAGE PLACEHOLDER - Figure 2.5: Entity-Relationship (ER) Diagram]**  
> *What to paste:* Paste ER diagram depicting relational schema tables (users, exams, questions, student_results, question_marks, recheck_requests, reviews, audit_logs) with primary/foreign keys.  
> *Source / Location:* Docs / ER Diagram

| Table Name | Primary Key | Foreign Keys | Key Constraints / Indices |
| :--- | :--- | :--- | :--- |
| `users` | id (BIGINT) | None | `UNIQUE(email)`, `INDEX(role)` |
| `exams` | id (BIGINT) | None | `INDEX(status)` |
| `questions` | id (BIGINT) | `exam_id -> exams.id` | `UNIQUE(exam_id, question_number)` |
| `student_results` | id (BIGINT) | `student_id -> users.id`, `exam_id -> exams.id` | `UNIQUE(student_id, exam_id)` |
| `question_marks` | id (BIGINT) | `student_id -> users.id`, `question_id -> questions.id` | `UNIQUE(student_id, question_id)` |
| `recheck_requests` | id (BIGINT) | `student_id -> users.id`, `exam_id -> exams.id`, `question_id -> questions.id` | `ADR-003: UNIQUE(student_id, exam_id, question_id)`, `INDEX(status)` |
| `reviews` | id (BIGINT) | `request_id -> recheck_requests.id`, `reviewer_id -> users.id` | `INDEX(reviewed_at)` |
| `audit_logs` | id (BIGINT) | `user_id -> users.id` | `INDEX(timestamp)` |

### 2.6 Module Description
1. **Authentication & Role-Based Access Control**: Spring Security 6 filter chains, BCrypt hashing, role authentication, and session protection.
2. **Exam Management Module**: Faculty tools to create exams, define questions, set maximum marks, and manage status transitions.
3. **Marks Management Module**: Granular marks recording, input bounds validation, and automated student aggregate calculation.
4. **Re-evaluation Request Core**: Validates student eligibility, time window, and duplicate prevention.
5. **Request Tracking Module**: Real-time lifecycle dashboard for student visibility.
6. **Faculty Review Module**: Review queue, remarks logging, and automated total mark recalculation upon approved revision.
7. **Dispute Analytics Module**: Aggregation queries detecting frequently challenged questions.
8. **Audit Trail Module**: Tamper-proof recording of administrative actions and grade changes.

---

## Chapter 3: Implementation

### 3.1 Technologies and Tools Used
- **JDK 21 LTS**: Core modern Java runtime.
- **Spring Boot 3.4.3**: Enterprise rapid web application framework.
- **Spring Security 6.4.3**: Authentication, RBAC, and CSRF protection.
- **Spring Data JPA & Hibernate 6.6.8**: ORM, query execution, and transactions.
- **Thymeleaf 3.1.3**: Server-side template engine.
- **MySQL 8 & H2 Database**: Production and testing persistence stores.
- **JUnit 5 & MockMvc**: Comprehensive test automation.

### 3.2 Project Structure
```
com.example.examreview
├── ExamReviewApplication.java
├── config/ (SecurityConfig.java, DataInitializer.java)
├── controller/ (StudentController, FacultyController, AdminController, HomeController)
├── entity/ (User, Exam, Question, StudentResult, QuestionMark, RecheckRequest, Review, AuditLog)
├── repository/ (All JPA repositories with @EntityGraph optimizations)
├── security/ (CustomUserDetailsService, RoleBasedAuthenticationSuccessHandler)
└── service/ (UserService, ExamService, MarksService, RecheckRequestService, ReviewService, AuditService)
```

### 3.3 Description of Classes and Interfaces
- `StudentController`: Exposes `/student/dashboard`, `/student/exams`, `/student/requests`.
- `FacultyController`: Exposes `/faculty/dashboard`, `/faculty/exams`, `/faculty/requests`, `/faculty/analytics`.
- `AdminController`: Exposes `/admin/dashboard`, `/admin/students`, `/admin/audit-logs`.
- `RecheckRequestService`: Encapsulates recheck submission, period checking, and duplicate prevention.
- `ReviewService`: Handles faculty evaluations, mark amendments, and audit events.

### 3.4 Major Modules Implementation
- **Eligibility & Period Validation**: Verifies active exam status and time bounds before allowing request creation.
- **Duplicate Prevention**: Multi-tier check using `existsByStudentIdAndExamIdAndQuestionId()` backed by database unique constraint.
- **Mark Revision**: Updates question mark and calls `marksService.recordMark()` to automatically update overall student totals.

### 3.5 Exception Handling
- **LazyInitializationException**: Eliminated by enabling `spring.jpa.open-in-view: true` and adding `@EntityGraph` join-fetching to repository queries.
- **DataIntegrityViolationException**: Traps duplicate submission attempts gracefully.
- **IllegalArgumentException**: Enforces mark bounds between 0 and question maximum marks.
- **AccessDeniedException (403)**: Renders a dedicated access-denied template.

### 3.6 Collection Framework Usage
Extensive utilization of `java.util.List` for ordered entity collections, `java.util.Map` for question dispute counts, and Java Streams for declarative status filtering.

### 3.7 Database Connectivity
Configured via HikariCP in `application.yml` with dual profiles: `dev` (in-memory H2) and `prod` (MySQL 8).

### 3.8 Important Code Snippets

```java
// RecheckRequestService.java: Duplicate Prevention & Re-evaluation Submission
@Transactional
public RecheckRequest submitRequest(User student, Long examId, Long questionId, String reason) {
    Exam exam = examRepository.findById(examId)
            .orElseThrow(() -> new IllegalArgumentException("Examination not found."));
    Question question = questionRepository.findById(questionId)
            .orElseThrow(() -> new IllegalArgumentException("Question not found."));

    if (exam.getStatus() != ExamStatus.RE_EVALUATION_OPEN) {
        throw new IllegalStateException("Re-evaluation window is not open for this exam.");
    }
    if (recheckRequestRepository.existsByStudentIdAndExamIdAndQuestionId(student.getId(), examId, questionId)) {
        throw new IllegalStateException("A re-evaluation request already exists for this question.");
    }

    RecheckRequest request = new RecheckRequest(student, exam, question, reason.trim());
    return recheckRequestRepository.saveAndFlush(request);
}
```

```java
// ReviewService.java: Faculty Review and Mark Revision
@Transactional
public Review submitReview(Long requestId, User faculty, ReviewDecision decision, 
                           Double revisedMarks, String remarks) {
    RecheckRequest request = recheckRequestRepository.findById(requestId)
            .orElseThrow(() -> new IllegalArgumentException("Request not found."));

    QuestionMark qMark = marksService.getQuestionMark(request.getStudent().getId(), 
                                                     request.getQuestion().getId()).orElseThrow();
    Double previousMarks = qMark.getMarksObtained();

    if (decision == ReviewDecision.APPROVED && revisedMarks != null) {
        if (revisedMarks < 0 || revisedMarks > request.getQuestion().getMaxMarks()) {
            throw new IllegalArgumentException("Marks must be between 0 and " + request.getQuestion().getMaxMarks());
        }
        marksService.recordMark(request.getStudent(), request.getQuestion(), revisedMarks);
        request.setStatus(RequestStatus.APPROVED);
    } else {
        request.setStatus(RequestStatus.REJECTED);
    }

    Review review = new Review(request, faculty, decision, previousMarks, revisedMarks, remarks);
    reviewRepository.save(review);
    return review;
}
```

---

## Chapter 4: Results and Screenshots

### 4.1 Main Application Screen

> **[IMAGE PLACEHOLDER - Figure 4.1: Main Application Landing & Sign In Screen]**  
> *What to paste:* Capture the public Sign In page showing the login card, email/password fields, and Quick Demo Credentials box.  
> *Source / Location:* `http://localhost:8080/login`

### 4.2 Functional Screenshots

> **[IMAGE PLACEHOLDER - Figure 4.2: Student Dashboard Interface]**  
> *What to paste:* Capture student dashboard displaying summary stat cards (Exams Enrolled, Pending Requests, Approved, Rejected) and the examinations table.  
> *Source / Location:* `http://localhost:8080/student/dashboard` (Logged in as `student@example.com`)

> **[IMAGE PLACEHOLDER - Figure 4.3: Examination Question Breakdown and Marks Table]**  
> *What to paste:* Capture student exam detail view showing each question number, description, maximum marks, marks obtained, and the 'Request Re-evaluation' action buttons.  
> *Source / Location:* `http://localhost:8080/student/exams/1`

> **[IMAGE PLACEHOLDER - Figure 4.4: Question Re-evaluation Request Submission Form]**  
> *What to paste:* Capture re-evaluation form with preselected Exam, Question number, current marks, and the student Reason text area.  
> *Source / Location:* `http://localhost:8080/student/exams/1/recheck/4`

> **[IMAGE PLACEHOLDER - Figure 4.5: Student Re-evaluation Request Tracking Lifecycle]**  
> *What to paste:* Capture 'My Re-evaluation Requests' page showing the table of filed claims with dates, question numbers, and colored status badges.  
> *Source / Location:* `http://localhost:8080/student/requests`

> **[IMAGE PLACEHOLDER - Figure 4.6: Faculty Dashboard & Evaluation Worklist]**  
> *What to paste:* Capture faculty dashboard displaying active re-evaluations count, pending review cards, and quick actions to manage exams.  
> *Source / Location:* `http://localhost:8080/faculty/dashboard` (Logged in as `faculty@example.com`)

> **[IMAGE PLACEHOLDER - Figure 4.7: Question Analytics & Dispute Heatmap Interface]**  
> *What to paste:* Capture faculty analytics page displaying question dispute counts (e.g. Q4 showing high request volume) and dispute percentages.  
> *Source / Location:* `http://localhost:8080/faculty/analytics`

> **[IMAGE PLACEHOLDER - Figure 4.8: Faculty Review & Marks Amendment Interface]**  
> *What to paste:* Capture review modal or form showing student's justification, radio buttons for Approve/Reject, revised marks input field, and remarks box.  
> *Source / Location:* `http://localhost:8080/faculty/requests/1/review`

> **[IMAGE PLACEHOLDER - Figure 4.9: Administrator Student Registry]**  
> *What to paste:* Capture admin students list showing registered student names, email addresses, and roles.  
> *Source / Location:* `http://localhost:8080/admin/students` (Logged in as `admin@example.com`)

> **[IMAGE PLACEHOLDER - Figure 4.10: System Compliance Audit Log Interface]**  
> *What to paste:* Capture admin audit logs page showing timestamped audit events (`SYSTEM_INIT`, `EXAM_PUBLISHED`, `REQUEST_SUBMITTED`, `REVIEW_COMPLETED`).  
> *Source / Location:* `http://localhost:8080/admin/audit-logs`

### 4.3 Input and Output Demonstrations
- **Step 1**: Student signs in and opens *Data Structures Mid-Semester Examination* (Scores: Q1: 8/10, Q2: 3/10, Q3: 9/10, Q4: 2/10, Q5: 10/10).
- **Step 2**: Student lodges recheck on Question 4 with technical reasoning.
- **Step 3**: Faculty opens review queue, inspects Q4 dispute, verifies code, and approves request with revised score: 7.0/10.
- **Step 4**: Student cumulative grade card updates automatically from 32/50 to 37/50, and action is logged in audit trail.

### 4.4 Error Handling Demonstrations

> **[IMAGE PLACEHOLDER - Figure 4.11: Duplicate Re-evaluation Request Prevention Alert]**  
> *What to paste:* Capture student screen when attempting to submit a duplicate re-evaluation for the same question, displaying error alert: 'A re-evaluation request already exists for this question.'  
> *Source / Location:* `http://localhost:8080/student/exams/1/recheck/4` (Second submission attempt)

> **[IMAGE PLACEHOLDER - Figure 4.12: Access Denied (403 Forbidden) Security Protection]**  
> *What to paste:* Capture HTTP 403 Forbidden access-denied page when a student attempts to navigate directly to `/faculty/dashboard` or `/admin/dashboard`.  
> *Source / Location:* `http://localhost:8080/faculty/dashboard` (While logged in as student)

> **[IMAGE PLACEHOLDER - Figure 4.13: Form Input Validation Feedback]**  
> *What to paste:* Capture validation error messages when submitting out-of-range marks or an empty dispute reason.  
> *Source / Location:* `http://localhost:8080/faculty/requests/1/review`

---

## References
1. Walls, C. (2022). *Spring in Action* (6th ed.). Manning Publications.
2. Bauer, C., King, G., & Gregory, G. (2015). *Java Persistence with Hibernate* (2nd ed.). Manning Publications.
3. Thyam, S. (2023). *Pro Spring Security: Securing Spring Boot Applications*. Apress.
4. Oracle Corporation. (2023). *Java Platform, Standard Edition Documentation (JDK 21 LTS)*. https://docs.oracle.com/en/java/javase/21/
5. Spring Framework Team. (2025). *Spring Boot Reference Documentation (v3.4.x)*. https://docs.spring.io/spring-boot/docs/current/reference/html/
6. Thymeleaf Standard Documentation. (2024). *Using Thymeleaf (v3.1.x)*. https://www.thymeleaf.org/doc/tutorials/3.1/usingthymeleaf.html
7. Sommerville, I. (2016). *Software Engineering* (10th ed.). Pearson Education.
8. Martin, R. C. (2018). *Clean Architecture: A Craftsman's Guide to Software Structure and Design*. Prentice Hall.
"""
    with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
        f.write(md)
    print(f"Markdown report generated at: {OUTPUT_MD}")

def main():
    print("Extracting template...")
    with zipfile.ZipFile(TEMPLATE_PATH) as z:
        content = z.read('word/document.xml').decode('utf-8')
        
    split_token = '<w:t>Java Mini Project Report Format</w:t>'
    idx = content.find(split_token)
    p_start = content.rfind('<w:p ', 0, idx)
    cover_xml = content[:p_start]
    
    # Replace Project title in cover page
    cover_xml = cover_xml.replace('Name of the Project', 'Exam Question Re-evaluation and Review Management System')
    
    # Final section XML
    final_sect = """<w:sectPr w:rsidR="000E72B8"><w:type w:val="continuous"/><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1320" w:right="1133" w:bottom="280" w:left="1700" w:header="720" w:footer="720" w:gutter="0"/><w:pgBorders w:offsetFrom="page"><w:top w:val="single" w:sz="8" w:space="22" w:color="000000"/><w:left w:val="single" w:sz="8" w:space="22" w:color="000000"/><w:bottom w:val="single" w:sz="8" w:space="22" w:color="000000"/><w:right w:val="single" w:sz="8" w:space="22" w:color="000000"/></w:pgBorders><w:cols w:space="720"/></w:sectPr></w:body></w:document>"""
    
    print("Building report content...")
    report_body = build_report_content()
    
    full_document_xml = cover_xml + report_body + final_sect
    
    print("Packaging into docx...")
    temp_zip = OUTPUT_DOCX + '.tmp'
    with zipfile.ZipFile(TEMPLATE_PATH, 'r') as zin:
        with zipfile.ZipFile(temp_zip, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                if item.filename == 'word/document.xml':
                    zout.writestr(item, full_document_xml.encode('utf-8'))
                else:
                    zout.writestr(item, zin.read(item.filename))
                    
    shutil.move(temp_zip, OUTPUT_DOCX)
    print(f"Generated DOCX at: {OUTPUT_DOCX}")
    
    generate_markdown_version()
    print("Done!")

if __name__ == '__main__':
    main()
