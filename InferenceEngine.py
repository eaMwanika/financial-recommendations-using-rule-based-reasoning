import operator

class InferenceEngine:
    """
    Implements forward chaining using the rules
    stored in the knowledge base.
    """

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

            if self.evaluate_rule(rule, facts):

                recommendations.append({

                    "category": rule["category"],

                    "title": rule["title"],

                    "message": rule["action"]["message"]

                })

        return recommendations

    
    # Complete Analysis
    

    def analyze(self, facts):

        inferred_facts = self.infer(facts)

        recommendations = self.recommend(inferred_facts)

        return {

            "facts": inferred_facts,

            "recommendations": recommendations

        }