"""
Flask web UI for the Personal Finance Advisor.
Thin presentation layer over finance_advisor.FinanceAdvisorEngine — the
same knowledge base and inference engine used by the CLI (finance_advisor.py).
"""

from flask import Flask, render_template, request
from finance_advisor import FinanceAdvisorEngine

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    recommendations = None
    explanation = None
    if request.method == "POST":
        facts = {
            "monthly_income": float(request.form["monthly_income"]),
            "monthly_expenses": float(request.form["monthly_expenses"]),
            "current_savings": float(request.form["current_savings"]),
            "monthly_debt_payment": float(request.form["monthly_debt_payment"]),
            "total_debt": float(request.form["total_debt"]),
            "highest_debt_interest_rate": float(request.form["highest_debt_interest_rate"]),
            "dependents": int(request.form["dependents"]),
            "age": int(request.form["age"]),
            "risk_tolerance": request.form["risk_tolerance"],
            "investment_experience": request.form["investment_experience"],
            "employment_status": request.form["employment_status"],
        }
        engine = FinanceAdvisorEngine()
        recommendations = engine.infer(facts)
        explanation = engine.explain()

    return render_template("index.html", recommendations=recommendations, explanation=explanation)


if __name__ == "__main__":
    app.run(debug=True)
