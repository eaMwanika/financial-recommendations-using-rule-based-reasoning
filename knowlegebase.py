rules = {
    "Budgetting Rule" : {
        "IF" : ["expenses > income"],
        "THEN": "recommend reducing discretionary spending"
    },

    "Saving Rule" : {
        "IF" : ["savings < 20% of income"],
        "THEN": "recommend increasing monthly savings contributions"
    },

    "Emergency Fund Rule" : {
        "IF" : ["emergency fund < 3 months of expenses"],
        "THEN": "recommend prioritizing emergency fund contributions"
    },

    "Investment Rule": {
        "IF": ["emergency fund is sufficient AND savings rate ≥ 20%"],
        "THEN": "recommend investing surplus funds"
    },

     "Debt Management Rule": {
         "IF": ["debt-to-income ratio > 40%"],
         "THEN": "recommend debt repayment strategies before new investments"
     }
}