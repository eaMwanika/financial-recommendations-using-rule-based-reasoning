"""
Automated test suite for the Personal Finance Advisor KBS.
Covers KnowledgeBase loading, FinancialCalculator derived-fact math,
and InferenceEngine forward chaining + recommendation generation.

Run with: python -m unittest discover -s tests -v
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from knowledge_base import KnowledgeBase
from financialCalculator import FinancialCalculator
from InferenceEngine import InferenceEngine

KB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "knowledge.json")


def sample_facts(**overrides):
    facts = {
        "earned_income": 3000,
        "passive_income": 0,
        "dividends_received": 0,
        "interest_from_savings": 0,
        "expenses": 1500,
        "monthly_debt_payment": 300,
        "current_emergency_fund": 6000,
        "risk_preference": "Risk Neutral",
    }
    facts.update(overrides)
    return facts


class TestKnowledgeBase(unittest.TestCase):
    def setUp(self):
        self.kb = KnowledgeBase(KB_PATH)

    def test_loads_inference_rules(self):
        self.assertGreater(len(self.kb.get_inference_rules()), 0)

    def test_loads_recommendation_rules(self):
        self.assertGreater(len(self.kb.get_recommendation_rules()), 0)

    def test_budget_model_sums_to_one(self):
        budget = self.kb.get_budget_model()
        total = budget["needs"] + budget["wants"] + budget["savings"] + budget["investment"]
        self.assertAlmostEqual(total, 1.0)

    def test_missing_file_raises(self):
        with self.assertRaises(FileNotFoundError):
            KnowledgeBase("does_not_exist.json")


class TestFinancialCalculator(unittest.TestCase):
    def setUp(self):
        self.kb = KnowledgeBase(KB_PATH)
        self.calc = FinancialCalculator(self.kb)

    def test_total_income_sums_all_sources(self):
        result = self.calc.calculate(sample_facts(earned_income=3000, passive_income=200,
                                                    dividends_received=50, interest_from_savings=10))
        self.assertEqual(result["total_income"], 3260)

    def test_debt_to_income_ratio(self):
        result = self.calc.calculate(sample_facts(earned_income=2000, monthly_debt_payment=400))
        self.assertAlmostEqual(result["debt_to_income_ratio"], 0.2)

    def test_debt_to_income_ratio_zero_income(self):
        result = self.calc.calculate(sample_facts(earned_income=0, passive_income=0,
                                                    dividends_received=0, interest_from_savings=0))
        self.assertEqual(result["debt_to_income_ratio"], 0)

    def test_emergency_fund_target_uses_expenses_and_months(self):
        result = self.calc.calculate(sample_facts(expenses=1000))
        expected = 1000 * self.kb.get_emergency_months()
        self.assertEqual(result["emergency_fund_target"], expected)


class TestInferenceEngine(unittest.TestCase):
    def setUp(self):
        self.kb = KnowledgeBase(KB_PATH)
        self.calc = FinancialCalculator(self.kb)
        self.engine = InferenceEngine(self.kb)

    def test_within_budget_true_when_expenses_low(self):
        facts = self.calc.calculate(sample_facts(earned_income=5000, expenses=500))
        inferred = self.engine.infer(facts)
        self.assertTrue(inferred["within_budget"])

    def test_debt_manageable_false_when_ratio_high(self):
        facts = self.calc.calculate(sample_facts(earned_income=2000, monthly_debt_payment=900))
        inferred = self.engine.infer(facts)
        self.assertFalse(inferred["debt_manageable"])

    def test_eligible_to_invest_requires_both_conditions(self):
        facts = self.calc.calculate(sample_facts(earned_income=5000, expenses=500,
                                                   monthly_debt_payment=100,
                                                   current_emergency_fund=20000))
        inferred = self.engine.infer(facts)
        self.assertTrue(inferred["eligible_to_invest"])

    def test_recommendations_generated_for_over_budget_case(self):
        report = self.engine.analyze(self.calc.calculate(
            sample_facts(earned_income=2000, expenses=1900, monthly_debt_payment=900,
                          current_emergency_fund=0)))
        categories = [r["category"] for r in report["recommendations"]]
        self.assertIn("Budget", categories)
        self.assertIn("Debt", categories)

    def test_financial_score_is_between_0_and_100(self):
        report = self.engine.analyze(self.calc.calculate(sample_facts()))
        self.assertGreaterEqual(report["financial_score"], 0)
        self.assertLessEqual(report["financial_score"], 100)


if __name__ == "__main__":
    unittest.main()
