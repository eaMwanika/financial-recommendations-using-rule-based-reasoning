"""
Personal Finance Advisor - Knowledge-Based System
====================================================
APT 3020 - Knowledge-Based Systems

A rule-based expert system that gives personal finance recommendations
using forward-chaining inference over a JSON-stored knowledge base.

Components:
    - Knowledge representation : JSON rule base (knowledge_base.json)
      with a documented fact schema and IF-THEN production rules.
    - Inference engine         : forward chaining with priority-based
      conflict resolution, implemented in FinanceAdvisorEngine.
    - Knowledge acquisition    : interactive CLI menu option to add
      new rules to the knowledge base at run time (see add_rule_interactive).
    - Explanation facility     : every recommendation records which
      rule fired and why (the exact fact values that satisfied it).
    - User interface           : command-line interface below; a Flask
      web UI (app.py) reuses this same engine.

Author: mmicheni (APT 3020 coursework)
"""

import json
import operator
import os

KB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "knowledge_base.json")

OPERATORS = {
    "<": operator.lt,
    "<=": operator.le,
    ">": operator.gt,
    ">=": operator.ge,
    "==": operator.eq,
    "!=": operator.ne,
}


def load_knowledge_base(path=KB_PATH):
    """Load the JSON knowledge base from disk."""
    with open(path, "r") as f:
        return json.load(f)


def save_knowledge_base(kb, path=KB_PATH):
    """Persist the (possibly updated) knowledge base back to disk."""
    with open(path, "w") as f:
        json.dump(kb, f, indent=2)


class FinanceAdvisorEngine:
    """Forward-chaining inference engine for personal finance advice."""

    def __init__(self, kb_path=KB_PATH):
        self.kb_path = kb_path
        self.kb = load_knowledge_base(kb_path)
        self.facts = {}
        self.fired_rules = []  # populated by infer(); each item is an explanation dict

    # ---------- Knowledge representation / derived facts ----------

    def compute_derived_facts(self, user_facts):
        """Compute derived facts (ratios) from raw user-supplied facts."""
        facts = dict(user_facts)
        income = facts.get("monthly_income", 0) or 0.0001  # avoid div/0
        expenses = facts.get("monthly_expenses", 0)
        savings = facts.get("current_savings", 0)
        debt_payment = facts.get("monthly_debt_payment", 0)

        facts["disposable_income"] = facts.get("monthly_income", 0) - expenses
        facts["savings_rate"] = facts["disposable_income"] / income
        facts["debt_to_income_ratio"] = debt_payment / income
        facts["emergency_fund_months"] = savings / (expenses if expenses else 0.0001)
        return facts

    # ---------- Inference engine (forward chaining) ----------

    def _evaluate_condition(self, cond, facts):
        fact_name = cond["fact"]
        if fact_name not in facts:
            return False
        return OPERATORS[cond["op"]](facts[fact_name], cond["value"])

    def infer(self, user_facts):
        """
        Run forward chaining: evaluate every rule's conditions against the
        current fact base. All rules whose conditions are fully satisfied
        are considered 'fired'. Conflict resolution (when multiple rules
        fire) is by descending 'priority', so the most critical advice
        surfaces first.
        Returns a list of explanation dicts (also stored in self.fired_rules).
        """
        self.facts = self.compute_derived_facts(user_facts)
        fired = []
        for rule in self.kb["rules"]:
            conditions = rule["conditions"]
            matched = all(self._evaluate_condition(c, self.facts) for c in conditions)
            if matched:
                fired.append({
                    "id": rule["id"],
                    "category": rule["category"],
                    "priority": rule["priority"],
                    "conclusion": rule["conclusion"],
                    "why": self._explain_conditions(conditions, self.facts),
                })
        fired.sort(key=lambda r: r["priority"], reverse=True)
        self.fired_rules = fired
        return fired

    def _explain_conditions(self, conditions, facts):
        """Build a human-readable explanation of why a rule fired."""
        parts = []
        for c in conditions:
            fact_name = c["fact"]
            value = facts.get(fact_name)
            display_value = f"{value:.3f}" if isinstance(value, float) else value
            parts.append(f"{fact_name} ({display_value}) {c['op']} {c['value']}")
        return " AND ".join(parts)

    # ---------- Explanation facility ----------

    def explain(self):
        """Return a formatted explanation trace for the last inference run."""
        if not self.fired_rules:
            return "No rules fired for the given facts."
        lines = []
        for r in self.fired_rules:
            lines.append(
                f"[{r['id']} | {r['category']} | priority {r['priority']}]\n"
                f"  IF {r['why']}\n"
                f"  THEN {r['conclusion']}"
            )
        return "\n\n".join(lines)

    # ---------- Knowledge acquisition ----------

    def add_rule_interactive(self):
        """
        Interactive knowledge acquisition: prompts an expert/user to add a
        new production rule to the knowledge base, then persists it to
        knowledge_base.json so future sessions include it.
        """
        print("\n--- Add a new rule to the knowledge base ---")
        rule_id = input("Rule ID (e.g. R25): ").strip()
        category = input("Category (budgeting/saving/emergency_fund/investments/debt_management): ").strip()
        try:
            priority = int(input("Priority (1-10, higher = more urgent): ").strip())
        except ValueError:
            print("Priority must be an integer. Aborting.")
            return

        conditions = []
        print("Enter conditions one at a time. Leave fact name blank to stop.")
        print(f"Available facts: {', '.join(self.kb['fact_schema'].keys())} plus derived facts "
              f"({', '.join(self.kb['derived_facts'].keys())})")
        while True:
            fact = input("  Fact name: ").strip()
            if not fact:
                break
            op = input("  Operator (<, <=, >, >=, ==, !=): ").strip()
            raw_value = input("  Value: ").strip()
            value = self._coerce_value(raw_value)
            conditions.append({"fact": fact, "op": op, "value": value})

        conclusion = input("Conclusion / recommendation text: ").strip()

        new_rule = {
            "id": rule_id,
            "category": category,
            "priority": priority,
            "conditions": conditions,
            "conclusion": conclusion,
        }
        self.kb["rules"].append(new_rule)
        save_knowledge_base(self.kb, self.kb_path)
        print(f"Rule {rule_id} added and saved to {self.kb_path}.")

    @staticmethod
    def _coerce_value(raw_value):
        for caster in (int, float):
            try:
                return caster(raw_value)
            except ValueError:
                continue
        return raw_value  # keep as string (e.g. "high", "unemployed")


