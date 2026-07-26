from flask import Flask, render_template, request

from knowledge_base import KnowledgeBase
from financialCalculator import FinancialCalculator
from InferenceEngine import InferenceEngine

app = Flask(__name__)

kb = KnowledgeBase()
print("Inference Rules:", len(kb.get_inference_rules()))
print("Recommendation Rules:", len(kb.get_recommendation_rules()))
calculator = FinancialCalculator(kb)
engine = InferenceEngine(kb)

# landing Page
@app.route("/")
def landing():
    return render_template("landing.html")

# Assessment Page
@app.route("/assessment")
def assessment():
    return render_template("assessment.html")

# Results page
@app.route("/analyze", methods=["POST"])
def analyze():

    facts = {

        "earned_income": float(request.form["earned_income"]),

        "passive_income": float(request.form["passive_income"]),

        "dividends_received": float(request.form["dividends_received"]),

        "interest_from_savings": float(request.form["interest_from_savings"]),

        "expenses": float(request.form["expenses"]),
        
        "monthly_debt_payment": float(request.form["monthly_debt_payment"]),

        "current_emergency_fund": float(request.form["current_emergency_fund"]),

        "risk_preference": request.form["risk_preference"]

    }

    # Perform calculations
    calculated_facts = calculator.calculate(facts)

    # Run the expert system
    report = engine.analyze(calculated_facts)

    print("\n REPORT")
    print(report)

    report["facts"]["debt_ratio_percent"] = (
    report["facts"]["debt_to_income_ratio"] * 100
)
    # grouped recommendations
    grouped_recommendations = {}
    for recommendation in report["recommendations"]:
        category = recommendation["category"]
        if category not in grouped_recommendations:
            grouped_recommendations[category]=[]
        grouped_recommendations[category].append(recommendation)


    print("\nGrouped Recommendations")
    print(grouped_recommendations)
            



    # Display results
    return render_template(
        "results.html",
        report=report,
        grouped_recommendations=grouped_recommendations
    )


if __name__ == "__main__":
    app.run(debug=True)