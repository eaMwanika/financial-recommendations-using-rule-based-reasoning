"""
Command-line interface for the Personal Finance Advisor.

Reuses the existing KnowledgeBase, FinancialCalculator, and InferenceEngine
(knowledge_base.py, financialCalculator.py, InferenceEngine.py) so the CLI
and the Flask web app (app.py) always reason over the exact same knowledge
base and produce identical results — this file adds a second interface,
it does not duplicate the reasoning logic.

Also adds an explanation trace: for each recommendation, prints which
inference/recommendation rule fired and which fact values satisfied it,
since InferenceEngine.recommend() returns only the final message.
"""

from knowledge_base import KnowledgeBase
from financialCalculator import FinancialCalculator
from InferenceEngine import InferenceEngine


def prompt_float(label):
    while True:
        try:
            return float(input(label))
        except ValueError:
            print("Please enter a number.")


def prompt_choice(label, choices):
    while True:
        val = input(f"{label} ({'/'.join(choices)}): ").strip()
        if val in choices:
            return val
        print(f"Please enter exactly one of: {', '.join(choices)}")


def collect_facts():
    print("\nAnswer the following questions about your finances.\n")
    return {
        "earned_income": prompt_float("Monthly earned income: "),
        "passive_income": prompt_float("Monthly passive income: "),
        "dividends_received": prompt_float("Monthly dividends received: "),
        "interest_from_savings": prompt_float("Monthly interest from savings: "),
        "expenses": prompt_float("Monthly expenses: "),
        "monthly_debt_payment": prompt_float("Monthly debt payment: "),
        "current_emergency_fund": prompt_float("Current emergency fund balance: "),
        "risk_preference": prompt_choice(
            "Risk preference", ["Risk Averse", "Risk Neutral", "Risk Tolerant"]),
    }


def explain_condition(condition, facts):
    field = condition["field"]
    op = condition["operator"]
    left_val = facts.get(field)
    if "field_compare" in condition:
        right_desc = condition["field_compare"]
        right_val = facts.get(right_desc)
    else:
        right_desc = condition["value"]
        right_val = condition["value"]
    return f"{field} ({left_val}) {op} {right_desc}" + (f" ({right_val})" if "field_compare" in condition else "")


def explain_rule(rule, facts):
    return " AND ".join(explain_condition(c, facts) for c in rule["conditions"])


def print_explanation_trace(kb, inferred_facts):
    """Explanation facility: show which inference and recommendation rules
    fired, and the exact fact values that satisfied each one."""
    print("\n--- Explanation trace ---")
    for rule in kb.get_inference_rules():
        if all(_matches(c, inferred_facts) for c in rule["conditions"]):
            action = rule["action"]
            print(f"[{rule['id']}] IF {explain_rule(rule, inferred_facts)}"
                  f"  THEN {action['fact']} = {action['value']}")
    for rule in kb.get_recommendation_rules():
        if all(_matches(c, inferred_facts) for c in rule["conditions"]):
            print(f"[{rule['id']}] IF {explain_rule(rule, inferred_facts)}"
                  f"  THEN \"{rule['title']}\": {rule['action']['message']}")


def _matches(condition, facts):
    import operator
    ops = {">": operator.gt, "<": operator.lt, ">=": operator.ge,
           "<=": operator.le, "==": operator.eq, "!=": operator.ne}
    left = facts.get(condition["field"])
    right = facts.get(condition["field_compare"]) if "field_compare" in condition else condition["value"]
    if left is None or right is None:
        return False
    return ops[condition["operator"]](left, right)


def run():
    kb = KnowledgeBase()
    calculator = FinancialCalculator(kb)
    engine = InferenceEngine(kb)

    while True:
        print("\n===== Personal Finance Advisor (CLI) =====")
        print("1. Get financial advice")
        print("2. View knowledge base rules")
        print("3. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            facts = collect_facts()
            calculated = calculator.calculate(facts)
            report = engine.analyze(calculated)

            print(f"\nFinancial score: {report['financial_score']}/100")
            print(f"Assessment: {report['assessment']}")
            print("\n--- Recommendations ---")
            if not report["recommendations"]:
                print("No specific recommendations triggered by your current facts.")
            for rec in report["recommendations"]:
                print(f"\n[{rec['category']}] {rec['title']}: {rec['message']}")

            if input("\nShow explanation trace? (y/n): ").strip().lower() == "y":
                print_explanation_trace(kb, report["facts"])

        elif choice == "2":
            print("\nInference rules:")
            for r in kb.get_inference_rules():
                print(f"  {r['id']} [{r['category']}]")
            print("\nRecommendation rules:")
            for r in kb.get_recommendation_rules():
                print(f"  {r['id']} [{r['category']}] {r['title']}")

        elif choice == "3":
            print("Goodbye.")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    run()
