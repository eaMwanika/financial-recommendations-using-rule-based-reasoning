"""
Automated test suite for the Personal Finance Advisor KBS.
Run with: python -m unittest discover -s tests
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from finance_advisor import FinanceAdvisorEngine


def base_facts(**overrides):
    facts = {
        "monthly_income": 3000,
        "monthly_expenses": 2000,
        "current_savings": 6000,
        "monthly_debt_payment": 300,
        "total_debt": 0,
        "highest_debt_interest_rate": 0.0,
        "dependents": 0,
        "age": 28,
        "risk_tolerance": "medium",
        "investment_experience": "some",
        "employment_status": "employed",
    }
    facts.update(overrides)
    return facts


class TestDerivedFacts(unittest.TestCase):
    def setUp(self):
        self.engine = FinanceAdvisorEngine()

    def test_disposable_income_calculation(self):
        facts = self.engine.compute_derived_facts(base_facts(monthly_income=3000, monthly_expenses=2000))
        self.assertEqual(facts["disposable_income"], 1000)

    def test_savings_rate_calculation(self):
        facts = self.engine.compute_derived_facts(base_facts(monthly_income=4000, monthly_expenses=3000))
        self.assertAlmostEqual(facts["savings_rate"], 0.25)

    def test_emergency_fund_months_calculation(self):
        facts = self.engine.compute_derived_facts(base_facts(current_savings=6000, monthly_expenses=2000))
        self.assertAlmostEqual(facts["emergency_fund_months"], 3.0)


class TestInferenceRules(unittest.TestCase):
    def setUp(self):
        self.engine = FinanceAdvisorEngine()

    def test_overspending_triggers_R01(self):
        fired = self.engine.infer(base_facts(monthly_income=2000, monthly_expenses=2500))
        ids = [r["id"] for r in fired]
        self.assertIn("R01", ids)

    def test_low_emergency_fund_triggers_R05(self):
        fired = self.engine.infer(base_facts(current_savings=1000, monthly_expenses=2000))
        ids = [r["id"] for r in fired]
        self.assertIn("R05", ids)

    def test_high_debt_to_income_triggers_R09(self):
        fired = self.engine.infer(base_facts(monthly_income=2000, monthly_debt_payment=900))
        ids = [r["id"] for r in fired]
        self.assertIn("R09", ids)

    def test_debt_free_triggers_R12(self):
        fired = self.engine.infer(base_facts(total_debt=0))
        ids = [r["id"] for r in fired]
        self.assertIn("R12", ids)

    def test_low_risk_tolerance_triggers_R19(self):
        fired = self.engine.infer(base_facts(risk_tolerance="low"))
        ids = [r["id"] for r in fired]
        self.assertIn("R19", ids)

    def test_rules_sorted_by_priority_descending(self):
        fired = self.engine.infer(base_facts(monthly_income=2000, monthly_expenses=2500,
                                              current_savings=500, monthly_debt_payment=900))
        priorities = [r["priority"] for r in fired]
        self.assertEqual(priorities, sorted(priorities, reverse=True))

    def test_explanation_facility_generates_trace(self):
        self.engine.infer(base_facts(risk_tolerance="low"))
        trace = self.engine.explain()
        self.assertIn("R19", trace)
        self.assertIn("IF", trace)
        self.assertIn("THEN", trace)


if __name__ == "__main__":
    unittest.main()
