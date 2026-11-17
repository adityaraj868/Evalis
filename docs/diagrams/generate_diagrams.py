import os
import subprocess

DIAGRAMS_DIR = '/home/epsilon/clg/Enterprise/docs/diagrams'
os.makedirs(DIAGRAMS_DIR, exist_ok=True)

def save_and_convert(svg_content, name):
    svg_path = os.path.join(DIAGRAMS_DIR, f"{name}.svg")
    png_path = os.path.join(DIAGRAMS_DIR, f"{name}.png")
    with open(svg_path, 'w', encoding='utf-8') as f:
        f.write(svg_content)
    
    cmd = ["soffice", "--headless", "--convert-to", "png", svg_path, "--outdir", DIAGRAMS_DIR]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if res.returncode != 0:
        print(f"Error converting {name}: {res.stderr.decode()}")
    else:
        print(f"Generated {name}.png ({os.path.getsize(png_path)} bytes)")

# 1. High-Level System Architecture
def make_system_architecture():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 600" width="1000" height="600" font-family="Arial, sans-serif">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#F8FAFC"/><stop offset="100%" stop-color="#EDF2F7"/></linearGradient>
    <linearGradient id="clientGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#3182CE"/><stop offset="100%" stop-color="#2B6CB0"/></linearGradient>
    <linearGradient id="secGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#DD6B20"/><stop offset="100%" stop-color="#C05621"/></linearGradient>
    <linearGradient id="ctrlGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#319795"/><stop offset="100%" stop-color="#285E61"/></linearGradient>
    <linearGradient id="srvGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#805AD5"/><stop offset="100%" stop-color="#6B46C1"/></linearGradient>
    <linearGradient id="repoGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#D69E2E"/><stop offset="100%" stop-color="#B7791F"/></linearGradient>
    <linearGradient id="dbGrad" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#E53E3E"/><stop offset="100%" stop-color="#C53030"/></linearGradient>
    <filter id="shadow" x="-2%" y="-2%" width="104%" height="104%"><feDropShadow dx="2" dy="3" stdDeviation="3" flood-opacity="0.15"/></filter>
  </defs>
  <rect width="1000" height="600" fill="url(#bg)" rx="10"/>
  <text x="500" y="35" text-anchor="middle" font-size="20" font-weight="bold" fill="#1A202C">High-Level System Architecture</text>
  <text x="500" y="58" text-anchor="middle" font-size="13" fill="#4A5568">Multi-Tier Enterprise Examination Re-evaluation Platform</text>

  <!-- Client Layer -->
  <rect x="50" y="80" width="900" height="65" rx="8" fill="url(#clientGrad)" filter="url(#shadow)"/>
  <text x="500" y="105" text-anchor="middle" font-size="15" font-weight="bold" fill="#FFF">Client Presentation Tier (Web Browsers)</text>
  <text x="500" y="128" text-anchor="middle" font-size="12" fill="#EBF8FF">HTML5 / Responsive CSS3 (theme.css, main.css) · Thymeleaf Server-Side Templates · JavaScript DOM Interaction</text>

  <!-- Arrow -->
  <path d="M 500 145 L 500 170" stroke="#4A5568" stroke-width="2" marker-end="url(#arrow)"/>
  <text x="510" y="162" font-size="11" fill="#718096">HTTPS / Requests (CSRF)</text>

  <!-- Security Filter -->
  <rect x="50" y="175" width="900" height="55" rx="8" fill="url(#secGrad)" filter="url(#shadow)"/>
  <text x="500" y="198" text-anchor="middle" font-size="15" font-weight="bold" fill="#FFF">Spring Security 6 Tier</text>
  <text x="500" y="218" text-anchor="middle" font-size="12" fill="#FEEBC8">SecurityFilterChain · BCryptPasswordEncoder · Role Authorization (STUDENT, FACULTY, ADMIN) · CSRF Protection</text>

  <!-- Arrow -->
  <path d="M 500 230 L 500 255" stroke="#4A5568" stroke-width="2"/>

  <!-- Controllers -->
  <rect x="50" y="255" width="900" height="70" rx="8" fill="url(#ctrlGrad)" filter="url(#shadow)"/>
  <text x="500" y="278" text-anchor="middle" font-size="15" font-weight="bold" fill="#FFF">Presentation &amp; Controller Tier (Spring MVC)</text>
  <g font-size="12" fill="#E6FFFA" text-anchor="middle">
    <rect x="70" y="288" width="190" height="26" rx="4" fill="#234E52"/>
    <text x="165" y="305">HomeController</text>
    <rect x="290" y="288" width="190" height="26" rx="4" fill="#234E52"/>
    <text x="385" y="305">StudentController</text>
    <rect x="510" y="288" width="190" height="26" rx="4" fill="#234E52"/>
    <text x="605" y="305">FacultyController</text>
    <rect x="730" y="288" width="190" height="26" rx="4" fill="#234E52"/>
    <text x="825" y="305">AdminController</text>
  </g>

  <!-- Arrow -->
  <path d="M 500 325 L 500 350" stroke="#4A5568" stroke-width="2"/>

  <!-- Services -->
  <rect x="50" y="350" width="900" height="70" rx="8" fill="url(#srvGrad)" filter="url(#shadow)"/>
  <text x="500" y="373" text-anchor="middle" font-size="15" font-weight="bold" fill="#FFF">Business Logic &amp; Service Tier (@Transactional)</text>
  <g font-size="11" fill="#FAF5FF" text-anchor="middle">
    <rect x="65" y="383" width="130" height="26" rx="4" fill="#44337A"/><text x="130" y="400">UserService</text>
    <rect x="210" y="383" width="130" height="26" rx="4" fill="#44337A"/><text x="275" y="400">ExamService</text>
    <rect x="355" y="383" width="135" height="26" rx="4" fill="#44337A"/><text x="422" y="400">MarksService</text>
    <rect x="505" y="383" width="155" height="26" rx="4" fill="#44337A"/><text x="582" y="400">RecheckRequestService</text>
    <rect x="675" y="383" width="130" height="26" rx="4" fill="#44337A"/><text x="740" y="400">ReviewService</text>
    <rect x="820" y="383" width="115" height="26" rx="4" fill="#44337A"/><text x="877" y="400">AuditService</text>
  </g>

  <!-- Arrow -->
  <path d="M 500 420 L 500 445" stroke="#4A5568" stroke-width="2"/>

  <!-- Repositories -->
  <rect x="50" y="445" width="900" height="60" rx="8" fill="url(#repoGrad)" filter="url(#shadow)"/>
  <text x="500" y="468" text-anchor="middle" font-size="15" font-weight="bold" fill="#FFF">Data Access Tier (Spring Data JPA &amp; Hibernate 6)</text>
  <text x="500" y="490" text-anchor="middle" font-size="11" fill="#FEFCBF">UserRepository · ExamRepository · QuestionRepository · StudentResultRepository · QuestionMarkRepository · RecheckRequestRepository · ReviewRepository · AuditLogRepository</text>

  <!-- Arrow -->
  <path d="M 500 505 L 500 525" stroke="#4A5568" stroke-width="2"/>

  <!-- Database -->
  <rect x="180" y="525" width="640" height="55" rx="8" fill="url(#dbGrad)" filter="url(#shadow)"/>
  <text x="500" y="548" text-anchor="middle" font-size="15" font-weight="bold" fill="#FFF">Database Tier (ACID Relational Storage)</text>
  <text x="500" y="567" text-anchor="middle" font-size="12" fill="#FED7D7">MySQL 8.0+ (Production) / H2 In-Memory Database (Development &amp; Automated Testing)</text>
