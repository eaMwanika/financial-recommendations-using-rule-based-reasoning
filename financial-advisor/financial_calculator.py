class FinancialCalculator:
    
    def prepare_facts(
        self,
        earned_income,
        passive_income,
        dividends,
        interest,
        expenses,
        monthly_debt_payments,
        emergency_fund,
        risk_preference
    ):
        total_income = self.calculate_total_income(
            earned_income,
            passive_income,
            dividends,
            interest
            
        )
        recommended_expenses = self.calculate_recommended_expenses(
            total_income
        )
        recommended_wants = self.calculate_recommended_wants(
            total_income
        )
        recommended_savings = self.calculate_recommended_savings(
            total_income
            
        )
        recommended_investment = self.calculate_recommended_investment(
            total_income
        )
        
        
        debt_ratio = self.calculate_debt_ratio(
            monthly_debt_payments,
            total_income
        )
        
        emergency_months = self.calculate_emergency_months(
            emergency_fund,
            recommended_expenses
        )
        
        facts ={
            "earned_income": earned_income,
            "passive_income": passive_income,
            "dividends": dividends,
            "interest": interest,
            
            "total_income": total_income,
            
            "expenses": expenses,
            
            "recommended_expenses": recommended_expenses,
            "recommended_wants": recommended_wants,
            "recommended_savings": recommended_savings,
            "recommended_investment": recommended_investment,
            
            "monthly_debt_payments": monthly_debt_payments,
            "debt_ratio": debt_ratio,
            
            "emergency_fund": emergency_fund,
            "emergency_months": emergency_months,
            
            "risk_preference": risk_preference
            
        }
        return facts
    
       
    
    
    def __init__(self):
        pass
    
    def calculate_total_income(
        self,
        earned_income,
        passive_income,
        dividends, 
        interest
        
    ):
        return (
            earned_income
            + passive_income
            + dividends
            + interest
        )
        
    def calculate_recommended_expenses(self, total_income):
        return total_income *0.50
    
    def calculate_recommended_wants(self,total_income):
        return total_income * 0.30
    
    def calculate_recommended_savings(self,total_income):
        return total_income * 0.10
    
    def calculate_recommended_investment(self,total_income):
            return total_income * 0.10
        
    def calculate_debt_ratio(self, monthly_debt_payments, total_income):
        if total_income <=0:
            return 0
        
        return monthly_debt_payments / total_income
    
    def calculate_emergency_months(
        self,
        emergency_fund,
        monthly_essential_expenses
    ):
        if monthly_essential_expenses <=0:
            return 0
        return emergency_fund / monthly_essential_expenses
        