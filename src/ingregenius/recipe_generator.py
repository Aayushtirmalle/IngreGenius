import os
import time
from openai import OpenAI
from dotenv import load_dotenv

# --- Configuration ---
# Load environment variables from the .env file in your project root
load_dotenv()

# Securely get your OpenRouter API key (using the name from your file)
OPENROUTER_API_KEY = os.getenv("LLM_API_KEY")

def generate_two_recipes(meal_type: str, ingredients: list[str]) -> tuple[str, str]:
    """
    Connects to the Deepseek LLM via OpenRouter to generate two distinct recipes
    using a single, efficient API call.
    """
    if not OPENROUTER_API_KEY:
        error_message = "Error: LLM_API_KEY not found. Please check your .env file."
        print(error_message)
        return error_message, error_message

    try:
        # --- Initialize the API Client for OpenRouter ---
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )

        ingredients_str = ", ".join(ingredients)
        
        # --- Construct a Single, Combined Prompt ---
        print("Generating two recipes with a single API call...")
        response = client.chat.completions.create(
            model="deepseek/deepseek-r1:free", 
            messages=[
                {"role": "system", "content": "You are a creative and helpful chef. You will generate two distinct recipes based on the user's request and separate them with a specific marker."},
                {"role": "user", "content": f"""
                    Generate TWO distinct recipes for **{meal_type}** using the available ingredients: **{ingredients_str}**.
                    You can assume common pantry staples are also available.

                    **Recipe 1: Healthy and Diet-Conscious**
                    Focus on fresh ingredients, low-fat cooking methods, and high nutritional value.

                    **Recipe 2: Tasty and Flavorful**
                    Prioritize taste and satisfaction. Feel free to use butter, cheese, or other rich ingredients.
                    
                    Please format both outputs in Markdown with a title, ingredients, and instructions.
                    
                    **IMPORTANT:** After the first recipe, place the exact separator `---SEPARATOR---` before starting the second recipe.
                """}
            ]
        )
        
        full_response = response.choices[0].message.content

        # --- Split the Response into Two Recipes ---
        separator = "---SEPARATOR---"
        if separator in full_response:
            parts = full_response.split(separator, 1)
            healthy_recipe = parts[0].strip()
            tasty_recipe = parts[1].strip()
        else:
            # Fallback in case the LLM doesn't follow instructions perfectly
            healthy_recipe = full_response
            tasty_recipe = "Sorry, I had trouble generating the second recipe. Please try again."

        return healthy_recipe, tasty_recipe

    except Exception as e:
        print(f"An error occurred while calling the LLM: {e}")
        error_message = f"Sorry, I couldn't generate recipes at the moment. The API returned an error. Please check the console for details."
        return error_message, error_message


# --- This block allows you to test the file directly ---
if __name__ == '__main__':
    print("--- Testing recipe_generator.py ---")
    test_meal = "Dinner"
    test_ingredients = ["Chicken Breast", "Tomato", "Onion", "Cheese", "Spinach"]
    
    healthy, tasty = generate_two_recipes(test_meal, test_ingredients)
    
    print("\n" + "="*20 + " HEALTHY RECIPE " + "="*20)
    print(healthy)
    
    print("\n" + "="*20 + " TASTY RECIPE " + "="*20)
    print(tasty)