"""
Knowledge acquisition tool for the Personal Finance Advisor.

Currently knowledge.json can only be extended by hand-editing the file.
This script provides a guided, validated way to add a new inference_rule
or recommendation_rule at run time, and persists it back to knowledge.json
via the existing KnowledgeBase loader (so both the CLI and the Flask app
immediately see the new rule on their next run).

Usage: python add_rule.py
"""

import json
from knowledge_base import KnowledgeBase

VALID_OPERATORS = [">", "<", ">=", "<=", "==", "!="]


def prompt(label):
    return input(label).strip()


def coerce_value(raw):
    if raw.lower() == "true":
        return True
    if raw.lower() == "false":
        return False
    for caster in (int, float):
        try:
            return caster(raw)
        except ValueError:
            continue
    return raw


def collect_conditions():
    conditions = []
    print("Enter conditions one at a time. Leave the field name blank to stop.")
    while True:
        field = prompt("  Field name (fact this condition checks): ")
        if not field:
            break
        operator_ = prompt(f"  Operator {VALID_OPERATORS}: ")
        if operator_ not in VALID_OPERATORS:
            print(f"  Invalid operator, must be one of {VALID_OPERATORS}. Try again.")
            continue
        compare_mode = prompt("  Compare against a fixed value or another field? (value/field): ").lower()
        condition = {"field": field, "operator": operator_}
        if compare_mode == "field":
            condition["field_compare"] = prompt("  Field to compare against: ")
        else:
            condition["value"] = coerce_value(prompt("  Value: "))
        conditions.append(condition)
    return conditions


def add_inference_rule(kb):
    rule_id = prompt("New rule ID (e.g. IR12): ")
    category = prompt("Category: ")
    conditions = collect_conditions()
    fact = prompt("Fact this rule sets (action.fact): ")
    value = coerce_value(prompt("Value to set it to (action.value): "))

    rule = {
        "id": rule_id,
        "category": category,
        "conditions": conditions,
        "action": {"type": "infer", "fact": fact, "value": value},
    }
    kb.data.setdefault("inference_rules", []).append(rule)
    return rule


def add_recommendation_rule(kb):
    rule_id = prompt("New rule ID (e.g. RR15): ")
    category = prompt("Category: ")
    title = prompt("Title: ")
    conditions = collect_conditions()
    message = prompt("Recommendation message: ")

    rule = {
        "id": rule_id,
        "category": category,
        "title": title,
        "conditions": conditions,
        "action": {"type": "recommend", "message": message},
    }
    kb.data.setdefault("recommendation_rules", []).append(rule)
    return rule


def save(kb):
    with open(kb.filename, "w", encoding="utf-8") as f:
        json.dump(kb.data, f, indent=2)


def run():
    kb = KnowledgeBase()
    print("=== Knowledge Acquisition: Add a New Rule ===")
    kind = prompt("Add an (i)nference rule or a (r)ecommendation rule? ").strip().lower()

    if kind == "i":
        rule = add_inference_rule(kb)
    elif kind == "r":
        rule = add_recommendation_rule(kb)
    else:
        print("Invalid choice. Aborting.")
        return

    save(kb)
    print(f"\nRule {rule['id']} added and saved to {kb.filename}.")


if __name__ == "__main__":
    run()
