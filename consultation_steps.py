CONSULTATION_STEPS = [
   {
    "id": 1,

    "title": "Personal Profile",

    "description": (
        "Let's begin by understanding your personal circumstances "
        "and financial goals."
    ),

    "advisor_insight": (
        "Every financial plan begins with understanding your life stage, "
        "responsibilities, and financial priorities."
    ),

    "fields": [

        {
            "name": "age_group",
            "label": "Age Group",
            "type": "select",
            "required": True,
            "options": [
                "18–24",
                "25–34",
                "35–44",
                "45–54",
                "55+"
            ]
        },

        {
            "name": "employment_status",
            "label": "Employment Status",
            "type": "select",
            "required": True,
            "options": [
                "Employed",
                "Self-employed",
                "Student",
                "Unemployed",
                "Retired"
            ]
        },

        {
            "name": "dependents",
            "label": "Number of Dependents",
            "type": "select",
            "required": True,
            "options": [
                "0",
                "1",
                "2",
                "3",
                "4+"
            ]
        },

        {
            "name": "financial_goal",
            "label": "Primary Financial Goal",
            "type": "select",
            "required": True,
            "options": [
                "Build an Emergency Fund",
                "Reduce Debt",
                "Buy a Home",
                "Save for Education",
                "Grow Investments",
                "Retirement Planning",
                "Improve Financial Stability"
            ]
        }

    ]
},
   
   {
    "id": 2,
    "title": "Income Assessment",

    "description": (
        "Let's understand the money available to support your financial goals."
    ),

    "advisor_insight": (
        "A complete picture of your income allows realistic budgeting, debt management, and investment planning."
    ),

    "fields": [

        {
            "name": "employment_income",
            "label": "Monthly Employment Income",
            "type": "number",
            "required": True,
            "prefix": "KSh"
        },

        {
            "name": "business_income",
            "label": "Monthly Business Income",
            "type": "number",
            "required": False,
            "prefix": "KSh"
        },

        {
            "name": "passive_income",
            "label": "Monthly Passive Income",
            "type": "number",
            "required": False,
            "prefix": "KSh"
        },

        {
            "name": "investment_income",
            "label": "Monthly Investment Income",
            "type": "number",
            "required": False,
            "prefix": "KSh"
        },

        {
            "name": "other_income",
            "label": "Other Monthly Income",
            "type": "number",
            "required": False,
            "prefix": "KSh"
        }

    ]
},
   
   {
    "id": 3,

    "title": "Expense Assessment",

    "description": (
        "Let's understand how your monthly income is spent."
    ),

    "advisor_insight": (
        "Understanding spending patterns helps identify opportunities "
        "to improve financial health."
    ),

    "fields": [

        {
            "name": "housing_expenses",
            "label": "Monthly Housing Expenses",
            "type": "number",
            "required": True,
            "prefix": "KSh"
        },

        {
            "name": "living_expenses",
            "label": "Monthly Living Expenses",
            "type": "number",
            "required": True,
            "prefix": "KSh"
        },

        {
            "name": "lifestyle_expenses",
            "label": "Monthly Lifestyle Expenses",
            "type": "number",
            "required": True,
            "prefix": "KSh"
        },

        {
            "name": "other_expenses",
            "label": "Other Monthly Expenses",
            "type": "number",
            "required": False,
            "prefix": "KSh"
        }

    ]
},
   {
    "id": 4,

    "title": "Debt Assessment",

    "description": (
        "Let's understand your current debt commitments."
    ),

    "advisor_insight": (
        "Monthly debt repayments help determine whether your current debt level is sustainable."
    ),

    "fields": [

        {
            "name": "monthly_debt_payment",
            "label": "Monthly Debt Repayments",
            "type": "number",
            "required": True,
            "prefix": "KSh",
            "helper_text": (
                "Include all monthly repayments for loans, mortgages, "
                "HELB, SACCO loans, credit cards, digital loans, and other debts."
            )
        }

    ]
},
   {
    "id": 5,

    "title": "Emergency Savings",

    "description": (
        "Let's determine whether you are financially prepared "
        "for unexpected situations."
    ),

    "advisor_insight": (
        "Emergency savings provide financial security and reduce the need "
        "to rely on debt during difficult times."
    ),

    "fields": [

        {
            "name": "current_emergency_fund",
            "label": "Current Emergency Savings",
            "type": "number",
            "required": True,
            "prefix": "KSh",
            "helper_text": (
                "Include savings that are easily accessible during emergencies."
            )
        }

    ]
},

{
    "id": 6,

    "title": "Investment Profile",

    "description": (
        "Let's understand your comfort level with investment risk."
    ),

    "advisor_insight": (
        "The best investment strategy is one that matches both your financial situation "
        "and your tolerance for investment risk."
    ),

    "fields": [

        {
            "name": "risk_preference",
            "label": "Investment Risk Preference",
            "type": "select",
            "required": True,
            "options": [

                "Conservative",

                "Moderate",

                "Aggressive"

            ],
            "helper_text": (
                "Choose the option that best reflects how comfortable you are with investment risk."
            )
        }

    ]
},
{
    "id":7,

    "title":"Review",

    "description":"Review your consultation before generating your financial advisory report.",

    "advisor_insight":"Accurate information results in more reliable financial recommendations.",

    "fields":[]
}

    
]