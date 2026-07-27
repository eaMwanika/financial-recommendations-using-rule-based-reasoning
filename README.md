# Personal Finance Advisor — Rule-Based Reasoning System

APT 3020 (Knowledge-Based Systems) coursework. A knowledge-based expert
system that gives personal finance recommendations across five domains —
**budgeting, saving, emergency funds, investments, and debt management** —
using forward-chaining, rule-based reasoning.

## 1. Problem Statement

Many people struggle to translate raw numbers (income, expenses, debt,
savings) into concrete financial actions. Certified financial planners
apply a well-known set of heuristics (e.g. the 50/30/20 budgeting rule,
the 3–6 month emergency fund rule, the debt avalanche method) to a
client's numbers to produce a personalized action plan. This project
encodes that expert reasoning as an explicit, machine-readable rule base
so that a user can input their financial facts and receive the same kind
of structured, explainable recommendations — without needing to consult
a human advisor for routine guidance.

## 2. Knowledge Acquisition Process

The rule base was built by:
1. Reviewing standard personal-finance heuristics used by financial
   planners and consumer-finance resources (e.g. CFPB guidance,
   Investopedia explainers on budgeting rules, emergency funds, debt
   payoff strategies, and risk-based asset allocation).
2. Distilling each heuristic into an explicit **IF (conditions) THEN
   (recommendation)** production rule, tagged with a category and a
   priority (so that when several rules fire at once, the most urgent
   advice — e.g. "you are overspending" — is surfaced above lower-priority
   advice like portfolio diversification).
3. Iteratively testing the rules against sample user profiles (see
   `tests/test_finance_advisor.py`) and refining thresholds (e.g. the
   3-month / 6-month emergency fund bands, the 15% high-interest-debt
   cutoff) until the system's advice matched what a human advisor would
   reasonably say for that profile.
4. Building in a **live knowledge acquisition channel**: option 3 in the
   CLI (`Add a new rule`) lets a user/expert add a brand-new rule at run
   time, which is validated and persisted back into `knowledge_base.json`
   — so the knowledge base can keep growing after deployment, not just
   at development time.

## 3. Knowledge Representation

Knowledge is represented as an external **JSON knowledge base**
(`knowledge_base.json`), kept fully separate from the inference engine
code, containing:

- `fact_schema` — documents every raw input fact the system accepts
  (`monthly_income`, `monthly_expenses`, `current_savings`,
  `monthly_debt_payment`, `total_debt`, `highest_debt_interest_rate`,
  `dependents`, `age`, `risk_tolerance`, `investment_experience`,
  `employment_status`).
- `derived_facts` — documents facts computed from raw facts
  (`disposable_income`, `savings_rate`, `debt_to_income_ratio`,
  `emergency_fund_months`).
- `rules` — a flat list of 24 production rules. Each rule has:
  ```json
  {
    "id": "R05",
    "category": "emergency_fund",
    "priority": 9,
    "conditions": [{"fact": "emergency_fund_months", "op": "<", "value": 3}],
    "conclusion": "Your emergency fund covers less than 3 months ..."
  }
  ```
  Conditions are AND-combined comparisons (`<, <=, >, >=, ==, !=`) over
  facts, which keeps the representation simple, human-readable, and
  directly editable without touching Python code.

## 4. Inference Strategy

The engine (`finance_advisor.FinanceAdvisorEngine`) uses **forward
chaining**:

1. Raw facts supplied by the user are combined with derived facts
   computed from them (`compute_derived_facts`).
2. Every rule in the knowledge base is checked against the current fact
   base; a rule **fires** if all of its conditions are satisfied.
3. All fired rules are collected (data-driven — the system reasons from
   the known facts forward to conclusions, rather than backward from a
   hypothesis).
4. **Conflict resolution**: fired rules are sorted by descending
   `priority`, so the most urgent, safety-critical advice (e.g.
   overspending, high debt-to-income ratio) is always listed first.
5. **Explanation facility**: for every fired rule, the engine records
   the exact fact values that satisfied its conditions, so the system
   can answer "why was I told this?" (`engine.explain()`), in the
   classic `IF <condition, with actual values> THEN <conclusion>` form.

## 5. Installation Instructions

Requires Python 3.9+.

```bash
git clone https://github.com/eaMwanika/financial-recommendations-using-rule-based-reasoning.git
cd financial-recommendations-using-rule-based-reasoning
pip install flask
```

### Run the CLI
```bash
python finance_advisor.py
```

### Run the Flask web UI
```bash
python app.py
# then open http://127.0.0.1:5000 in a browser
```

### Run the automated tests
```bash
python -m unittest discover -s tests -v
```

## 6. User Guide

**CLI (`finance_advisor.py`):**
1. `1. Get financial advice` — answer the prompted questions about your
   income, expenses, savings, debt, age, risk tolerance, investment
   experience, and employment status. The system prints every
   recommendation that fires, ordered by priority, and can optionally
   show the full explanation trace.
2. `2. View knowledge base rules` — lists every rule currently in the
   knowledge base.
3. `3. Add a new rule (knowledge acquisition)` — walk through adding a
   new production rule (fact/operator/value conditions plus a
   conclusion), which is saved permanently to `knowledge_base.json`.
4. `4. Exit`.

**Web UI (`app.py`):** fill in the same fields in the form and submit —
the results page shows the fired recommendations grouped by category
plus the full explanation trace underneath.

## 7. Sample Knowledge Base

See `knowledge_base.json` in the repository root — 24 rules spanning
budgeting (4), emergency funds (4), debt management (6), saving (4), and
investments (6), plus the documented fact schema and derived-fact
formulas described in section 3 above.

## 8. Project Structure

```
.
├── finance_advisor.py          # Inference engine, CLI, knowledge acquisition
├── knowledge_base.json         # External knowledge base (facts + 24 rules)
├── app.py                      # Flask web UI (reuses the same engine)
├── templates/
│   └── index.html              # Flask form + results template
├── tests/
│   └── test_finance_advisor.py # 10 automated test cases
├── screenshots/                # Screenshots for submission (see screenshots/README.md)
└── README.md
```

## 9. Screenshots

Placeholder text captures of a sample CLI run and the passing test suite
are included in `screenshots/`. See `screenshots/README.md` for the list
of PNG screenshots to add before final submission (CLI run, test results,
Flask UI, GitHub repo, merged Pull Request).

## 10. GitHub Collaboration

This work was developed on branch `feature/mmicheni-finance-advisor` and
submitted as a Pull Request into `main` per the group's collaboration
workflow (each member: own feature branch, ≥3 meaningful commits,
descriptive commit messages, one reviewed and merged PR).
