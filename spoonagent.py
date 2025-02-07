#!/usr/bin/env python3
"""
Recipe Recommendation Agent using smolagents
Author: Merouane Zouaid (kaito)

This script demonstrates how to build a recipe recommendation agent.
It leverages a custom tool that calls the Spoonacular API to fetch a recipe
suggestion based on available ingredients and an optional dietary preference.
After testing locally, you can share your tool to the Hub using the provided method.
"""

# inspect your agent runs with opentelementry

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from openinference.instrumentation.smolagents import SmolagentsInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor

endpoint = "http://localhost:6006/v1/traces"
trace_provider = TracerProvider()
trace_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(endpoint)))

SmolagentsInstrumentor().instrument(tracer_provider=trace_provider)



from typing import Optional
from smolagents import CodeAgent, HfApiModel, tool

@tool
def get_recipe(ingredients: str, diet: Optional[str] = None) -> str:
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

def main():
    # Create the agent using our custom recipe tool and a language model
    agent = CodeAgent(tools=[get_recipe], model=HfApiModel())

    # Example query for the agent
    query = (
        "I have chickpeas, lamb, dried apricots, olives, and couscous available. Can you suggest an authentic Moroccan recipe with spices commonly used in the region, like cumin, cinnamon, and paprika? I'd prefer something traditional like a tagine or vegetarian option if possible."
    )
    result = agent.run(query)
    print("Agent Response: ")
    print(result)

    get_recipe.save("get-recipe-tool")

    # To share your tool to the Hub, uncomment the following line and replace {your_username}:
    # get_recipe.push_to_hub("{your_username}/get-recipe-tool")

if __name__ == "__main__":
    main()