</svg>"""
    save_and_convert(svg, "system-architecture")

# 2. Layered Architecture Diagram
def make_layered_architecture():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 550" width="900" height="550" font-family="Arial, sans-serif">
  <defs>
    <filter id="shd" x="-2%" y="-2%" width="104%" height="104%"><feDropShadow dx="2" dy="2" stdDeviation="2" flood-opacity="0.1"/></filter>
  </defs>
  <rect width="900" height="550" fill="#F7FAFC" rx="8"/>
  <text x="450" y="32" text-anchor="middle" font-size="19" font-weight="bold" fill="#2D3748">Layered Enterprise Software Architecture</text>
  <text x="450" y="52" text-anchor="middle" font-size="12" fill="#718096">Separation of Concerns across Presentation, Controller, Service, Persistence, and Storage</text>

  <!-- Layer 1 -->
  <rect x="60" y="70" width="780" height="75" rx="6" fill="#EBF8FF" stroke="#3182CE" stroke-width="2" filter="url(#shd)"/>
  <text x="80" y="95" font-size="15" font-weight="bold" fill="#2B6CB0">1. Presentation Layer (UI &amp; Views)</text>
  <text x="80" y="115" font-size="12" fill="#2C5282">Thymeleaf HTML5 Templates (student/, faculty/, admin/, fragments/, auth/) · Responsive layout.html · Bootstrap Theme CSS</text>
  <text x="80" y="133" font-size="11" fill="#4A5568">Responsibilities: Display exam results, question mark breakdown, dispute forms, status badges, and aggregate analytics.</text>

  <!-- Layer 2 -->
  <rect x="60" y="160" width="780" height="75" rx="6" fill="#E6FFFA" stroke="#319795" stroke-width="2" filter="url(#shd)"/>
  <text x="80" y="185" font-size="15" font-weight="bold" fill="#234E52">2. Web &amp; Controller Layer (HTTP &amp; Security)</text>
  <text x="80" y="205" font-size="12" fill="#285E61">Spring MVC Controllers (@Controller) · SecurityFilterChain · Role-Based Routing · Form Binding &amp; Flash Attributes</text>
  <text x="80" y="223" font-size="11" fill="#4A5568">Responsibilities: Intercept HTTP requests, validate session identity, verify CSRF tokens, map request models, handle 403 access.</text>

  <!-- Layer 3 -->
  <rect x="60" y="250" width="780" height="75" rx="6" fill="#FAF5FF" stroke="#805AD5" stroke-width="2" filter="url(#shd)"/>
  <text x="80" y="275" font-size="15" font-weight="bold" fill="#553C9A">3. Business Logic &amp; Service Layer (Domain Processing)</text>
  <text x="80" y="295" font-size="12" fill="#6B46C1">Spring Services (@Service, @Transactional) · Domain Services (RecheckRequestService, ReviewService, MarksService, AuditService)</text>
  <text x="80" y="313" font-size="11" fill="#4A5568">Responsibilities: Verify recheck periods, duplicate check (ADR-003), compute total marks, apply score revisions, record audit logs.</text>

  <!-- Layer 4 -->
  <rect x="60" y="340" width="780" height="75" rx="6" fill="#FEFCBF" stroke="#D69E2E" stroke-width="2" filter="url(#shd)"/>
  <text x="80" y="365" font-size="15" font-weight="bold" fill="#744210">4. Persistence &amp; Data Access Layer (ORM)</text>
  <text x="80" y="385" font-size="12" fill="#975A16">Spring Data JPA Repositories · Hibernate 6 ORM · @EntityGraph Eager Fetching · Open-in-View Transaction Handling</text>
  <text x="80" y="403" font-size="11" fill="#4A5568">Responsibilities: Abstract SQL generation, prevent N+1 queries, manage entity proxies, enforce unique constraint handling.</text>

  <!-- Layer 5 -->
  <rect x="60" y="430" width="780" height="75" rx="6" fill="#FFF5F5" stroke="#E53E3E" stroke-width="2" filter="url(#shd)"/>
  <text x="80" y="455" font-size="15" font-weight="bold" fill="#9B2C2C">5. Infrastructure &amp; Database Layer (Relational Storage)</text>
  <text x="80" y="475" font-size="12" fill="#C53030">HikariCP Connection Pool · MySQL 8.0 InnoDB (Production) · H2 Database (In-Memory Testing) · Relational Constraints</text>
  <text x="80" y="493" font-size="11" fill="#4A5568">Responsibilities: Provide ACID guarantees, primary/foreign key cascading, index lookups, and unique constraint enforcement.</text>
</svg>"""
    save_and_convert(svg, "layered-architecture")

