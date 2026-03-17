# Cost Optimizer / "Best Bang for Your Buck"

## Purpose
Analyze and optimize project costs with alternative suggestions.

---

## Pencil Prompt

```
Design a cost optimization report interface for KerfOS.

Layout:
- Top summary card:
  - Current total cost
  - Potential savings amount (highlighted in green)
  - Percentage savings possible
  - "Apply All Suggestions" button

- Main area: Optimization suggestions
  - Grouped by category (Materials, Hardware, Alternatives)
  - Each suggestion card:
    - Current item vs suggested alternative
    - Price comparison (old vs new)
    - Quality impact rating (None, Minor, Moderate)
    - Pros and cons bullet list
    - "Apply" button
    - "Dismiss" button

- Right sidebar: Impact preview
  - Updated cost breakdown chart
  - Quality score impact
  - Project timeline impact

- Bulk purchasing suggestions:
  - "Buy these items together" sections
  - Bundle savings amount
  - Supplier recommendation

- Bottom actions:
  - Export optimization report
  - Create shopping list
  - Share with team

Style: Financial dashboard with clear savings highlights
Charts: Bar charts for cost comparison, donut for breakdown
Suggestions: Cards with clear accept/reject actions
```

---

## Design Tokens Used

- Savings: #10B981 (green)
- Cost: #DC2626 (red for high costs)
- Neutral: #6B7280
- Primary: #2563EB

---

## Components

- Summary card
- Suggestion cards
- Cost comparison chart
- Impact preview
- Apply/dismiss buttons

---

## Interactions

- Apply individual suggestion
- Dismiss suggestion
- Apply all suggestions
- Export report
- Create shopping list
