from flask import Flask, render_template, request

from financial_calculator import FinancialCalculator
from knowledge_base import KnowledgeBase
from Inference_engine import InferenceEngine


app = Flask(__name__)

# Initialize expert system components
calculator = FinancialCalculator()
knowledge_base = KnowledgeBase('knowledge.json')
engine = InferenceEngine(knowledge_base)


@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/assessment')
def assessment():
    return render_template('assessment.html')


@app.route('/results', methods=['POST'])
def results():

    # ===== Form data =====
    earned_income = float(request.form.get('earned_income', 0))
    passive_income = float(request.form.get('passive_income', 0))
    expenses = float(request.form.get('expenses', 0))
    monthly_debt_payments = float(request.form.get('total_debts', 0))
    emergency_fund = float(request.form.get('emergency_fund', 0))
    risk_preference = request.form.get('risk_preference', 'low')
    dividends = float(request.form.get('dividends', 0))

    # Not collected yet in the wizard
    interest = 0

    # ===== Financial calculations =====
    facts = calculator.prepare_facts(
        earned_income=earned_income,
        passive_income=passive_income,
        dividends=dividends,
        interest=interest,
        expenses=expenses,
        monthly_debt_payments=monthly_debt_payments,
        emergency_fund=emergency_fund,
        risk_preference=risk_preference
    )

    # ===== Expert system inference =====
    results_data = engine.infer(facts)

    return render_template('results.html', data=results_data)


if __name__ == '__main__':
    app.run(debug=True)