# 3. UML Use Case Diagram
def make_use_case_diagram():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 620" width="950" height="620" font-family="Arial, sans-serif">
  <rect width="950" height="620" fill="#F8FAFC" rx="8"/>
  <text x="475" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#1A202C">UML Use Case Diagram — Exam Question Re-evaluation System</text>

  <!-- System Boundary -->
  <rect x="250" y="55" width="460" height="540" fill="#FFFFFF" stroke="#4A5568" stroke-width="2" rx="8"/>
  <text x="270" y="80" font-size="13" font-weight="bold" fill="#2B6CB0">Exam Review Portal System Boundary</text>

  <!-- Use cases -->
  <!-- Auth -->
  <ellipse cx="480" cy="110" rx="130" ry="22" fill="#EDF2F7" stroke="#4A5568"/>
  <text x="480" y="115" text-anchor="middle" font-size="12">Authenticate (Login / Logout)</text>

  <!-- Student UCs -->
  <ellipse cx="480" cy="165" rx="140" ry="22" fill="#EBF8FF" stroke="#3182CE"/>
  <text x="480" y="170" text-anchor="middle" font-size="12">View Examination Results</text>

  <ellipse cx="480" cy="220" rx="150" ry="22" fill="#EBF8FF" stroke="#3182CE"/>
  <text x="480" y="225" text-anchor="middle" font-size="12">Inspect Question-Wise Marks</text>

  <ellipse cx="480" cy="275" rx="160" ry="22" fill="#EBF8FF" stroke="#3182CE"/>
  <text x="480" y="280" text-anchor="middle" font-size="12">Submit Re-evaluation Request</text>

  <ellipse cx="480" cy="330" rx="140" ry="22" fill="#EBF8FF" stroke="#3182CE"/>
  <text x="480" y="335" text-anchor="middle" font-size="12">Track Recheck Request Status</text>

  <!-- Faculty UCs -->
  <ellipse cx="480" cy="385" rx="145" ry="22" fill="#E6FFFA" stroke="#319795"/>
  <text x="480" y="390" text-anchor="middle" font-size="12">Create Exam &amp; Configure Questions</text>

  <ellipse cx="480" cy="440" rx="140" ry="22" fill="#E6FFFA" stroke="#319795"/>
  <text x="480" y="445" text-anchor="middle" font-size="12">Review Re-evaluation Requests</text>

  <ellipse cx="480" cy="495" rx="150" ry="22" fill="#E6FFFA" stroke="#319795"/>
  <text x="480" y="500" text-anchor="middle" font-size="12">Amend Marks &amp; Submit Verdict</text>

  <ellipse cx="480" cy="550" rx="140" ry="22" fill="#E6FFFA" stroke="#319795"/>
  <text x="480" y="555" text-anchor="middle" font-size="12">View Question Dispute Analytics</text>

  <!-- Admin UC -->
  <ellipse cx="480" cy="580" rx="130" ry="14" fill="#FAF5FF" stroke="#805AD5"/>
  <text x="480" y="584" text-anchor="middle" font-size="10">Inspect System Audit Logs</text>

  <!-- Student Actor -->
  <g transform="translate(100, 220)">
    <circle cx="20" cy="20" r="16" fill="#EBF8FF" stroke="#2B6CB0" stroke-width="2"/>
    <line x1="20" y1="36" x2="20" y2="80" stroke="#2B6CB0" stroke-width="2"/>
    <line x1="-10" y1="52" x2="50" y2="52" stroke="#2B6CB0" stroke-width="2"/>
    <line x1="20" y1="80" x2="-5" y2="120" stroke="#2B6CB0" stroke-width="2"/>
    <line x1="20" y1="80" x2="45" y2="120" stroke="#2B6CB0" stroke-width="2"/>
    <text x="20" y="145" text-anchor="middle" font-size="14" font-weight="bold" fill="#2B6CB0">Student</text>
  </g>

  <!-- Connect Student to UCs -->
  <line x1="140" y1="250" x2="350" y2="115" stroke="#2B6CB0" stroke-width="1.5"/>
  <line x1="140" y1="260" x2="340" y2="165" stroke="#2B6CB0" stroke-width="1.5"/>
  <line x1="140" y1="270" x2="330" y2="220" stroke="#2B6CB0" stroke-width="1.5"/>
  <line x1="140" y1="280" x2="320" y2="275" stroke="#2B6CB0" stroke-width="1.5"/>
  <line x1="140" y1="290" x2="340" y2="330" stroke="#2B6CB0" stroke-width="1.5"/>

  <!-- Faculty Actor -->
  <g transform="translate(830, 360)">
    <circle cx="20" cy="20" r="16" fill="#E6FFFA" stroke="#234E52" stroke-width="2"/>
    <line x1="20" y1="36" x2="20" y2="80" stroke="#234E52" stroke-width="2"/>
    <line x1="-10" y1="52" x2="50" y2="52" stroke="#234E52" stroke-width="2"/>
    <line x1="20" y1="80" x2="-5" y2="120" stroke="#234E52" stroke-width="2"/>
    <line x1="20" y1="80" x2="45" y2="120" stroke="#234E52" stroke-width="2"/>
    <text x="20" y="145" text-anchor="middle" font-size="14" font-weight="bold" fill="#234E52">Faculty</text>
  </g>

  <!-- Connect Faculty to UCs -->
  <line x1="810" y1="390" x2="610" y2="115" stroke="#234E52" stroke-width="1.5"/>
  <line x1="810" y1="400" x2="625" y2="385" stroke="#234E52" stroke-width="1.5"/>
  <line x1="810" y1="410" x2="620" y2="440" stroke="#234E52" stroke-width="1.5"/>
  <line x1="810" y1="420" x2="630" y2="495" stroke="#234E52" stroke-width="1.5"/>
  <line x1="810" y1="430" x2="620" y2="550" stroke="#234E52" stroke-width="1.5"/>

  <!-- Admin Actor -->
  <g transform="translate(830, 110)">
    <circle cx="20" cy="20" r="16" fill="#FAF5FF" stroke="#553C9A" stroke-width="2"/>
    <line x1="20" y1="36" x2="20" y2="80" stroke="#553C9A" stroke-width="2"/>
    <line x1="-10" y1="52" x2="50" y2="52" stroke="#553C9A" stroke-width="2"/>
    <line x1="20" y1="80" x2="-5" y2="120" stroke="#553C9A" stroke-width="2"/>
    <line x1="20" y1="80" x2="45" y2="120" stroke="#553C9A" stroke-width="2"/>
    <text x="20" y="145" text-anchor="middle" font-size="14" font-weight="bold" fill="#553C9A">Admin</text>
  </g>
  <line x1="810" y1="130" x2="610" y2="115" stroke="#553C9A" stroke-width="1.5"/>
  <line x1="810" y1="160" x2="610" y2="580" stroke="#553C9A" stroke-width="1.5"/>
