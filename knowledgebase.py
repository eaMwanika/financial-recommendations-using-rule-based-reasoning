import json
from pathlib import Path


class KnowledgeBase:
    """
    Loads and provides access to the knowledge base.
    """

    def __init__(self, filename="knowledge.json"):
        self.filename = Path(filename)
        self.data = self.load()

    def load(self):
        """Load the JSON knowledge base."""
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



    def get_metadata(self):
        return self.data.get("metadata", {})

    def get_budget_model(self):
        metadata = self.get_metadata()
        return metadata.get("budget_model", {})

    def get_debt_ratio_limit(self):
        metadata = self.get_metadata()
        return metadata.get("debt_ratio_limit", 0.30)

    def get_emergency_months(self):
        metadata = self.get_metadata()
        return metadata.get("emergency_months", 6)


    def get_inference_rules(self):
        return self.data.get("inference_rules", [])

    def get_recommendation_rules(self):
        return self.data.get(
            "recommendation_rules",
            []
        )

    

    def reload(self):
        """Reload the knowledge base from disk."""
        self.data = self.load()