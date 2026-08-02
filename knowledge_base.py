import json
from pathlib import Path


class KnowledgeBase:
   # LOading json

    def __init__(self, filename="knowledge.json"):
        self.filename = Path(filename)
        self.data = self.load()

    def load(self):
        #Load the JSON knowledge base.#
        try:
            with open(self.filename, "r", encoding="utf-8") as file:
                return json.load(file)

        except FileNotFoundError:
            raise FileNotFoundError(
                f"Knowledge base '{self.filename}' not found."
            )

        except json.JSONDecodeError as e:
            raise ValueError(
                f"Invalid JSON format: {e}"
            )

    
    def get_system(self):
        # return system information#
        return self.data.get("system", {})
    
    def get_financial_thresholds(self):
        return self.data.get("financial_thresholds", {})
    
    def get_recommendations(self):
        return self.data.get("recommendations",{})
    
    def get_action_plans(self):
        return self.data.get("action_plans", {})
    
    def get_investment_guidance(self):
        return self.data.get("investment_guidance", {})
    
    def get_rules(self):
        return self.data.get("rules", {})
    
    def get_value(self,path):
        current = self.data
        
        for key in path.split("."):
            if isinstance(current, dict) and key in current:
                current = current[key]
            else:
                raise KeyError(
                    f"Knowledge path '{path}' not found."
                )
        return current
    




    def reload(self):
       
        self.data = self.load()