</svg>"""
    save_and_convert(svg, "use-case-diagram")

# 4. UML Class Diagram
def make_class_diagram():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1050 750" width="1050" height="750" font-family="monospace" font-size="11">
  <rect width="1050" height="750" fill="#F8FAFC" rx="8"/>
  <text x="525" y="28" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#1A202C">UML Class Diagram — Domain Model Entities</text>

  <!-- User Class -->
  <g transform="translate(40, 50)">
    <rect width="210" height="150" fill="#FFF" stroke="#2B6CB0" stroke-width="1.5" rx="4"/>
    <rect width="210" height="28" fill="#2B6CB0" rx="4"/>
    <text x="105" y="19" text-anchor="middle" fill="#FFF" font-weight="bold">User</text>
    <text x="10" y="48" fill="#2D3748">- id: Long</text>
    <text x="10" y="65" fill="#2D3748">- name: String</text>
    <text x="10" y="82" fill="#2D3748">- email: String [UK]</text>
    <text x="10" y="99" fill="#2D3748">- passwordHash: String</text>
    <text x="10" y="116" fill="#2D3748">- role: Role</text>
    <text x="10" y="133" fill="#2D3748">- createdAt: LocalDateTime</text>
  </g>

  <!-- Role Enum -->
  <g transform="translate(40, 230)">
    <rect width="210" height="85" fill="#FFF" stroke="#4A5568" stroke-width="1.5" rx="4"/>
    <rect width="210" height="24" fill="#4A5568" rx="4"/>
    <text x="105" y="17" text-anchor="middle" fill="#FFF" font-weight="bold">&lt;&lt;enum&gt;&gt; Role</text>
    <text x="10" y="44" fill="#2D3748">+ STUDENT</text>
    <text x="10" y="60" fill="#2D3748">+ FACULTY</text>
    <text x="10" y="76" fill="#2D3748">+ ADMIN</text>
  </g>

  <!-- Exam Class -->
  <g transform="translate(380, 50)">
    <rect width="270" height="175" fill="#FFF" stroke="#234E52" stroke-width="1.5" rx="4"/>
    <rect width="270" height="28" fill="#234E52" rx="4"/>
    <text x="135" y="19" text-anchor="middle" fill="#FFF" font-weight="bold">Exam</text>
    <text x="10" y="48" fill="#2D3748">- id: Long</text>
    <text x="10" y="65" fill="#2D3748">- name: String</text>
    <text x="10" y="82" fill="#2D3748">- subject: String</text>
    <text x="10" y="99" fill="#2D3748">- examDate: LocalDate</text>
    <text x="10" y="116" fill="#2D3748">- reevaluationStart: LocalDateTime</text>
    <text x="10" y="133" fill="#2D3748">- reevaluationEnd: LocalDateTime</text>
    <text x="10" y="150" fill="#2D3748">- status: ExamStatus</text>
    <text x="10" y="167" fill="#2D3748">- questions: List&amp;lt;Question&amp;gt;</text>
  </g>

  <!-- Question Class -->
  <g transform="translate(750, 50)">
    <rect width="250" height="150" fill="#FFF" stroke="#553C9A" stroke-width="1.5" rx="4"/>
    <rect width="250" height="28" fill="#553C9A" rx="4"/>
    <text x="125" y="19" text-anchor="middle" fill="#FFF" font-weight="bold">Question</text>
    <text x="10" y="48" fill="#2D3748">- id: Long</text>
    <text x="10" y="65" fill="#2D3748">- exam: Exam</text>
    <text x="10" y="82" fill="#2D3748">- questionNumber: Integer</text>
    <text x="10" y="99" fill="#2D3748">- description: String</text>
    <text x="10" y="116" fill="#2D3748">- maxMarks: Double</text>
    <text x="10" y="133" fill="#2D3748">- createdAt: LocalDateTime</text>
  </g>

  <!-- QuestionMark Class -->
  <g transform="translate(750, 280)">
    <rect width="250" height="135" fill="#FFF" stroke="#B7791F" stroke-width="1.5" rx="4"/>
    <rect width="250" height="28" fill="#B7791F" rx="4"/>
    <text x="125" y="19" text-anchor="middle" fill="#FFF" font-weight="bold">QuestionMark</text>
    <text x="10" y="48" fill="#2D3748">- id: Long</text>
    <text x="10" y="65" fill="#2D3748">- student: User</text>
    <text x="10" y="82" fill="#2D3748">- question: Question</text>
    <text x="10" y="99" fill="#2D3748">- marksObtained: Double</text>
    <text x="10" y="116" fill="#2D3748">- updatedAt: LocalDateTime</text>
  </g>

  <!-- StudentResult Class -->
  <g transform="translate(40, 480)">
    <rect width="230" height="140" fill="#FFF" stroke="#C53030" stroke-width="1.5" rx="4"/>
    <rect width="230" height="28" fill="#C53030" rx="4"/>
    <text x="115" y="19" text-anchor="middle" fill="#FFF" font-weight="bold">StudentResult</text>
    <text x="10" y="48" fill="#2D3748">- id: Long</text>
    <text x="10" y="65" fill="#2D3748">- student: User</text>
    <text x="10" y="82" fill="#2D3748">- exam: Exam</text>
    <text x="10" y="99" fill="#2D3748">- totalMarks: Double</text>
    <text x="10" y="116" fill="#2D3748">- updatedAt: LocalDateTime</text>
  </g>

  <!-- RecheckRequest Class -->
  <g transform="translate(380, 280)">
    <rect width="280" height="185" fill="#FFF" stroke="#2B6CB0" stroke-width="1.5" rx="4"/>
    <rect width="280" height="28" fill="#2B6CB0" rx="4"/>
    <text x="140" y="19" text-anchor="middle" fill="#FFF" font-weight="bold">RecheckRequest</text>
    <text x="10" y="48" fill="#2D3748">- id: Long</text>
    <text x="10" y="65" fill="#2D3748">- student: User</text>
    <text x="10" y="82" fill="#2D3748">- exam: Exam</text>
    <text x="10" y="99" fill="#2D3748">- question: Question</text>
    <text x="10" y="116" fill="#2D3748">- reason: String</text>
    <text x="10" y="133" fill="#2D3748">- status: RequestStatus</text>
    <text x="10" y="150" fill="#2D3748">- reviews: List&amp;lt;Review&amp;gt;</text>
    <text x="10" y="167" fill="#2D3748">- createdAt: LocalDateTime</text>
  </g>

  <!-- Review Class -->
  <g transform="translate(380, 520)">
    <rect width="280" height="170" fill="#FFF" stroke="#234E52" stroke-width="1.5" rx="4"/>
    <rect width="280" height="28" fill="#234E52" rx="4"/>
    <text x="140" y="19" text-anchor="middle" fill="#FFF" font-weight="bold">Review</text>
    <text x="10" y="48" fill="#2D3748">- id: Long</text>
    <text x="10" y="65" fill="#2D3748">- request: RecheckRequest</text>
    <text x="10" y="82" fill="#2D3748">- reviewer: User</text>
    <text x="10" y="99" fill="#2D3748">- decision: ReviewDecision</text>
    <text x="10" y="116" fill="#2D3748">- previousMarks: Double</text>
    <text x="10" y="133" fill="#2D3748">- revisedMarks: Double</text>
    <text x="10" y="150" fill="#2D3748">- remarks: String</text>
    <text x="10" y="167" fill="#2D3748">- reviewedAt: LocalDateTime</text>
  </g>

  <!-- AuditLog Class -->
  <g transform="translate(750, 480)">
    <rect width="250" height="140" fill="#FFF" stroke="#4A5568" stroke-width="1.5" rx="4"/>
    <rect width="250" height="28" fill="#4A5568" rx="4"/>
    <text x="125" y="19" text-anchor="middle" fill="#FFF" font-weight="bold">AuditLog</text>
    <text x="10" y="48" fill="#2D3748">- id: Long</text>
    <text x="10" y="65" fill="#2D3748">- user: User</text>
    <text x="10" y="82" fill="#2D3748">- action: String</text>
    <text x="10" y="99" fill="#2D3748">- details: String</text>
    <text x="10" y="116" fill="#2D3748">- timestamp: LocalDateTime</text>
  </g>

  <!-- Association lines -->
  <!-- Exam 1 to * Question -->
  <line x1="650" y1="110" x2="750" y2="110" stroke="#4A5568" stroke-width="1.5"/>
  <text x="660" y="105">1</text><text x="735" y="105">1..*</text>

  <!-- Question 1 to * QuestionMark -->
  <line x1="875" y1="200" x2="875" y2="280" stroke="#4A5568" stroke-width="1.5"/>
  <text x="880" y="220">1</text><text x="880" y="270">*</text>

  <!-- RecheckRequest 1 to * Review -->
  <line x1="520" y1="465" x2="520" y2="520" stroke="#4A5568" stroke-width="1.5"/>
  <text x="525" y="485">1</text><text x="525" y="510">0..*</text>

  <!-- User 1 to * RecheckRequest -->
  <line x1="250" y1="125" x2="380" y2="350" stroke="#4A5568" stroke-width="1.5"/>
  <text x="260" y="145">1</text><text x="360" y="340">*</text>
</svg>"""
    save_and_convert(svg, "class-diagram")

