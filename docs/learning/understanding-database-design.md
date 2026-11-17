# Understanding Database Design & Normalization
## Relational Design Insights for Academic Systems

### 1. Database Normalization (3NF)
The schema is normalized to **Third Normal Form (3NF)**:
1. **1NF (First Normal Form)**:
   - All attributes contain atomic values (no comma-separated lists of marks or questions).
   - Each row has a unique primary key (`id`).
2. **2NF (Second Normal Form)**:
   - All non-key columns depend on the entire primary key. In `question_marks`, each mark entry depends strictly on the foreign keys `student_id` and `question_id`.
3. **3NF (Third Normal Form)**:
   - No transitive dependencies. Student personal details live in `users`, exam definitions in `exams`, and question texts in `questions`. `question_marks` does not duplicate the question text or the student's email.

---

### 2. Controlled Redundancy: Total Marks in `student_results`
You may notice that `student_results` stores `total_marks`, which is the sum of `question_marks.marks_obtained`.
- **Why is this stored?**
  Calculating the sum across all questions for hundreds of students during high-traffic dashboard views causes repeated expensive table scans.
- **How is consistency maintained?**
  Whenever marks are initially entered or revised via review approval, `MarksService` recalculates and updates `StudentResult.totalMarks` within the **exact same ACID transaction**. This gives $O(1)$ read performance with guaranteed consistency.
