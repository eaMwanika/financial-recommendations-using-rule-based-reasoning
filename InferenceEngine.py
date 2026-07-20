import operator

class InferenceEngine:
    
    #Implements forward chaining using the rules
    #stored in the knowledge base.
    

    OPERATORS = {
        ">": operator.gt,
        "<": operator.lt,
        ">=": operator.ge,
        "<=": operator.le,
        "==": operator.eq,
        "!=": operator.ne
    }

    def __init__(self, knowledge_base):
        self.kb = knowledge_base

    # Evaluate one condition


    def evaluate_condition(self, condition, facts):

        left = facts.get(condition["field"])

        if "field_compare" in condition:

            right = facts.get(condition["field_compare"])

        else:

            right = condition["value"]

        operation = self.OPERATORS[condition["operator"]]

        return operation(left, right)


    # Evaluate one rule
    

    def evaluate_rule(self, rule, facts):

        for condition in rule["conditions"]:

            if not self.evaluate_condition(condition, facts):

                return False

        return True

    # Forward Chaining
    

    def infer(self, facts):

        inferred = facts.copy()

        changed = True

        while changed:

            changed = False

            for rule in self.kb.get_inference_rules():

                if self.evaluate_rule(rule, inferred):

                    action = rule["action"]

                    fact = action["fact"]

                    value = action["value"]

                    if inferred.get(fact) != value:

                        inferred[fact] = value

                        changed = True

        return inferred

    
    # Generate Recommendations

    def recommend(self, facts):

        recommendations = []

        for rule in self.kb.get_recommendation_rules():

            print(f"Checking {rule['id']}")

            if self.evaluate_rule(rule, facts):

                recommendations.append({

                    "category": rule["category"],

                    "title": rule["title"],

                    "message": rule["action"]["message"]

                })

        return recommendations
    
    # Scoring Method
    
    def calculate_financial_score(self, facts):

        score = 0

        if facts.get("within_budget"):
            score += 25
        
        if facts.get("debt_manageable"):
            score += 25
        
        if facts.get("emegency_fund_sufficient"):
            score += 25
        if facts.get("eligible_to_invest"):
            score += 25

        return score
    
    # Assessment Method
    def get_assessment(self, score):

        if score >=85:
            return "Excellent Financial Health"
        
        elif score >=70:
            return "Financial Stable"
        
        elif score >=50:
            return "DEveloping Financial Health"
        
        else:
            return "Financial Improvement Needed"





    
    # Complete Analysis
    

    def analyze(self, facts):

        inferred_facts = self.infer(facts)

        score = self.calculate_financial_score(inferred_facts)
            
        assessment = self.get_assessment(score)
        
        recommendations = self.recommend(inferred_facts)

        return {

            "facts": inferred_facts,
            "financial_score": score,
            "assessment": assessment,
            "recommendations": recommendations

        }