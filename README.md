# financial-recommendations-using-rule-based-reasoning
A class project to demonstrate financial recommendations using rule-based reasoning

##  Project Overview
This project implements a **Knowledge-Based System (KBS)** that provides financial recommendations in key areas of personal finance. The system uses **facts** and **rules** to reason about a user’s financial situation and generate actionable advice. The goal is to demonstrate how rule-based reasoning can support decision-making in budgeting, saving, emergency funds, investments, and debt management.

---

## Problem Being Solved
Managing personal finances requires balancing multiple priorities:
- Creating a sustainable **budget**
- Building **savings** habits
- Maintaining an **emergency fund**
- Making informed **investment** decisions
- Handling **debt** responsibly

This KBS helps users by applying structured rules to facts about their financial situation, producing clear recommendations.

---

##  Knowledge Base Structure

### Facts
Examples of facts the system may store:
- Monthly income
- Monthly expenses
- Current savings balance
- Existing debt amount
- Emergency fund status
- Investment portfolio size

### Rules
The system applies rules such as:
- **Budgeting Rule:** IF expenses > income THEN recommend reducing discretionary spending.
- **Saving Rule:** IF savings < 20% of income THEN recommend increasing monthly savings contributions.
- **Emergency Fund Rule:** IF emergency fund < 3 months of expenses THEN recommend prioritizing emergency fund contributions.
- **Investment Rule:** IF emergency fund is sufficient AND savings rate ≥ 20% THEN recommend investing surplus funds.
- **Debt Management Rule:** IF debt-to-income ratio > 40% THEN recommend debt repayment strategies before new investments.

### Conclusions
Based on facts and rules, the system can conclude:
- “You should reduce discretionary spending.”
- “Increase monthly savings by 10%.”
- “Prioritize building your emergency fund.”
- “Consider investing in diversified assets.”
- “Focus on debt repayment before investing.”

---

##  How Inference Works
1. **User Input:** The system accepts facts about the user’s financial situation.
2. **Rule Matching:** It applies rules to these facts.
3. **Reasoning:** Multi-step reasoning is supported (e.g., debt rules may override investment rules).
4. **Output:** The system generates recommendations and explains the reasoning behind them.

---

##  How to Run the System
1. Clone the repository:
   ```bash
   git clone https://github.com/eaMwanika/financial-recommendations-using-rule-based-reasoning