# 5. Activity Diagram
def make_activity_diagram():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 820" width="850" height="820" font-family="Arial, sans-serif">
  <rect width="850" height="820" fill="#F8FAFC" rx="8"/>
  <text x="425" y="30" text-anchor="middle" font-size="18" font-weight="bold" fill="#1A202C">UML Activity Diagram — Re-evaluation Lifecycle</text>

  <!-- Start node -->
  <circle cx="425" cy="60" r="14" fill="#2B6CB0"/>

  <path d="M 425 74 L 425 105" stroke="#4A5568" stroke-width="2"/>
  
  <!-- Step 1 -->
  <rect x="295" y="105" width="260" height="40" rx="8" fill="#EBF8FF" stroke="#3182CE" stroke-width="1.5"/>
  <text x="425" y="130" text-anchor="middle" font-size="12">Student Inspects Question Breakdown</text>

  <path d="M 425 145 L 425 175" stroke="#4A5568" stroke-width="2"/>

  <!-- Decision 1: Window Open? -->
  <polygon points="425,175 495,205 425,235 355,205" fill="#FEFCBF" stroke="#D69E2E" stroke-width="1.5"/>
  <text x="425" y="210" text-anchor="middle" font-size="11">Re-eval Open?</text>

  <path d="M 495 205 L 670 205 L 670 260" stroke="#E53E3E" stroke-width="1.5"/>
  <text x="560" y="195" font-size="11" fill="#E53E3E">[No]</text>
  <rect x="580" y="260" width="180" height="35" rx="6" fill="#FFF5F5" stroke="#E53E3E"/>
  <text x="670" y="282" text-anchor="middle" font-size="11" fill="#C53030">Window Closed Alert</text>

  <path d="M 425 235 L 425 270" stroke="#4A5568" stroke-width="2"/>
  <text x="435" y="255" font-size="11" fill="#2B6CB0">[Yes]</text>

  <!-- Step 2 -->
  <rect x="295" y="270" width="260" height="40" rx="8" fill="#EBF8FF" stroke="#3182CE" stroke-width="1.5"/>
  <text x="425" y="295" text-anchor="middle" font-size="12">Student Submits Request &amp; Reason</text>

  <path d="M 425 310 L 425 340" stroke="#4A5568" stroke-width="2"/>

  <!-- Decision 2: Duplicate check -->
  <polygon points="425,340 500,370 425,400 350,370" fill="#FEFCBF" stroke="#D69E2E" stroke-width="1.5"/>
  <text x="425" y="374" text-anchor="middle" font-size="11">Duplicate Request?</text>

  <path d="M 500 370 L 670 370 L 670 410" stroke="#E53E3E" stroke-width="1.5"/>
  <text x="560" y="360" font-size="11" fill="#E53E3E">[Yes]</text>
  <rect x="575" y="410" width="190" height="35" rx="6" fill="#FFF5F5" stroke="#E53E3E"/>
  <text x="670" y="432" text-anchor="middle" font-size="11" fill="#C53030">Reject (ADR-003 Violation)</text>

  <path d="M 425 400 L 425 435" stroke="#4A5568" stroke-width="2"/>
  <text x="435" y="420" font-size="11" fill="#2B6CB0">[No]</text>

  <!-- Step 3 -->
  <rect x="290" y="435" width="270" height="40" rx="8" fill="#E6FFFA" stroke="#319795" stroke-width="1.5"/>
  <text x="425" y="460" text-anchor="middle" font-size="12">Store Request (Status: SUBMITTED)</text>

  <path d="M 425 475 L 425 505" stroke="#4A5568" stroke-width="2"/>

  <!-- Step 4 -->
  <rect x="280" y="505" width="290" height="40" rx="8" fill="#FAF5FF" stroke="#805AD5" stroke-width="1.5"/>
  <text x="425" y="530" text-anchor="middle" font-size="12">Faculty Opens &amp; Reviews (UNDER_REVIEW)</text>

  <path d="M 425 545 L 425 575" stroke="#4A5568" stroke-width="2"/>

  <!-- Decision 3: Verdict -->
  <polygon points="425,575 495,605 425,635 355,605" fill="#FEFCBF" stroke="#D69E2E" stroke-width="1.5"/>
  <text x="425" y="610" text-anchor="middle" font-size="11">Approve?</text>

  <!-- Left: Approved -->
  <path d="M 355 605 L 230 605 L 230 645" stroke="#2B6CB0" stroke-width="1.5"/>
  <text x="280" y="595" font-size="11" fill="#2B6CB0">[Approved]</text>
  <rect x="110" y="645" width="240" height="45" rx="6" fill="#EBF8FF" stroke="#3182CE"/>
  <text x="230" y="665" text-anchor="middle" font-size="11">Amend Question Marks</text>
  <text x="230" y="680" text-anchor="middle" font-size="10" fill="#4A5568">Recalculate Student Total</text>

  <!-- Right: Rejected -->
  <path d="M 495 605 L 610 605 L 610 645" stroke="#C53030" stroke-width="1.5"/>
  <text x="540" y="595" font-size="11" fill="#C53030">[Rejected]</text>
  <rect x="510" y="645" width="200" height="45" rx="6" fill="#FFF5F5" stroke="#E53E3E"/>
  <text x="610" y="665" text-anchor="middle" font-size="11">Keep Marks Unchanged</text>
  <text x="610" y="680" text-anchor="middle" font-size="10" fill="#4A5568">Record Justification</text>

  <!-- Join -->
  <path d="M 230 690 L 230 720 L 425 720" stroke="#4A5568" stroke-width="1.5"/>
  <path d="M 610 690 L 610 720 L 425 720" stroke="#4A5568" stroke-width="1.5"/>
  <path d="M 425 720 L 425 745" stroke="#4A5568" stroke-width="2"/>

  <!-- Step 5 -->
  <rect x="300" y="745" width="250" height="35" rx="6" fill="#EDF2F7" stroke="#4A5568"/>
  <text x="425" y="767" text-anchor="middle" font-size="11">Record Immutable Audit Log</text>

  <path d="M 425 780 L 425 800" stroke="#4A5568" stroke-width="2"/>
  <circle cx="425" cy="808" r="8" fill="#1A202C"/>
  <circle cx="425" cy="808" r="12" fill="none" stroke="#1A202C" stroke-width="1.5"/>
