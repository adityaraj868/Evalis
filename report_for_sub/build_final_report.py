import zipfile
import html
import os
import shutil
import struct
import subprocess

TEMPLATE_PATH = '/home/epsilon/clg/Enterprise/report_for_sub/Java Project Report Format.docx'
FINAL_DOCX = '/home/epsilon/clg/Enterprise/report_for_sub/Exam_Review_System_Final_Report.docx'
FINAL_PDF = '/home/epsilon/clg/Enterprise/report_for_sub/Exam_Review_System_Final_Report.pdf'
FINAL_MD = '/home/epsilon/clg/Enterprise/report_for_sub/FINAL_PROJECT_REPORT.md'
DIAGRAMS_DIR = '/home/epsilon/clg/Enterprise/docs/diagrams'
SCREENSHOTS_DIR = '/home/epsilon/clg/Enterprise/docs/website-screenshots'

def get_png_dimensions(file_path):
    with open(file_path, 'rb') as f:
        data = f.read(24)
        if data[:8] == b'\x89PNG\r\n\x1a\n' and data[12:16] == b'IHDR':
            w, h = struct.unpack('>LL', data[16:24])
            return w, h
    return 1920, 1080

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
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:color w:val="1A365D"/>
      <w:sz w:val="34"/>
      <w:szCs w:val="34"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
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
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:color w:val="2B6CB0"/>
      <w:sz w:val="28"/>
      <w:szCs w:val="28"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
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
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:color w:val="2D3748"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
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
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
    <w:t xml:space="preserve">{esc(bold_prefix)}: </w:t>
  </w:r>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:sz w:val="24"/>
      <w:szCs w:val="24"/>
    </w:rPr>
    <w:t xml:space="preserve">{esc(text)}</w:t>
  </w:r>
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

def make_embedded_image(r_id, doc_pr_id, name, img_path, fig_num, caption, max_width_in=6.0, max_height_in=4.2):
    w_px, h_px = get_png_dimensions(img_path)
    aspect = w_px / float(h_px) if h_px else 1.77
    
    target_w = max_width_in
    target_h = target_w / aspect
    
    if target_h > max_height_in:
        target_h = max_height_in
        target_w = target_h * aspect
        
    cx = int(target_w * 914400)
    cy = int(target_h * 914400)
    
    p_img = f"""<w:p>
  <w:pPr>
    <w:jc w:val="center"/>
    <w:spacing w:before="140" w:after="60"/>
  </w:pPr>
  <w:r>
    <w:drawing>
      <wp:inline distT="0" distB="0" distL="0" distR="0">
        <wp:extent cx="{cx}" cy="{cy}"/>
        <wp:effectExtent l="0" t="0" r="0" b="0"/>
        <wp:docPr id="{doc_pr_id}" name="{esc(name)}"/>
        <wp:cNvGraphicFramePr>
          <a:graphicFrameLocks xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" noChangeAspect="1"/>
        </wp:cNvGraphicFramePr>
        <a:graphic xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
          <a:graphicData uri="http://schemas.openxmlformats.org/drawingml/2006/picture">
            <pic:pic xmlns:pic="http://schemas.openxmlformats.org/drawingml/2006/picture">
              <pic:nvPicPr>
                <pic:cNvPr id="{doc_pr_id}" name="{esc(name)}"/>
                <pic:cNvPicPr/>
              </pic:nvPicPr>
              <pic:blipFill>
                <a:blip r:embed="{r_id}" cstate="print"/>
                <a:stretch>
                  <a:fillRect/>
                </a:stretch>
              </pic:blipFill>
              <pic:spPr>
                <a:xfrm>
                  <a:off x="0" y="0"/>
                  <a:ext cx="{cx}" cy="{cy}"/>
                </a:xfrm>
                <a:prstGeom prst="rect">
                  <a:avLst/>
                </a:prstGeom>
              </pic:spPr>
            </pic:pic>
          </a:graphicData>
        </a:graphic>
      </wp:inline>
    </w:drawing>
  </w:r>
</w:p>"""
    p_cap = f"""<w:p>
  <w:pPr>
    <w:jc w:val="center"/>
    <w:spacing w:before="40" w:after="160"/>
  </w:pPr>
  <w:r>
    <w:rPr>
      <w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/>
      <w:b/>
      <w:i/>
      <w:color w:val="2D3748"/>
      <w:sz w:val="20"/>
    </w:rPr>
    <w:t>Figure {esc(fig_num)}: {esc(caption)}</w:t>
  </w:r>
</w:p>"""
    return p_img + "\n" + p_cap

print("Base generator utilities initialized.")

