from financial_calculator import FinancialCalculator
from Inference_engine import InferenceEngine
from knowledge_base import KnowledgeBase

calculator = FinancialCalculator()
kb = KnowledgeBase()


facts = calculator.prepare_facts(
    earned_income=100000,
    passive_income=5000,
    dividends=2000,
    interest=1000,
    expenses=70000,
    monthly_debt_payments=40000,
    emergency_fund=100000,
    risk_preference="Risk Neutral"
)

engine = InferenceEngine(kb)



def get_results(self):
    results = self.facts.copy()
    results.update(self.derived_facts)
    return results

results = engine.infer(facts)





