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
def get_recipe(ingredients: str, diet: Optional[str] = None, laziness: Optional[int] = 5) -> str:
    """
    Gets a recipe suggestion based on provided ingredients, dietary preference, 
    and your laziness level (1=active chef, 10=super lazy). After finding a recipe, it
    retrieves detailed recipe information.
    
    Args:
        ingredients: A comma-separated string of available ingredients.
        diet: Dietary restrictions such as 'vegetarian', 'vegan', or 'gluten free'. Defaults to None.
        laziness: An integer from 1 (active) to 10 (super lazy); higher means recipes with quicker prep.
        
    Returns:
        A string with detailed information about the recommended recipe.
    """
    import os
    import requests

    api_key = os.getenv("SPOONACULAR_API_KEY")
    if not api_key:
        return "Spoonacular API key not set. Please set the SPOONACULAR_API_KEY environment variable."

    # Step 1: Search for recipes using the ingredients
    base_search_url = "https://api.spoonacular.com/recipes/findByIngredients"
    params = {
        "ingredients": ingredients,
        "number": 1,      # We want one suggestion
        "ranking": 1,
        "apiKey": api_key,
    }
    
    # Add diet if provided
    if diet:
        params["diet"] = diet
    
    # Incorporate the laziness factor: filter by maxReadyTime if needed.
    try:
        laziness = int(laziness)
    except ValueError:
        return "Laziness must be an integer from 1 to 10."
    if laziness >= 8:
        params["maxReadyTime"] = 15  # 15 minutes for super lazy cooks
    elif 5 <= laziness < 8:
        params["maxReadyTime"] = 30  # 30 minutes for moderately lazy cooks
    
    try:
        search_response = requests.get(base_search_url, params=params)
        search_response.raise_for_status()
        search_data = search_response.json()
    except Exception as e:
        return f"Error during recipe search: {e}"
    
    if not search_data:
        return "No recipes found with these parameters. Try adjusting your ingredients, diet, or laziness level."
    
    # Assume the first result is the best match
    recipe = search_data[0]
    recipe_id = recipe.get("id")
    if not recipe_id:
        return "Recipe ID not found in the search result."
    
    # Step 2: Retrieve detailed recipe information using the recipe id
    info_url = f"https://api.spoonacular.com/recipes/{recipe_id}/information"
    info_params = {
        "apiKey": api_key,
    }
    try:
        info_response = requests.get(info_url, params=info_params)
        info_response.raise_for_status()
        info_data = info_response.json()
    except Exception as e:
        return f"Error retrieving detailed recipe information: {e}"
    
    # Extract detailed information
    title = info_data.get("title", "Untitled Recipe")
    ready_time = info_data.get("readyInMinutes", "N/A")
    servings = info_data.get("servings", "N/A")
    instructions = info_data.get("instructions", "No instructions provided.")
    
    # Extract ingredients list (names only)
    ingredients_list = info_data.get("extendedIngredients", [])
    ingredients_names = [ing.get("name") for ing in ingredients_list if ing.get("name")]
    ingredients_str = ", ".join(ingredients_names) if ingredients_names else "N/A"
    
    # Build the detailed summary message
    detailed_info = (
        f"Recipe suggestion: {title}\n"
        f"Ready in: {ready_time} minutes | Servings: {servings}\n"
        f"Ingredients: {ingredients_str}\n\n"
        f"Instructions:\n{instructions}"
    )
    
    return detailed_info

def main():
    # Instantiate the agent using our detailed recipe tool and a language model.
    agent = CodeAgent(tools=[get_recipe], model=HfApiModel())

    # Example query:
    # "I have tofu, tomatoes, and basil. I'm vegetarian and super lazy (laziness=9)."
    query = (
        "I have tofu, tomatoes, and basil. I'm vegetarian and super lazy when it comes to cooking. "
        "What recipe do you recommend? return all recipe details, ready time, servings and instructions (Consider laziness level 9.)"
    )
    result = agent.run(query)
    print("Agent's Response:")
    print(result)

    get_recipe.save("my-fridge-tool")

    # To share your tool to the Hub, uncomment the following line and replace {your_username}:
    # get_recipe.push_to_hub("{your_username}/ai-recipe-recommender-tool")

if __name__ == "__main__":
    main()