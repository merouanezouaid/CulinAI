from smolagents import Tool
from typing import Optional

class SimpleTool(Tool):
    name = "CulinAI -- your AI Recipe Assistant"
    description = "Gets a recipe suggestion based on the provided ingredients and dietary preference."
    inputs = {"ingredients":{"type":"string","description":"A comma-separated string of available ingredients."},"diet":{"type":"string","nullable":True,"description":"Dietary restrictions such as 'vegetarian', 'vegan', or 'gluten free'. Defaults to None."}}
    output_type = "string"

    def forward(self, ingredients: str, diet: Optional[str] = None) -> str:
        """
        Gets a recipe suggestion based on the provided ingredients and dietary preference.

        Args:
            ingredients: A comma-separated string of available ingredients.
            diet: Dietary restrictions such as 'vegetarian', 'vegan', or 'gluten free'. Defaults to None.
        """
        import os
        import requests

        # Retrieve your Spoonacular API key from the environment
        api_key = os.getenv("SPOONACULAR_API_KEY")
        if not api_key:
            return "Spoonacular API key not set. Please set the SPOONACULAR_API_KEY environment variable."

        base_url = "https://api.spoonacular.com/recipes/findByIngredients"
        params = {
            "ingredients": ingredients,
            "number": 1,      # Retrieve one recipe suggestion
            "ranking": 1,
            "apiKey": api_key,
        }
        if diet:
            params["diet"] = diet

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            if not data:
                return "No recipes found with these ingredients and dietary restrictions."
            recipe = data[0]
            title = recipe.get("title", "Untitled Recipe")
            used_count = recipe.get("usedIngredientCount", 0)
            missed_count = recipe.get("missedIngredientCount", 0)
            return (f"Recipe suggestion: {title} "
                    f"(used {used_count} of your ingredients, missing {missed_count} additional ingredient(s)).")
        except Exception as e:
            return f"Error occurred: {e}"