from KnowledgeBase import KnowledgeBase
from InferenceEngine import InferenceEngine

kb = KnowledgeBase()

engine = InferenceEngine(kb)

facts = {
    "debt_ratio": 0.45,
    "expenses": 70000,
    "recommended_expenses": 50000,
    "emergency_months": 2,
    "risk_preference": "Risk Neutral"
}

results = engine.infer(facts)

print("\nFinal Working Memory")
print("--------------------")
for key, value in results.items():
    print(f"{key}: {value}")