</svg>"""
    save_and_convert(svg, "activity-diagram")

# 6. ER Diagram
def make_er_diagram():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 650" width="1000" height="650" font-family="monospace" font-size="11">
  <rect width="1000" height="650" fill="#F8FAFC" rx="8"/>
  <text x="500" y="28" text-anchor="middle" font-family="Arial, sans-serif" font-size="18" font-weight="bold" fill="#1A202C">Entity Relationship (ER) Diagram</text>

  <!-- users -->
  <g transform="translate(50, 60)">
    <rect width="200" height="135" fill="#FFF" stroke="#2B6CB0" stroke-width="1.5" rx="4"/>
    <rect width="200" height="24" fill="#2B6CB0" rx="4"/>
    <text x="100" y="17" text-anchor="middle" fill="#FFF" font-weight="bold">users</text>
    <text x="8" y="42" fill="#2D3748">PK  id : BIGINT</text>
    <text x="8" y="58" fill="#2D3748">    name : VARCHAR</text>
    <text x="8" y="74" fill="#2D3748">UQ  email : VARCHAR</text>
    <text x="8" y="90" fill="#2D3748">    password_hash : VARCHAR</text>
    <text x="8" y="106" fill="#2D3748">    role : VARCHAR</text>
    <text x="8" y="122" fill="#2D3748">    created_at : DATETIME</text>
  </g>

  <!-- exams -->
  <g transform="translate(400, 60)">
    <rect width="220" height="150" fill="#FFF" stroke="#234E52" stroke-width="1.5" rx="4"/>
    <rect width="220" height="24" fill="#234E52" rx="4"/>
    <text x="110" y="17" text-anchor="middle" fill="#FFF" font-weight="bold">exams</text>
    <text x="8" y="42" fill="#2D3748">PK  id : BIGINT</text>
    <text x="8" y="58" fill="#2D3748">    name : VARCHAR</text>
    <text x="8" y="74" fill="#2D3748">    subject : VARCHAR</text>
    <text x="8" y="90" fill="#2D3748">    exam_date : DATE</text>
    <text x="8" y="106" fill="#2D3748">    reeval_start : DATETIME</text>
    <text x="8" y="122" fill="#2D3748">    reeval_end : DATETIME</text>
    <text x="8" y="138" fill="#2D3748">    status : VARCHAR</text>
  </g>

  <!-- questions -->
  <g transform="translate(730, 60)">
    <rect width="220" height="120" fill="#FFF" stroke="#553C9A" stroke-width="1.5" rx="4"/>
    <rect width="220" height="24" fill="#553C9A" rx="4"/>
    <text x="110" y="17" text-anchor="middle" fill="#FFF" font-weight="bold">questions</text>
    <text x="8" y="42" fill="#2D3748">PK  id : BIGINT</text>
    <text x="8" y="58" fill="#2D3748">FK  exam_id : BIGINT</text>
    <text x="8" y="74" fill="#2D3748">    question_number : INT</text>
    <text x="8" y="90" fill="#2D3748">    description : TEXT</text>
    <text x="8" y="106" fill="#2D3748">    max_marks : DOUBLE</text>
  </g>

  <!-- student_results -->
  <g transform="translate(50, 260)">
    <rect width="200" height="110" fill="#FFF" stroke="#C53030" stroke-width="1.5" rx="4"/>
    <rect width="200" height="24" fill="#C53030" rx="4"/>
    <text x="100" y="17" text-anchor="middle" fill="#FFF" font-weight="bold">student_results</text>
    <text x="8" y="42" fill="#2D3748">PK  id : BIGINT</text>
    <text x="8" y="58" fill="#2D3748">FK  student_id : BIGINT</text>
    <text x="8" y="74" fill="#2D3748">FK  exam_id : BIGINT</text>
    <text x="8" y="90" fill="#2D3748">    total_marks : DOUBLE</text>
    <text x="8" y="104" fill="#2D3748">UQ (student_id, exam_id)</text>
  </g>

  <!-- recheck_requests -->
  <g transform="translate(380, 260)">
    <rect width="260" height="150" fill="#FFF" stroke="#2B6CB0" stroke-width="1.5" rx="4"/>
    <rect width="260" height="24" fill="#2B6CB0" rx="4"/>
    <text x="130" y="17" text-anchor="middle" fill="#FFF" font-weight="bold">recheck_requests</text>
    <text x="8" y="42" fill="#2D3748">PK  id : BIGINT</text>
    <text x="8" y="58" fill="#2D3748">FK  student_id : BIGINT</text>
    <text x="8" y="74" fill="#2D3748">FK  exam_id : BIGINT</text>
    <text x="8" y="90" fill="#2D3748">FK  question_id : BIGINT</text>
    <text x="8" y="106" fill="#2D3748">    reason : TEXT</text>
    <text x="8" y="122" fill="#2D3748">    status : VARCHAR</text>
    <text x="8" y="138" fill="#B7791F">UQ(student, exam, question)</text>
  </g>

  <!-- question_marks -->
  <g transform="translate(730, 260)">
    <rect width="220" height="110" fill="#FFF" stroke="#B7791F" stroke-width="1.5" rx="4"/>
    <rect width="220" height="24" fill="#B7791F" rx="4"/>
    <text x="110" y="17" text-anchor="middle" fill="#FFF" font-weight="bold">question_marks</text>
    <text x="8" y="42" fill="#2D3748">PK  id : BIGINT</text>
    <text x="8" y="58" fill="#2D3748">FK  student_id : BIGINT</text>
    <text x="8" y="74" fill="#2D3748">FK  question_id : BIGINT</text>
    <text x="8" y="90" fill="#2D3748">    marks_obtained : DOUBLE</text>
    <text x="8" y="104" fill="#2D3748">UQ (student_id, question_id)</text>
  </g>

  <!-- reviews -->
  <g transform="translate(380, 470)">
    <rect width="260" height="150" fill="#FFF" stroke="#234E52" stroke-width="1.5" rx="4"/>
    <rect width="260" height="24" fill="#234E52" rx="4"/>
    <text x="130" y="17" text-anchor="middle" fill="#FFF" font-weight="bold">reviews</text>
    <text x="8" y="42" fill="#2D3748">PK  id : BIGINT</text>
    <text x="8" y="58" fill="#2D3748">FK  request_id : BIGINT</text>
    <text x="8" y="74" fill="#2D3748">FK  reviewer_id : BIGINT</text>
    <text x="8" y="90" fill="#2D3748">    decision : VARCHAR</text>
    <text x="8" y="106" fill="#2D3748">    previous_marks : DOUBLE</text>
    <text x="8" y="122" fill="#2D3748">    revised_marks : DOUBLE</text>
    <text x="8" y="138" fill="#2D3748">    remarks : TEXT</text>
  </g>

  <!-- audit_logs -->
  <g transform="translate(730, 470)">
    <rect width="220" height="120" fill="#FFF" stroke="#4A5568" stroke-width="1.5" rx="4"/>
    <rect width="220" height="24" fill="#4A5568" rx="4"/>
    <text x="110" y="17" text-anchor="middle" fill="#FFF" font-weight="bold">audit_logs</text>
    <text x="8" y="42" fill="#2D3748">PK  id : BIGINT</text>
    <text x="8" y="58" fill="#2D3748">FK  user_id : BIGINT</text>
    <text x="8" y="74" fill="#2D3748">    action : VARCHAR</text>
    <text x="8" y="90" fill="#2D3748">    details : TEXT</text>
    <text x="8" y="106" fill="#2D3748">    timestamp : DATETIME</text>
  </g>

  <!-- Foreign key relationship paths -->
  <line x1="620" y1="120" x2="730" y2="120" stroke="#4A5568" stroke-width="1.5"/>
  <line x1="840" y1="180" x2="840" y2="260" stroke="#4A5568" stroke-width="1.5"/>
  <line x1="510" y1="410" x2="510" y2="470" stroke="#4A5568" stroke-width="1.5"/>
</svg>"""
    save_and_convert(svg, "er-diagram")

