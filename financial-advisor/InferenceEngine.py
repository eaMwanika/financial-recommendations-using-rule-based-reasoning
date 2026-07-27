class InferenceEngine:

    def __init__(self, knowledge_base):

        self.knowledge_base = knowledge_base
        
        # load every rule from the knowledge base
        self.rules = knowledge_base.get_rules()
        self.facts= {}
        # working menory from the infered facts
        self.derived_facts = {}
        self.fired_rules = set()
        
    def infer(self, facts):

        self.facts = facts.copy()

        self.derived_facts = {}

        self.fired_rules = set()

        self.forward_chain()

        results = self.facts.copy()
        results.update(self.derived_facts)

        return results
    
    
            
    def evaluate_condition(self, condition):
        field = condition["field"]
        
        operator = condition ["operator"]
        
        operand = condition["operand"]
    
        
        left = self.facts.get(field)
        
        right = self.resolve_operand(operand)
        # compare left and right.
        
        if operator == "==":
            return left == right
        
        elif operator == "!=":
            return left != right
        
        elif operator == ">":
            return left > right
        
        elif operator == ">=":
            return left >= right
        
        elif operator == "<":
            return left < right 
        
        elif operator == "<=":
            return left <= right
        
        raise ValueError (
            f"Unsupported operator: {operator}"
        )
        
    
    def evaluate_rule(self, rule):
        conditions = rule.get ("conditions", [])
        
        for condition in conditions:
            if not self.evaluate_condition(condition):
                return False
        return True
    
        
        
    def resolve_operand(self, operand):
        if not isinstance(operand, str):
            return operand
        
        if operand in self.facts:
            return self.facts[operand]
        
        if "." in operand:
            return self.knowledge_base.get_value(operand)
        return operand
        
        
    def fire_rule(self, rule):
        
        changed = False
        
        actions = rule.get("actions", [])
        
        for action in actions:
            
            action_type = action["type"]
            
            if action_type == "derive_fact":
                fact = action["fact"]
                value = self.resolve_operand(action["value"])
                
                if self.facts.get(fact) != value:
                    self.derived_facts[fact] = value
                    self.facts[fact] = value
                    
                    changed = True
                
                
            elif action_type == "recommendation":
                

                recommendation_id = action["value"]

                recommendation = (
                    self.knowledge_base
                    .get_recommendations()
                    .get(recommendation_id)
                )
                
                recommendations = self.derived_facts.setdefault(
                    "recommendations",
                    []
                )
                if recommendation and recommendation not in recommendations:
                    recommendations.append({
                        "id":"recommendation_id",
                        "content":recommendation
                        
                    })
                    changed = True
                   
                
            elif action_type == "action_plan":
                    action_plan_id = action["value"]
                    
                    action_plan = (
                        self.knowledge_base
                        .get_action_plans()
                        .get(action_plan_id)
                    )
                    action_plans = self.derived_facts.setdefault(
                        "action_plans",
                        []
                    )
                    if action_plan and action_plan not in action_plans:
                        action_plans.append(action_plan)
                        changed = True
                        
            elif action_type == "investment_guidance":
                    guidance_id = action["value"]
                    
                    guidance = (
                        self.knowledge_base
                        .get_investment_guidance()
                        .get(guidance_id) 
                    )
                    guidance_list = self.derived_facts.setdefault(
                        "investment_guidance",
                        []
                    )
                    if guidance and guidance not in guidance_list:
                        guidance_list.append(guidance)
                        changed = True
        return changed
    
    
    def forward_chain(self):

        changed = True

        while changed:

            

        print("\n==========================")
        print("Starting Forward Chain Pass")
        print("==========================")

        for category_name, category in self.rules.items():

            print(f"\nCategory: {category_name}")

            for rule in category:

                rule_id = rule["id"]

                print(f"\nChecking Rule: {rule_id}")

                # Skip rules that have already fired
                if rule_id in self.fired_rules:
                    print(f"Rule {rule_id} already fired. Skipping.")
                    continue

                # Check whether the rule's conditions are satisfied
                if self.evaluate_rule(rule):

                    print(f"Rule {rule_id} conditions are TRUE.")

                    # Execute the rule's actions
                    if self.fire_rule(rule):

                        print(f"Rule {rule_id} FIRED.")
                        print("Derived Facts:", self.derived_facts)
                        print("Working Memory:", self.facts)

                        # Mark the rule as fired
                        self.fired_rules.add(rule_id)

                        # Continue another forward-chaining cycle
                        changed = True

                else:
                    print(f"Rule {rule_id} conditions are FALSE.")
               
    
   
            
            
            
                       

        
        
        
        
         
        
    
            
        