class FinancialCalculator:
    
     #Calculates all derived financial facts.


    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    def calculate(self, facts):
        
        #Takes user facts and returns the same dictionary
        #with additional calculated values.
        

        results = facts.copy()

    
        # Load configuration
    

        budget = self.kb.get_budget_model()

        needs_percentage = budget["needs"]
        wants_percentage = budget["wants"]
        savings_percentage = budget["savings"]
        investment_percentage = budget["investment"]

        emergency_months = self.kb.get_emergency_months()

    
        # Total Income

        total_income = (
            facts["earned_income"]
            + facts["passive_income"]
            + facts["dividends_received"]
            + facts["interest_from_savings"]
        )

        # budget Allocations

        recommended_expenses = total_income * needs_percentage

        recommended_wants = total_income * wants_percentage

        recommended_savings = total_income * savings_percentage

        recommended_investment = (
            total_income * investment_percentage
        )

    
        # Emergency Fund Target
        

        emergency_fund_target = (
            facts["expenses"] * emergency_months
        )

        
        # Debt Ratio
        

        if total_income > 0:

            debt_ratio = (
                facts["monthly_debt_payment"] / total_income
            )

        else:

            debt_ratio = 0
        
       

    
        # Save Calculated Facts
        

        results["total_income"] = total_income

        results["recommended_expenses"] = recommended_expenses

        results["recommended_wants"] = recommended_wants
        
        results["recommended_savings"] = recommended_savings

        results["recommended_investment"] = (
            recommended_investment
        )

        results["emergency_fund_target"] = (
            emergency_fund_target
        )

        results["debt_to_income_ratio"] = debt_ratio
        
        

        return results