# 7. Sequence Diagram: Submission
def make_seq_submission():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 560" width="950" height="560" font-family="Arial, sans-serif">
  <rect width="950" height="560" fill="#F8FAFC" rx="8"/>
  <text x="475" y="28" text-anchor="middle" font-size="17" font-weight="bold" fill="#1A202C">Sequence Diagram: Student Re-evaluation Request Submission</text>

  <!-- Lifeline headers -->
  <g font-size="12" font-weight="bold" fill="#FFF" text-anchor="middle">
    <rect x="30" y="55" width="120" height="30" rx="4" fill="#2B6CB0"/><text x="90" y="75">Student</text>
    <rect x="180" y="55" width="140" height="30" rx="4" fill="#2B6CB0"/><text x="250" y="75">StudentController</text>
    <rect x="350" y="55" width="170" height="30" rx="4" fill="#234E52"/><text x="435" y="75">RecheckRequestService</text>
    <rect x="550" y="55" width="150" height="30" rx="4" fill="#B7791F"/><text x="625" y="75">RequestRepository</text>
    <rect x="730" y="55" width="120" height="30" rx="4" fill="#4A5568"/><text x="790" y="75">AuditService</text>
  </g>

  <!-- Lifelines -->
  <line x1="90" y1="85" x2="90" y2="520" stroke="#A0AEC0" stroke-dasharray="4"/>
  <line x1="250" y1="85" x2="250" y2="520" stroke="#A0AEC0" stroke-dasharray="4"/>
  <line x1="435" y1="85" x2="435" y2="520" stroke="#A0AEC0" stroke-dasharray="4"/>
  <line x1="625" y1="85" x2="625" y2="520" stroke="#A0AEC0" stroke-dasharray="4"/>
  <line x1="790" y1="85" x2="790" y2="520" stroke="#A0AEC0" stroke-dasharray="4"/>

  <!-- Messages -->
  <line x1="90" y1="120" x2="250" y2="120" stroke="#2B6CB0" stroke-width="1.5"/>
  <text x="100" y="112" font-size="11" fill="#2B6CB0">POST /student/exams/{eId}/recheck/{qId} (reason)</text>

  <line x1="250" y1="150" x2="435" y2="150" stroke="#234E52" stroke-width="1.5"/>
  <text x="260" y="142" font-size="11" fill="#234E52">submitRequest(student, examId, questionId, reason)</text>

  <!-- Self call check window -->
  <path d="M 435 175 L 475 175 L 475 195 L 435 195" fill="none" stroke="#234E52" stroke-width="1.5"/>
  <text x="480" y="190" font-size="10" fill="#234E52">verifyWindowOpen()</text>

  <!-- Query duplicate -->
  <line x1="435" y1="230" x2="625" y2="230" stroke="#B7791F" stroke-width="1.5"/>
  <text x="445" y="222" font-size="11" fill="#B7791F">existsByStudentIdAndExamIdAndQuestionId()</text>

  <line x1="625" y1="260" x2="435" y2="260" stroke="#B7791F" stroke-width="1.5" stroke-dasharray="3"/>
  <text x="475" y="254" font-size="11" fill="#718096">false (no duplicate found)</text>

  <!-- Save request -->
  <line x1="435" y1="300" x2="625" y2="300" stroke="#B7791F" stroke-width="1.5"/>
  <text x="445" y="292" font-size="11" fill="#B7791F">saveAndFlush(new RecheckRequest(...))</text>

  <line x1="625" y1="330" x2="435" y2="330" stroke="#B7791F" stroke-width="1.5" stroke-dasharray="3"/>
  <text x="485" y="324" font-size="11" fill="#718096">savedRequest (Status: SUBMITTED)</text>

  <!-- Log audit -->
  <line x1="435" y1="370" x2="790" y2="370" stroke="#4A5568" stroke-width="1.5"/>
  <text x="450" y="362" font-size="11" fill="#4A5568">log(student, "REQUEST_SUBMITTED", details)</text>

  <line x1="435" y1="410" x2="250" y2="410" stroke="#234E52" stroke-width="1.5" stroke-dasharray="3"/>
  <text x="280" y="402" font-size="11" fill="#234E52">return savedRequest</text>

  <line x1="250" y1="450" x2="90" y2="450" stroke="#2B6CB0" stroke-width="1.5" stroke-dasharray="3"/>
  <text x="100" y="442" font-size="11" fill="#2B6CB0">Redirect /student/requests + flash: "Submitted successfully"</text>
</svg>"""
    save_and_convert(svg, "sequence-diagram-submission")

# 8. Sequence Diagram: Review
def make_seq_review():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 950 560" width="950" height="560" font-family="Arial, sans-serif">
  <rect width="950" height="560" fill="#F8FAFC" rx="8"/>
  <text x="475" y="28" text-anchor="middle" font-size="17" font-weight="bold" fill="#1A202C">Sequence Diagram: Faculty Review and Mark Revision</text>

  <!-- Lifeline headers -->
  <g font-size="12" font-weight="bold" fill="#FFF" text-anchor="middle">
    <rect x="30" y="55" width="120" height="30" rx="4" fill="#234E52"/><text x="90" y="75">Faculty</text>
    <rect x="180" y="55" width="140" height="30" rx="4" fill="#234E52"/><text x="250" y="75">FacultyController</text>
    <rect x="360" y="55" width="130" height="30" rx="4" fill="#553C9A"/><text x="425" y="75">ReviewService</text>
    <rect x="530" y="55" width="130" height="30" rx="4" fill="#B7791F"/><text x="595" y="75">MarksService</text>
    <rect x="700" y="55" width="130" height="30" rx="4" fill="#2B6CB0"/><text x="765" y="75">Repositories</text>
    <rect x="850" y="55" width="90" height="30" rx="4" fill="#4A5568"/><text x="895" y="75">Audit</text>
  </g>

  <!-- Lifelines -->
  <line x1="90" y1="85" x2="90" y2="520" stroke="#A0AEC0" stroke-dasharray="4"/>
  <line x1="250" y1="85" x2="250" y2="520" stroke="#A0AEC0" stroke-dasharray="4"/>
  <line x1="425" y1="85" x2="425" y2="520" stroke="#A0AEC0" stroke-dasharray="4"/>
  <line x1="595" y1="85" x2="595" y2="520" stroke="#A0AEC0" stroke-dasharray="4"/>
  <line x1="765" y1="85" x2="765" y2="520" stroke="#A0AEC0" stroke-dasharray="4"/>
  <line x1="895" y1="85" x2="895" y2="520" stroke="#A0AEC0" stroke-dasharray="4"/>

  <!-- Messages -->
  <line x1="90" y1="120" x2="250" y2="120" stroke="#234E52" stroke-width="1.5"/>
  <text x="100" y="112" font-size="11" fill="#234E52">POST /faculty/requests/{id}/review (APPROVED, revisedMarks=7.0)</text>

  <line x1="250" y1="150" x2="425" y2="150" stroke="#553C9A" stroke-width="1.5"/>
  <text x="260" y="142" font-size="11" fill="#553C9A">submitReview(requestId, faculty, APPROVED, 7.0, remarks)</text>

  <line x1="425" y1="180" x2="765" y2="180" stroke="#2B6CB0" stroke-width="1.5"/>
  <text x="440" y="172" font-size="11" fill="#2B6CB0">recheckRequestRepository.findById(requestId)</text>

  <line x1="765" y1="210" x2="425" y2="210" stroke="#2B6CB0" stroke-width="1.5" stroke-dasharray="3"/>
  <text x="460" y="204" font-size="11" fill="#718096">return request</text>

  <!-- Delegate to MarksService -->
  <line x1="425" y1="250" x2="595" y2="250" stroke="#B7791F" stroke-width="1.5"/>
  <text x="440" y="242" font-size="11" fill="#B7791F">recordMark(student, question, 7.0)</text>

  <!-- MarksService updates DB and rolls up total -->
  <line x1="595" y1="280" x2="765" y2="280" stroke="#B7791F" stroke-width="1.5"/>
  <text x="605" y="272" font-size="11" fill="#B7791F">save QuestionMark &amp; recalc StudentResult.totalMarks</text>

  <line x1="765" y1="310" x2="595" y2="310" stroke="#B7791F" stroke-width="1.5" stroke-dasharray="3"/>
  <text x="640" y="304" font-size="11" fill="#718096">updated marks saved</text>

  <!-- Save Review -->
  <line x1="425" y1="350" x2="765" y2="350" stroke="#2B6CB0" stroke-width="1.5"/>
  <text x="440" y="342" font-size="11" fill="#2B6CB0">reviewRepository.save(new Review(...))</text>

  <!-- Log Audit -->
  <line x1="425" y1="390" x2="895" y2="390" stroke="#4A5568" stroke-width="1.5"/>
  <text x="450" y="382" font-size="11" fill="#4A5568">auditService.log(faculty, "REVIEW_COMPLETED", details)</text>

  <line x1="425" y1="430" x2="250" y2="430" stroke="#553C9A" stroke-width="1.5" stroke-dasharray="3"/>
  <text x="270" y="422" font-size="11" fill="#553C9A">return saved Review</text>

  <line x1="250" y1="470" x2="90" y2="470" stroke="#234E52" stroke-width="1.5" stroke-dasharray="3"/>
  <text x="100" y="462" font-size="11" fill="#234E52">Redirect /faculty/requests + flash: "Review completed successfully"</text>
</svg>"""
    save_and_convert(svg, "sequence-diagram-review")

