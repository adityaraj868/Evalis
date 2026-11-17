# UI Theme & Design System

## Product Character

The application should look like a modern university academic administration system.

Desired qualities:
- Professional
- Trustworthy
- Clean
- Structured
- Calm
- Easy to scan

Avoid making it look like a generic CRUD tutorial.

## Visual Language

Use a restrained enterprise/academic design.

### Color Tokens

Define reusable CSS variables:

```css
--color-primary
--color-primary-hover
--color-background
--color-surface
--color-text
--color-muted
--color-border
--color-success
--color-warning
--color-danger
```

Use semantic colors consistently.

Do not use gradients as the primary visual treatment.

## Typography

Use a modern system sans-serif stack.

Hierarchy:
- Page title
- Section title
- Card title
- Body
- Metadata/helper text

Keep text readable rather than oversized.

## Application Shell

### Student

```text
┌───────────────────────────────────────────┐
│ Exam Review Portal       Student  Logout  │
├───────────────────────────────────────────┤
│ Dashboard                                 │
│ Exams                                     │
│ My Requests                               │
│                                           │
│ Main Content                              │
└───────────────────────────────────────────┘
```

### Faculty/Admin

```text
┌───────────────────────────────────────────┐
│ Exam Review Portal       Faculty  Logout  │
├──────────────┬────────────────────────────┤
│ Dashboard    │                            │
│ Exams        │ Main Content               │
│ Questions    │                            │
│ Marks        │                            │
│ Requests     │                            │
│ Analytics    │                            │
│ Audit Logs   │                            │
└──────────────┴────────────────────────────┘
```

## Status Badges

Use text + visual treatment.

Request statuses:
- SUBMITTED
- UNDER REVIEW
- APPROVED
- REJECTED
- COMPLETED

Exam states:
- DRAFT
- PUBLISHED
- RE-EVALUATION OPEN
- RE-EVALUATION CLOSED
- ARCHIVED

Never rely on color alone to communicate state.

## Student Marks UI

Present question-wise marks clearly:

```text
Question   Marks       Review
Q1         8 / 10      —
Q2         3 / 10      Request Review
Q3         9 / 10      —
Q4         2 / 10      Request Review
```

Once a request exists, replace the action with its status.

## Request Form

The form should clearly show:
- Exam
- Question
- Current marks
- Maximum marks
- Reason textarea
- Submit action

The user should understand that they are requesting review of a specific question, not the entire examination.

## Confirmation

Before submitting a request:

> Confirm Re-evaluation Request

Show the selected question and current marks.

Make clear that duplicate requests are not allowed.

## Faculty Analytics

Prioritize:
1. Pending reviews
2. High-request questions
3. Request counts
4. Flagged questions
5. Decision distribution

Use charts only when they communicate something useful.

## Tables

Use tables for:
- Examinations
- Questions
- Students
- Requests
- Reviews
- Audit logs

Tables need clear headers, consistent spacing, and useful empty states.

## Forms

Every form must:
- Have visible labels.
- Show server-side validation errors.
- Preserve safe entered data after validation failure.
- Identify required fields.
- Prevent impossible actions.

## Accessibility

Use:
- Semantic HTML
- Keyboard navigation
- Visible focus states
- Proper labels
- Accessible error messages
- Alt text for meaningful images
- Sufficient contrast
- Non-color status communication

## Responsive Behavior

On small screens:
- Sidebar collapses.
- Tables become horizontally scrollable or card-based.
- Forms stack.
- Buttons remain usable.

## Antigravity UI Rule

All pages must share the same visual system. Do not invent a new design for each page. Reuse layout fragments, buttons, cards, tables, forms, badges, and CSS variables.
