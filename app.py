import re
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

@app.route('/chat')
def chat():
    return render_template('chat.html')
def extract_amount(pattern, text):

    match = re.search(pattern, text)

    if not match:
        return 0

    value = match.group(1).replace(',', '')

    return float(value)
@app.route('/chat-assessment', methods=['POST'])
def chat_assessment():

    text = request.form['message'].lower()
    allowance = extract_amount(r'allowance[^\d]*(\d[\d,]*)', text)
    salary    = extract_amount(r'salary[^\d]*(\d[\d,]*)', text)
    business  = extract_amount(r'business[^\d]*(\d[\d,]*)', text)

    expenses  = extract_amount(r'(?:spend|expenses)[^\d]*(\d[\d,]*)', text)
    debt      = extract_amount(r'debt[^\d]*(\d[\d,]*)', text)
    savings   = extract_amount(r'(?:savings|emergency)[^\d]*(\d[\d,]*)', text)

    
    earned_income = allowance + salary + business

    risk = 'low'

    if 'medium risk' in text or 'moderate risk' in text:
        risk = 'medium'

    elif 'high risk' in text or 'aggressive' in text:
        risk = 'high'

    calculator = FinancialCalculator()

    facts = calculator.prepare_facts(
        earned_income=earned_income,
        passive_income=0,
        dividends=0,
        interest=0,
        expenses=expenses,
        monthly_debt_payments=debt,
        emergency_fund=savings,
        risk_preference=risk
    )

    kb = KnowledgeBase('knowledge.json')
    engine = InferenceEngine(kb)

    results = engine.infer(facts)

    return render_template('results.html', data=results)






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