# 9. Exam Lifecycle State Diagram
def make_exam_state():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 320" width="900" height="320" font-family="Arial, sans-serif">
  <rect width="900" height="320" fill="#F8FAFC" rx="8"/>
  <text x="450" y="30" text-anchor="middle" font-size="17" font-weight="bold" fill="#1A202C">Examination Lifecycle State Diagram</text>

  <!-- Start -->
  <circle cx="50" cy="140" r="14" fill="#2B6CB0"/>
  <line x1="64" y1="140" x2="110" y2="140" stroke="#4A5568" stroke-width="2"/>

  <!-- DRAFT -->
  <rect x="110" y="115" width="110" height="50" rx="8" fill="#EDF2F7" stroke="#4A5568" stroke-width="2"/>
  <text x="165" y="145" text-anchor="middle" font-weight="bold">DRAFT</text>

  <line x1="220" y1="140" x2="280" y2="140" stroke="#4A5568" stroke-width="2"/>
  <text x="250" y="130" text-anchor="middle" font-size="10" fill="#4A5568">Publish</text>

  <!-- PUBLISHED -->
  <rect x="280" y="115" width="125" height="50" rx="8" fill="#EBF8FF" stroke="#3182CE" stroke-width="2"/>
  <text x="342" y="145" text-anchor="middle" font-weight="bold" fill="#2B6CB0">PUBLISHED</text>

  <line x1="405" y1="140" x2="475" y2="140" stroke="#4A5568" stroke-width="2"/>
  <text x="440" y="130" text-anchor="middle" font-size="10" fill="#4A5568">Window Opens</text>

  <!-- RE_EVALUATION_OPEN -->
  <rect x="475" y="110" width="170" height="60" rx="8" fill="#E6FFFA" stroke="#319795" stroke-width="2"/>
  <text x="560" y="137" text-anchor="middle" font-weight="bold" fill="#234E52">RE_EVALUATION</text>
  <text x="560" y="155" text-anchor="middle" font-weight="bold" fill="#234E52">_OPEN</text>

  <line x1="645" y1="140" x2="710" y2="140" stroke="#4A5568" stroke-width="2"/>
  <text x="677" y="130" text-anchor="middle" font-size="10" fill="#4A5568">Window Closes</text>

  <!-- RE_EVALUATION_CLOSED -->
  <rect x="710" y="110" width="160" height="60" rx="8" fill="#FFF5F5" stroke="#E53E3E" stroke-width="2"/>
  <text x="790" y="137" text-anchor="middle" font-weight="bold" fill="#9B2C2C">RE_EVALUATION</text>
  <text x="790" y="155" text-anchor="middle" font-weight="bold" fill="#9B2C2C">_CLOSED</text>

  <!-- Transition to ARCHIVED below -->
  <path d="M 790 170 L 790 230 L 400 230" fill="none" stroke="#4A5568" stroke-width="2"/>
  <text x="600" y="222" font-size="10" fill="#4A5568">Semester Concludes</text>

  <!-- ARCHIVED -->
  <rect x="290" y="205" width="110" height="50" rx="8" fill="#EDF2F7" stroke="#718096" stroke-width="2"/>
  <text x="345" y="235" text-anchor="middle" font-weight="bold" fill="#4A5568">ARCHIVED</text>

  <line x1="290" y1="230" x2="230" y2="230" stroke="#4A5568" stroke-width="2"/>
  <circle cx="215" cy="230" r="8" fill="#1A202C"/>
  <circle cx="215" cy="230" r="12" fill="none" stroke="#1A202C" stroke-width="1.5"/>
</svg>"""
    save_and_convert(svg, "exam-state-diagram")

# 10. Request Lifecycle State Diagram
def make_request_state():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 320" width="900" height="320" font-family="Arial, sans-serif">
  <rect width="900" height="320" fill="#F8FAFC" rx="8"/>
  <text x="450" y="30" text-anchor="middle" font-size="17" font-weight="bold" fill="#1A202C">Re-evaluation Request Lifecycle State Diagram</text>

  <!-- Start -->
  <circle cx="60" cy="140" r="14" fill="#2B6CB0"/>
  <line x1="74" y1="140" x2="130" y2="140" stroke="#4A5568" stroke-width="2"/>
  <text x="100" y="130" font-size="10" fill="#4A5568">Submit</text>

  <!-- SUBMITTED -->
  <rect x="130" y="115" width="130" height="50" rx="8" fill="#EBF8FF" stroke="#3182CE" stroke-width="2"/>
  <text x="195" y="145" text-anchor="middle" font-weight="bold" fill="#2B6CB0">SUBMITTED</text>

  <line x1="260" y1="140" x2="350" y2="140" stroke="#4A5568" stroke-width="2"/>
  <text x="305" y="130" text-anchor="middle" font-size="10" fill="#4A5568">Faculty Opens</text>

  <!-- UNDER_REVIEW -->
  <rect x="350" y="115" width="150" height="50" rx="8" fill="#FEFCBF" stroke="#D69E2E" stroke-width="2"/>
  <text x="425" y="145" text-anchor="middle" font-weight="bold" fill="#744210">UNDER_REVIEW</text>

  <!-- Branches -->
  <!-- Top: APPROVED -->
  <path d="M 500 130 L 570 90 L 610 90" fill="none" stroke="#2B6CB0" stroke-width="2"/>
  <text x="545" y="85" font-size="10" fill="#2B6CB0">Approved</text>
  <rect x="610" y="65" width="120" height="50" rx="8" fill="#E6FFFA" stroke="#319795" stroke-width="2"/>
  <text x="670" y="95" text-anchor="middle" font-weight="bold" fill="#234E52">APPROVED</text>

  <!-- Bottom: REJECTED -->
  <path d="M 500 150 L 570 190 L 610 190" fill="none" stroke="#C53030" stroke-width="2"/>
  <text x="545" y="200" font-size="10" fill="#C53030">Rejected</text>
  <rect x="610" y="165" width="120" height="50" rx="8" fill="#FFF5F5" stroke="#E53E3E" stroke-width="2"/>
  <text x="670" y="195" text-anchor="middle" font-weight="bold" fill="#9B2C2C">REJECTED</text>

  <!-- Join to COMPLETED -->
  <path d="M 730 90 L 780 140" fill="none" stroke="#4A5568" stroke-width="2"/>
  <path d="M 730 190 L 780 140" fill="none" stroke="#4A5568" stroke-width="2"/>

  <!-- COMPLETED -->
  <rect x="760" y="115" width="110" height="50" rx="8" fill="#EDF2F7" stroke="#4A5568" stroke-width="2"/>
  <text x="815" y="145" text-anchor="middle" font-weight="bold" fill="#1A202C">COMPLETED</text>
</svg>"""
    save_and_convert(svg, "request-state-diagram")

if __name__ == '__main__':
    print("Generating system design & UML diagrams...")
    make_system_architecture()
    make_layered_architecture()
    make_use_case_diagram()
    make_class_diagram()
    make_activity_diagram()
    make_er_diagram()
    make_seq_submission()
    make_seq_review()
    make_exam_state()
    make_request_state()
    print("All diagrams generated successfully!")