# ---------------------------------------------------------------------------
# Command-line interface
# ---------------------------------------------------------------------------

def _prompt_float(label):
    while True:
        try:
            return float(input(label))
        except ValueError:
            print("Please enter a number.")


def _prompt_int(label):
    while True:
        try:
            return int(input(label))
        except ValueError:
            print("Please enter a whole number.")


def _prompt_choice(label, choices):
    choices_l = [c.lower() for c in choices]
    while True:
        val = input(f"{label} ({'/'.join(choices)}): ").strip().lower()
        if val in choices_l:
            return val
        print(f"Please enter one of: {', '.join(choices)}")


def collect_facts_cli():
    print("\nAnswer the following questions about your finances.\n")
    facts = {
        "monthly_income": _prompt_float("Monthly net income: "),
        "monthly_expenses": _prompt_float("Monthly living expenses: "),
        "current_savings": _prompt_float("Current liquid savings/cash: "),
        "monthly_debt_payment": _prompt_float("Total monthly debt payments: "),
        "total_debt": _prompt_float("Total outstanding debt balance: "),
        "highest_debt_interest_rate": _prompt_float(
            "Highest debt interest rate as a decimal (e.g. 0.22 for 22%, 0 if none): "),
        "dependents": _prompt_int("Number of financial dependents: "),
        "age": _prompt_int("Your age: "),
        "risk_tolerance": _prompt_choice("Investment risk tolerance", ["low", "medium", "high"]),
        "investment_experience": _prompt_choice("Investment experience", ["none", "some", "experienced"]),
        "employment_status": _prompt_choice(
            "Employment status", ["employed", "self_employed", "unemployed", "student"]),
    }
    return facts


def run_cli():
    engine = FinanceAdvisorEngine()
    while True:
        print("\n===== Personal Finance Advisor =====")
        print("1. Get financial advice")
        print("2. View knowledge base rules")
        print("3. Add a new rule (knowledge acquisition)")
        print("4. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            facts = collect_facts_cli()
            fired = engine.infer(facts)
            print("\n--- Recommendations ---")
            if not fired:
                print("No specific recommendations triggered by your current facts.")
            for r in fired:
                print(f"\n[{r['category'].upper()}] {r['conclusion']}")
            show_why = input("\nShow explanation trace? (y/n): ").strip().lower()
            if show_why == "y":
                print("\n" + engine.explain())

        elif choice == "2":
            for rule in engine.kb["rules"]:
                print(f"{rule['id']} [{rule['category']}] (priority {rule['priority']}): {rule['conclusion']}")

        elif choice == "3":
            engine.add_rule_interactive()

        elif choice == "4":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    run_cli()