def build_report_body():
    c = []

    # CERTIFICATE & DECLARATION
    c.append(page_break())
    c.append(heading1("Certificate of Original Work"))
    c.append(para("This is to certify that the project entitled \"Exam Question Re-evaluation and Review Management System\" submitted by Adityaraj Singh (Roll No. 1024170148), Sparsh Khandelwal (Roll No. 1024170139), and Vaibhav Goyal (Roll No. 1024170002) in partial fulfillment of the requirements for the award of Bachelor of Engineering in Computer Engineering at Thapar Institute of Engineering & Technology, Patiala, is an authentic record of our own original work carried out under the supervision and guidance of Chinu."))
    c.append(para("The matter embodied in this report has not been submitted in part or full to any other University or Institute for the award of any degree."))
    c.append(para(""))
    c.append(para(""))
    
    cert_headers = ["Student Name", "Roll Number", "Signature"]
    cert_rows = [
        ["Adityaraj Singh", "1024170148", "_______________________"],
        ["Sparsh Khandelwal", "1024170139", "_______________________"],
        ["Vaibhav Goyal", "1024170002", "_______________________"]
    ]
    c.append(table(cert_headers, cert_rows, [3000, 2600, 3600]))
    c.append(para(""))
    c.append(para("This is to certify that the above statement made by the candidates is correct to the best of my knowledge."))
    c.append(para(""))
    c.append(para("Project Guide / Supervisor:"))
    c.append(para("Chinu", bold=True))
    c.append(para("Thapar Institute of Engineering Technology, Patiala"))

    # ABSTRACT
    c.append(page_break())
    c.append(heading1("Abstract"))
    c.append(para("In contemporary higher education ecosystems, the conventional examination re-evaluation process remains predominantly paper-based, cumbersome, and inherently opaque. Students are frequently mandated to apply for a whole-subject re-check rather than querying specific disputed evaluation criteria or questions. Consequently, academic evaluators endure substantial repetitive manual workloads, administrative offices face costly logistical delays, and students remain deprived of timely, transparent feedback regarding the exact progress and rationale of their re-evaluation requests. Furthermore, institutions miss critical systemic insights—such as recurring evaluation discrepancies or inherently ambiguous exam questions that generate disproportionate dispute volumes."))
    c.append(para("This project presents the Exam Question Re-evaluation and Review Management System, an enterprise-grade, web-based software application engineered to modernize and streamline the academic re-evaluation lifecycle. Developed using Java 21, Spring Boot 3.4.3, Spring Security 6, Spring Data JPA, Hibernate 6, and Thymeleaf, the system delivers a secure, role-segregated environment for Students, Faculty, and Administrators. Students can inspect granular question-level marks against maximum ceilings, submit targeted re-evaluation claims with technical justifications within active submission windows, and monitor real-time decision transitions. Concurrency controls and database-level unique constraints strictly eliminate duplicate submissions."))
    c.append(para("Faculty evaluators access a centralized workspace to inspect disputes grouped by question, verify original student marks against question limits, record amended scores, and input official review remarks. System administrators maintain governance via a tamper-proof audit trail capturing all critical assessment events. By replacing subjective, opaque paperwork with a transparent, role-governed, and data-driven digital workflow, the platform accelerates dispute turnaround, enforces academic integrity, and equips institutional leadership with question-level analytics for curriculum enhancement."))

    # TABLE OF CONTENTS
    c.append(page_break())
    c.append(heading1("Table of Contents"))
    toc_headers = ["S. No.", "Chapter / Section Name", "Page No."]
    toc_rows = [
        ["1", "Cover Page", "1"],
        ["2", "Certificate of Original Work", "2"],
        ["3", "Abstract", "3"],
        ["4", "Table of Contents", "4"],
        ["5", "Chapter 1: Introduction", "5"],
        ["", "1.1 Introduction to the Project", "5"],
        ["", "1.2 Problem Statement", "6"],
        ["", "1.3 Objectives of the Project", "6"],
        ["", "1.4 Scope of the Project", "7"],
        ["6", "Chapter 2: System Design", "8"],
        ["", "2.1 System Architecture", "8"],
        ["", "2.2 Layered Architecture", "10"],
        ["", "2.3 Use Case Diagram", "11"],
        ["", "2.4 Class Diagram", "13"],
        ["", "2.5 Activity Diagram", "15"],
        ["", "2.6 Sequence Diagrams", "17"],
        ["", "2.7 State Transition Diagrams", "19"],
        ["", "2.8 Database Design / ER Diagram", "21"],
        ["", "2.9 Module Description", "24"],
        ["7", "Chapter 3: Implementation", "27"],
        ["", "3.1 Technologies and Tools Used", "27"],
        ["", "3.2 Project Structure / Package Structure", "28"],
        ["", "3.3 Description of Classes and Interfaces", "30"],
        ["", "3.4 Implementation of Major Modules", "33"],
        ["", "3.5 Exception Handling & Optimization", "35"],
        ["", "3.6 Collection Framework Usage", "37"],
        ["", "3.7 Database Connectivity", "38"],
        ["", "3.8 Important Code Snippets", "39"],
        ["8", "Chapter 4: Results and Screenshots", "43"],
        ["", "4.1 Student Portal Interface", "43"],
        ["", "4.2 Faculty Portal & Analytics Interface", "46"],
        ["", "4.3 Administrative Audit Trail Interface", "49"],
        ["", "4.4 Functional Walkthrough & Demonstrations", "51"],
        ["", "4.5 Security and Robustness Verification", "53"],
        ["9", "References", "55"]
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
    c.append(bullet("Absence of Diagnostic Feedback", "Conventional systems fail to provide institutional leadership with aggregate metrics. If an entire student cohort files re-evaluations for a single question due to an ambiguous problem statement or key error, the department remains blind to the anomaly."))

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
    c.append(para("To ensure software quality and high engineering rigor, the operational boundary of the project is categorized as follows:"))
    c.append(bullet("Implemented Core Scope", "User authentication, role segregation (Student, Faculty, Admin), student question-wise marks breakdown, re-evaluation window enforcement, dispute filing, duplicate request rejection, faculty review decisioning, automated mark rollups, dispute analytics, and audit logging."))
    c.append(bullet("Proposed Future Enhancements", "Automated email/SMS notification hooks, student PDF grade card export, supporting document attachments (such as official solution keys), and multi-department institutional routing."))
    c.append(bullet("Explicitly Out-of-Scope", "Conducting online computer-based examinations, automated AI auto-grading of subjective answers, optical character recognition (OCR) of handwritten answer sheets, and payment gateway banking integrations."))

    # CHAPTER 2: SYSTEM DESIGN
    c.append(page_break())
    c.append(heading1("Chapter 2: System Design"))

    c.append(heading2("2.1 System Architecture"))
    c.append(para("The system is engineered following the Modular Monolith pattern (ADR-001) using a standard enterprise multi-tier architecture. This architecture ensures high cohesion within domain modules, loose coupling between components, testability, and straightforward operational deployment."))
    c.append(para("Figure 2.1 illustrates the high-level system architecture, tracing incoming client traffic through Spring Security, Web Controllers, transactional Services, Spring Data JPA repositories, and the underlying relational database."))

    # Insert Figure 2.1: System Architecture
    img_arch = os.path.join(DIAGRAMS_DIR, 'system-architecture.png')
    c.append(make_embedded_image("rId101", 101, "System Architecture", img_arch, "2.1", "Multi-Tier Enterprise System Architecture Diagram"))

    c.append(heading2("2.2 Layered Architecture"))
    c.append(para("To maintain a clean separation of concerns, the codebase is strictly partitioned into five vertical layers:"))
    c.append(bullet("Presentation Layer (UI)", "Server-side HTML5 views rendered via Thymeleaf templates, styled with modern responsive CSS (theme.css, main.css)."))
    c.append(bullet("Web & Controller Layer", "Spring MVC Controllers (@Controller) managing request mapping, session validation, form binding, and HTTP redirection."))
    c.append(bullet("Service Layer", "Spring Services (@Service, @Transactional) executing core business rules, period validation, duplicate detection, and grade aggregation."))
    c.append(bullet("Persistence Layer", "Spring Data JPA repositories utilizing Hibernate 6 ORM with @EntityGraph join-fetching for optimal query execution."))
    c.append(bullet("Infrastructure & Database Layer", "ACID-compliant relational storage configured with HikariCP connection pooling."))

    # Insert Figure 2.2: Layered Architecture
    img_layer = os.path.join(DIAGRAMS_DIR, 'layered-architecture.png')
    c.append(make_embedded_image("rId102", 102, "Layered Architecture", img_layer, "2.2", "Layered Software Architecture Diagram"))

    c.append(heading2("2.3 Use Case Diagram"))
    c.append(para("The platform serves three distinct human actors: Student, Faculty, and Administrator. Figure 2.3 depicts the UML Use Case Diagram illustrating the system boundaries and authorized interactions."))

    # Insert Figure 2.3: Use Case Diagram
    img_uc = os.path.join(DIAGRAMS_DIR, 'use-case-diagram.png')
    c.append(make_embedded_image("rId103", 103, "Use Case Diagram", img_uc, "2.3", "UML Use Case Diagram of the Exam Review System"))

    c.append(para("The actor responsibilities and security access mappings are defined in Table 2.1:"))
    uc_headers = ["Actor", "Primary Use Cases", "Security Role"]
    uc_rows = [
        ["Student", "View enrolled exam marks, inspect question breakdown, submit re-evaluation request, track request status, view revised marks", "ROLE_STUDENT (/student/**)"],
        ["Faculty", "Create & publish exams, enter question marks, inspect re-evaluation requests, review & amend marks, view dispute analytics", "ROLE_FACULTY (/faculty/**)"],
        ["Administrator", "Manage student/faculty registry, monitor institutional exams, inspect system compliance audit logs", "ROLE_ADMIN (/admin/**)"]
    ]
    c.append(table(uc_headers, uc_rows, [1800, 5200, 2200]))

    c.append(heading2("2.4 Class Diagram"))
    c.append(para("Figure 2.4 illustrates the UML Class Diagram of the domain model, showing all persistent entity classes, enums, attributes, methods, and relationship cardinalities."))

    # Insert Figure 2.4: Class Diagram
    img_class = os.path.join(DIAGRAMS_DIR, 'class-diagram.png')
    c.append(make_embedded_image("rId104", 104, "Class Diagram", img_class, "2.4", "UML Class Diagram of Domain Model Entities"))

    c.append(para("Key entities in the domain model include:"))
    c.append(bullet("User", "Represents an authenticated principal (email, passwordHash, role, name, createdAt)."))
    c.append(bullet("Exam", "Represents an assessment (name, subject, examDate, reevaluationStart, reevaluationEnd, status)."))
    c.append(bullet("Question", "Represents a single question item (exam, questionNumber, description, maxMarks)."))
    c.append(bullet("QuestionMark", "Stores granular marks obtained by a student for a specific question (student, question, marksObtained)."))
    c.append(bullet("StudentResult", "Maintains total exam marks aggregated for a student (student, exam, totalMarks)."))
    c.append(bullet("RecheckRequest", "Tracks the re-evaluation claim (student, exam, question, reason, status)."))
    c.append(bullet("Review", "Stores faculty evaluation decisions and amended marks (request, reviewer, decision, previousMarks, revisedMarks, remarks)."))
    c.append(bullet("AuditLog", "Stores immutable administrative records (performedBy, action, details, timestamp)."))

    c.append(heading2("2.5 Activity Diagram"))
    c.append(para("Figure 2.5 depicts the UML Activity Diagram illustrating the sequential decision-making process for filing and processing an academic re-evaluation request."))

    # Insert Figure 2.5: Activity Diagram
    img_act = os.path.join(DIAGRAMS_DIR, 'activity-diagram.png')
    c.append(make_embedded_image("rId105", 105, "Activity Diagram", img_act, "2.5", "UML Activity Diagram — Re-evaluation Request and Review Lifecycle"))

    c.append(heading2("2.6 Sequence Diagrams"))
    c.append(para("To depict the runtime dynamic interactions across system components, two detailed UML Sequence Diagrams are modeled for the critical operational workflows."))
    c.append(para("1. Re-evaluation Request Submission: Traces the student request flow from the browser through controller validation, time window verification, duplicate checking (ADR-003), database persistence, and audit logging."))

    # Insert Figure 2.6: Sequence Submission
    img_seq_sub = os.path.join(DIAGRAMS_DIR, 'sequence-diagram-submission.png')
    c.append(make_embedded_image("rId106", 106, "Sequence Submission", img_seq_sub, "2.6", "Sequence Diagram — Student Re-evaluation Request Submission"))

    c.append(para("2. Faculty Review and Mark Revision: Traces the faculty review flow, showing decision processing, question mark update, cumulative score recalculation, and audit recording."))

    # Insert Figure 2.7: Sequence Review
    img_seq_rev = os.path.join(DIAGRAMS_DIR, 'sequence-diagram-review.png')
    c.append(make_embedded_image("rId107", 107, "Sequence Review", img_seq_rev, "2.7", "Sequence Diagram — Faculty Review and Mark Revision Workflow"))

    c.append(heading2("2.7 State Transition Diagrams"))
    c.append(para("The application enforces deterministic finite state machines for both examinations and re-evaluation requests."))
    c.append(para("Figure 2.8 outlines the Examination Lifecycle, traversing from DRAFT creation through PUBLISHED results, active RE_EVALUATION_OPEN window, RE_EVALUATION_CLOSED, and eventual ARCHIVED status."))

    # Insert Figure 2.8: Exam State Diagram
    img_exam_st = os.path.join(DIAGRAMS_DIR, 'exam-state-diagram.png')
    c.append(make_embedded_image("rId108", 108, "Exam State Diagram", img_exam_st, "2.8", "Examination Lifecycle State Transition Diagram"))

    c.append(para("Figure 2.9 depicts the Re-evaluation Request Lifecycle, progressing from SUBMITTED to UNDER_REVIEW, culminating in either APPROVED (with score amendment) or REJECTED status."))

    # Insert Figure 2.9: Request State Diagram
    img_req_st = os.path.join(DIAGRAMS_DIR, 'request-state-diagram.png')
    c.append(make_embedded_image("rId109", 109, "Request State Diagram", img_req_st, "2.9", "Re-evaluation Request Lifecycle State Transition Diagram"))

    c.append(heading2("2.8 Database Design / ER Diagram"))
    c.append(para("Figure 2.10 displays the Entity-Relationship (ER) Diagram representing the relational database schema normalized to Third Normal Form (3NF)."))

    # Insert Figure 2.10: ER Diagram
    img_er = os.path.join(DIAGRAMS_DIR, 'er-diagram.png')
    c.append(make_embedded_image("rId110", 110, "ER Diagram", img_er, "2.10", "Entity-Relationship (ER) Schema Diagram"))

    c.append(para("The schema enforces structural integrity through primary keys, foreign key relationships, and compound unique constraints as detailed in Table 2.2:"))
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

    c.append(heading2("2.9 Module Description"))
    c.append(para("The application is partitioned into eight modular subsystems:"))
    c.append(bullet("1. Authentication & Role-Based Access Control", "Implements Spring Security filter chains, BCrypt hashing, role authentication, custom user details loading, and session protection."))
    c.append(bullet("2. Exam Management Module", "Allows faculty to create exams, define question descriptions, set maximum marks, and manage status transitions."))
    c.append(bullet("3. Marks Entry & Calculation Module", "Manages question-wise mark recording, validates against maximum question marks, and automatically computes cumulative student totals."))
    c.append(bullet("4. Re-evaluation Request Submission Module", "Validates student enrollment, checks active re-evaluation time windows, requires student justification, and prevents duplicate submissions."))
    c.append(bullet("5. Request Tracking Module", "Provides real-time visibility for students on all filed claims, displaying current review state and faculty decision feedback."))
    c.append(bullet("6. Faculty Review & Mark Revision Module", "Provides faculty with request queues, question-specific review tools, mark adjustment inputs, and automated recalculation of overall student scores."))
    c.append(bullet("7. Dispute Analytics & Hotspots Module", "Aggregates recheck requests across questions for each examination to identify pedagogical anomalies or difficult questions."))
    c.append(bullet("8. Audit & Compliance Module", "Generates immutable records of exam publications, grade alterations, and review decisions for institutional transparency."))

    # CHAPTER 3: IMPLEMENTATION
    c.append(page_break())
    c.append(heading1("Chapter 3: Implementation"))

    c.append(heading2("3.1 Technologies and Tools Used"))
    tech_headers = ["Technology / Tool", "Version", "Role in Project"]
    tech_rows = [
        ["Java Development Kit (JDK)", "Java 21 (LTS)", "Core programming language leveraging records, pattern matching, and enhanced switch syntax"],
        ["Spring Boot", "3.4.3", "Application framework providing auto-configuration, dependency injection, and embedded Tomcat"],
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

    c.append(heading2("3.5 Exception Handling & Optimization"))
    c.append(para("Robust exception handling and performance optimizations are implemented across all architectural layers:"))
    c.append(bullet("LazyInitializationException Resolution", "Resolved by pairing Spring's Open-in-View configuration (spring.jpa.open-in-view: true) with @EntityGraph join-fetch annotations on repositories, eliminating proxy errors during Thymeleaf rendering while avoiding N+1 queries."))
    c.append(bullet("DataIntegrityViolationException Handling", "Catches duplicate submission collisions at the database level and converts them into user-friendly flash error messages."))
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

    c.append(heading2("4.1 Student Portal Interface"))
    c.append(para("The Student Portal provides students with a dedicated, role-segregated environment to review their enrolled examinations, inspect granular question-level scores, lodge justified re-evaluation requests, and track their dispute lifecycle."))
    c.append(para("Figure 4.1 captures the Student Dashboard interface. The upper section features key summary cards displaying Exams Enrolled (1), Pending Requests (0), Approved Reviews (0), and Rejected Reviews (0). The lower table lists enrolled examinations, displaying the examination name ('Data Structures Mid-Semester Examination'), subject ('Data Structures & Algorithms'), active status badge ('Re-eval Open'), total awarded marks ('32.0'), and an action button to inspect the question breakdown."))

    # Insert Figure 4.1: Student Dashboard
    img_sd = os.path.join(SCREENSHOTS_DIR, 'student-dashboard.png')
    c.append(make_embedded_image("rId111", 111, "Student Dashboard", img_sd, "4.1", "Student Portal Dashboard — Overview Cards and Enrolled Examinations Table"))

    c.append(para("Figure 4.2 illustrates the Question-Wise Marks Breakdown view accessed by clicking 'View Breakdown'. Unlike traditional monolithic report cards, the interface exposes question-by-question scoring against maximum limits. In this demonstration, the student received: Q1: 8.0/10.0, Q2: 3.0/10.0, Q3: 9.0/10.0, Q4: 2.0/10.0, and Q5: 10.0/10.0 (Total: 32.0/50.0). For each question, an active 'Request Re-evaluation' button enables students to challenge specific question scores."))

    # Insert Figure 4.2: Question Marks
    img_qm = os.path.join(SCREENSHOTS_DIR, 'question_marks.png')
    c.append(make_embedded_image("rId112", 112, "Question Marks Breakdown", img_qm, "4.2", "Examination Question-Wise Marks Breakdown and Re-evaluation Action Interface"))

    c.append(para("Figure 4.3 depicts the Student Re-evaluation Request Submission Form triggered when clicking 'Request Re-evaluation' on Question 4. The modal explicitly reminds the student of the question statement ('Describe Dijkstra's shortest path algorithm with a pseudocode example'), maximum marks (10.0), and current score (2.0). The student must provide a mandatory technical justification in the reason text area before submitting."))

    # Insert Figure 4.3: Re-evaluation Form
    img_rf = os.path.join(SCREENSHOTS_DIR, 'reevaluation-form.png')
    if not os.path.exists(img_rf):
        img_rf = os.path.join(SCREENSHOTS_DIR, 'reevalutaion-form.png')
    c.append(make_embedded_image("rId113", 113, "Re-evaluation Form", img_rf, "4.3", "Question Re-evaluation Request Submission Form with Mandatory Reason Input"))

    c.append(heading2("4.2 Faculty Portal & Analytics Interface"))
    c.append(para("The Faculty Portal provides educators and evaluators with comprehensive administrative controls over exam publishing, request review workflows, and cohort-level question performance analytics."))
    c.append(para("Figure 4.4 displays the Faculty Dashboard. The dashboard presents actionable metric cards: Open Re-evaluations (1), Total Examinations (1), Total Questions (5), and Pending Reviews (1). The lower tables provide direct management links for active examinations and a priority worklist of incoming re-evaluation requests submitted by students."))

    # Insert Figure 4.4: Faculty Dashboard
    img_fd = os.path.join(SCREENSHOTS_DIR, 'faculty-dashboard.png')
    c.append(make_embedded_image("rId114", 114, "Faculty Dashboard", img_fd, "4.4", "Faculty Portal Dashboard — Examination Overview and Pending Reviews Worklist"))

    c.append(para("Figure 4.5 highlights the Question-Wise Dispute Analytics interface. By aggregating recheck requests grouped by question, the system provides faculty with immediate diagnostic feedback on question difficulty and dispute distribution. In the demonstrated cohort, Question 4 accounts for 100% of all submitted re-evaluations, immediately flagging it as a potential dispute hotspot requiring review of the marking key or problem statement."))

    # Insert Figure 4.5: Question Analytics
    img_qa = os.path.join(SCREENSHOTS_DIR, 'question-analytics.png')
    c.append(make_embedded_image("rId115", 115, "Question Analytics", img_qa, "4.5", "Question-Wise Dispute Analytics and Request Distribution Heatmap"))

    c.append(heading2("4.3 Administrative Audit Trail Interface"))
    c.append(para("To ensure institutional compliance and eliminate unauthorized grade alterations, the platform incorporates an immutable, timestamped audit log visible to system administrators."))
    c.append(para("Figure 4.6 captures the Administrative Audit Log interface. Every significant action—system initialization, exam publication, student request lodging, and faculty grade revisions—is permanently chronicled with the performing user's name, role badge, action identifier, and detailed change context."))

    # Insert Figure 4.6: Audit Logs
    img_al = os.path.join(SCREENSHOTS_DIR, 'audit-logs.png')
    c.append(make_embedded_image("rId116", 116, "Audit Logs", img_al, "4.6", "System Compliance Audit Log Interface — Chronological Administrative Action Trail"))

    c.append(heading2("4.4 Functional Walkthrough & Demonstrations"))
    c.append(para("The end-to-end operational workflow of the application was thoroughly verified across all three user roles:"))
    c.append(bullet("Step 1: Student Mark Inspection", "Logged in as John Student (student@example.com). Inspected 'Data Structures Mid-Semester Examination' and identified an evaluation discrepancy on Question 4 (Dijkstra algorithm, scored 2.0/10.0, total 32.0/50.0)."))
    c.append(bullet("Step 2: Re-evaluation Lodging", "Navigated to Q4 recheck form, entered technical justification: 'The relaxation condition in Dijkstra step was correctly implemented using priority queues. Please recheck step 4.' Submitted request successfully; status transitioned to SUBMITTED."))
    c.append(bullet("Step 3: Duplicate Submission Guard", "Attempted to submit a duplicate re-evaluation for Question 4. The application intercepted the submission, displaying flash warning: 'A re-evaluation request already exists for this question.' Database constraint UNIQUE(student_id, exam_id, question_id) verified intact."))
    c.append(bullet("Step 4: Faculty Evaluation & Revision", "Logged in as Prof. Alan Turing (faculty@example.com). Inspected Question Analytics to observe Q4 dispute spike. Opened student review request, inspected student reasoning, selected APPROVED, entered revised score 7.0/10.0, and entered remarks 'Correction acknowledged.'"))
    c.append(bullet("Step 5: Automated Grade Rollup", "Verified that QuestionMark for Q4 updated from 2.0 to 7.0. StudentResult automatically recalculated total score from 32.0/50.0 to 37.0/50.0. An immutable audit record was written."))
    c.append(bullet("Step 6: Student Tracking Verification", "Logged back in as John Student. Verified that the re-evaluation status updated to APPROVED, revised mark 7.0 was displayed, and the cumulative score updated to 37.0."))

    c.append(heading2("4.5 Security and Robustness Verification"))
    c.append(para("The security and robustness mechanisms were validated against the test suite:"))
    c.append(bullet("Role-Based Access Enforcement", "Direct URL tampering attempts (e.g., student navigating to /faculty/dashboard or /admin/audit-logs) were successfully intercepted by Spring Security, rendering the custom HTTP 403 Forbidden page."))
    c.append(bullet("Mark Boundary Protection", "Attempting to enter negative marks (-2.0) or marks exceeding maximum ceilings (15.0 on a 10.0 mark question) resulted in immediate validation rejections."))
    c.append(bullet("ORM Session Safety", "All 12 automated JUnit 5 / MockMvc integration tests executed with zero failures, confirming that open-in-view and @EntityGraph eager join-fetching prevent lazy initialization proxy exceptions."))

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

def main():
    print("Extracting template cover page...")
    with zipfile.ZipFile(TEMPLATE_PATH) as z:
        content = z.read('word/document.xml').decode('utf-8')
        
    split_token = '<w:t>Java Mini Project Report Format</w:t>'
    idx = content.find(split_token)
    p_start = content.rfind('<w:p ', 0, idx)
    cover_xml = content[:p_start]
    
    # 1. Replace Project title
    cover_xml = cover_xml.replace('Name of the Project', 'Exam Question Re-evaluation and Review Management System')
    
    # 2. Replace Guide block
    p_guide_of = cover_xml.find('>of</w:t>')
    p_guide_end = cover_xml.find('<w:drawing>', p_guide_of)
    p_draw_para = cover_xml.rfind('<w:p ', 0, p_guide_end)
    p_of_para_end = cover_xml.find('</w:p>', p_guide_of) + 6
    
    new_guide = '''<w:p><w:pPr><w:spacing w:before="140" w:after="40"/><w:jc w:val="center"/><w:rPr><w:b/><w:sz w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="32"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr><w:t>Chinu</w:t></w:r></w:p><w:p><w:pPr><w:spacing w:before="40" w:after="140"/><w:jc w:val="center"/><w:rPr><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr></w:pPr><w:r><w:rPr><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr><w:t>Thapar Institute of Engineering Technology, Patiala</w:t></w:r></w:p>'''
    cover_xml = cover_xml[:p_of_para_end] + new_guide + cover_xml[p_draw_para:]
    
    # 3. Replace Student block
    sub_idx = cover_xml.find('Submitted ')
    p_sub_end = cover_xml.find('</w:p>', sub_idx) + 6
    cs_idx = cover_xml.find('Computer Science', p_sub_end)
    p_cs_start = cover_xml.rfind('<w:p ', 0, cs_idx)
    
    new_students = '''<w:p><w:pPr><w:ind w:left="2200"/><w:spacing w:before="80" w:after="40"/><w:rPr><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr><w:t xml:space="preserve">1024170148    </w:t></w:r><w:r><w:rPr><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr><w:t>Adityaraj Singh</w:t></w:r></w:p><w:p><w:pPr><w:ind w:left="2200"/><w:spacing w:before="40" w:after="40"/><w:rPr><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr><w:t xml:space="preserve">1024170139    </w:t></w:r><w:r><w:rPr><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr><w:t>Sparsh Khandelwal</w:t></w:r></w:p><w:p><w:pPr><w:ind w:left="2200"/><w:spacing w:before="40" w:after="100"/><w:rPr><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr></w:pPr><w:r><w:rPr><w:b/><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr><w:t xml:space="preserve">1024170002    </w:t></w:r><w:r><w:rPr><w:sz w:val="24"/><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman"/></w:rPr><w:t>Vaibhav Goyal</w:t></w:r></w:p>'''
    cover_xml = cover_xml[:p_sub_end] + new_students + cover_xml[p_cs_start:]

    print("Building full report body...")
    body_xml = build_report_body()
    
    final_sect = """<w:sectPr w:rsidR="000E72B8"><w:type w:val="continuous"/><w:pgSz w:w="12240" w:h="15840"/><w:pgMar w:top="1320" w:right="1133" w:bottom="280" w:left="1700" w:header="720" w:footer="720" w:gutter="0"/><w:pgBorders w:offsetFrom="page"><w:top w:val="single" w:sz="8" w:space="22" w:color="000000"/><w:left w:val="single" w:sz="8" w:space="22" w:color="000000"/><w:bottom w:val="single" w:sz="8" w:space="22" w:color="000000"/><w:right w:val="single" w:sz="8" w:space="22" w:color="000000"/></w:pgBorders><w:cols w:space="720"/></w:sectPr></w:body></w:document>"""
    full_document_xml = cover_xml + body_xml + final_sect

    # Images mapping to embed
    images_to_embed = [
        # (rId, filename, full_path)
        ("rId101", "system-architecture.png", os.path.join(DIAGRAMS_DIR, "system-architecture.png")),
        ("rId102", "layered-architecture.png", os.path.join(DIAGRAMS_DIR, "layered-architecture.png")),
        ("rId103", "use-case-diagram.png", os.path.join(DIAGRAMS_DIR, "use-case-diagram.png")),
        ("rId104", "class-diagram.png", os.path.join(DIAGRAMS_DIR, "class-diagram.png")),
        ("rId105", "activity-diagram.png", os.path.join(DIAGRAMS_DIR, "activity-diagram.png")),
        ("rId106", "sequence-diagram-submission.png", os.path.join(DIAGRAMS_DIR, "sequence-diagram-submission.png")),
        ("rId107", "sequence-diagram-review.png", os.path.join(DIAGRAMS_DIR, "sequence-diagram-review.png")),
        ("rId108", "exam-state-diagram.png", os.path.join(DIAGRAMS_DIR, "exam-state-diagram.png")),
        ("rId109", "request-state-diagram.png", os.path.join(DIAGRAMS_DIR, "request-state-diagram.png")),
        ("rId110", "er-diagram.png", os.path.join(DIAGRAMS_DIR, "er-diagram.png")),
        ("rId111", "student-dashboard.png", os.path.join(SCREENSHOTS_DIR, "student-dashboard.png")),
        ("rId112", "question_marks.png", os.path.join(SCREENSHOTS_DIR, "question_marks.png")),
        ("rId113", "reevaluation-form.png", os.path.join(SCREENSHOTS_DIR, "reevaluation-form.png")),
        ("rId114", "faculty-dashboard.png", os.path.join(SCREENSHOTS_DIR, "faculty-dashboard.png")),
        ("rId115", "question-analytics.png", os.path.join(SCREENSHOTS_DIR, "question-analytics.png")),
        ("rId116", "audit-logs.png", os.path.join(SCREENSHOTS_DIR, "audit-logs.png"))
    ]

    print("Packaging DOCX with all 16 embedded images...")
    temp_docx = FINAL_DOCX + '.tmp'
    with zipfile.ZipFile(TEMPLATE_PATH, 'r') as zin:
        with zipfile.ZipFile(temp_docx, 'w', compression=zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == 'word/document.xml':
                    data = full_document_xml.encode('utf-8')
                elif item.filename == '[Content_Types].xml':
                    txt = data.decode('utf-8')
                    if 'Extension="png"' not in txt:
                        txt = txt.replace('</Types>', '<Default Extension="png" ContentType="image/png"/></Types>')
                    data = txt.encode('utf-8')
                elif item.filename == 'word/_rels/document.xml.rels':
                    txt = data.decode('utf-8')
                    rel_entries = []
                    for rid, fname, fpath in images_to_embed:
                        rel_entries.append(f'<Relationship Id="{rid}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/image" Target="media/{fname}"/>')
                    txt = txt.replace('</Relationships>', "".join(rel_entries) + '</Relationships>')
                    data = txt.encode('utf-8')
                zout.writestr(item, data)
                
            # Add all image bytes into word/media/
            for rid, fname, fpath in images_to_embed:
                with open(fpath, 'rb') as imgf:
                    zout.writestr(f'word/media/{fname}', imgf.read())

    shutil.move(temp_docx, FINAL_DOCX)
    print(f"Final DOCX created: {FINAL_DOCX} ({os.path.getsize(FINAL_DOCX)} bytes)")

    # Also copy to root project directory for convenience
    root_docx = '/home/epsilon/clg/Enterprise/Exam_Review_System_Final_Report.docx'
    shutil.copyfile(FINAL_DOCX, root_docx)
    print(f"Copied to root: {root_docx}")

    # Convert to PDF
    print("Converting DOCX to PDF via LibreOffice...")
    cmd = ["soffice", "--headless", "--convert-to", "pdf", FINAL_DOCX, "--outdir", "/home/epsilon/clg/Enterprise/report_for_sub/"]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode == 0 and os.path.exists(FINAL_PDF):
        print(f"Final PDF created: {FINAL_PDF} ({os.path.getsize(FINAL_PDF)} bytes)")
        root_pdf = '/home/epsilon/clg/Enterprise/Exam_Review_System_Final_Report.pdf'
        shutil.copyfile(FINAL_PDF, root_pdf)
        print(f"Copied PDF to root: {root_pdf}")
    else:
        print(f"PDF conversion failed: {res.stderr.decode()}")

if __name__ == '__main__':
    main()
