# Design Doctor

## Purpose
Analyze cabinet designs for common mistakes and issues.

---

## Pencil Prompt

```
Design a design analysis interface for KerfOS that checks for common mistakes.

Layout:
- Left panel: Issue list
  - Severity indicators (Critical, Warning, Info)
  - Issue category icons
  - Affected component name
  - Quick description
  - Click to highlight in design

- Center: Design preview
  - 3D view with highlighted problem areas
  - Red outline for critical issues
  - Yellow outline for warnings
  - Blue outline for suggestions
  - Click on highlight to see details

- Right panel: Issue details
  - Issue title and severity badge
  - Detailed explanation
  - Why it's a problem
  - Suggested fix with step-by-step
  - "Auto-fix" button (if available)
  - "Ignore" button with reason dropdown
  - "Learn more" link to documentation

- Top summary bar:
  - Total issues count
  - By severity breakdown
  - "Fix All" button
  - Export report button

- Bottom progress:
  - Issues fixed counter
  - Remaining issues
  - Overall design health score (0-100)

Style: IDE error panel meets medical interface
Severity: Use clear color coding and icons
Auto-fix: Show before/after preview
```

---

## Design Tokens Used

- Critical: #DC2626
- Warning: #D97706
- Info: #3B82F6
- Success: #10B981

---

## Components

- Issue list panel
- Design preview
- Issue details panel
- Severity badges
- Health score
- Auto-fix button

---

## Interactions

- Click issue to highlight
- Auto-fix action
- Ignore issue
- Fix all
- Export report
