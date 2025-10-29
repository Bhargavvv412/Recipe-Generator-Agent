import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
# We don't need 'os' or 'dotenv' anymore
# import os
# from dotenv import load_dotenv

# --- Prompt Engineering ---
# (Putting this function at the top)
def create_recipe_prompt(ingredients_list):
    """Creates a robust prompt for the recipe generation agent."""
    
    prompt_template = f"""
    You are a creative and practical "What's in my Fridge" chef. Your one and only task is to generate a complete recipe using **only** the ingredients provided by the user.

    **User's Ingredients:**
    {ingredients_list}

    **Your Constraints & Rules:**
    1.  **Strict Ingredient Use:** You MUST create a recipe using *only* the ingredients from the list. Do not add any new food items (e.g., if they list "chicken" but not "onion", you cannot use onion).
    2.  **Basic Staples:** You MAY assume the user has basic pantry staples: **salt, black pepper, cooking oil (like olive or vegetable oil), and water.** You must state which of these staples you used in a "Note" section.
    3.  **No Shopping:** Do not suggest ingredients the user "might want to add." Use what you're given.
    4.  **Formatting:** You must format the output in clean, easy-to-read Markdown.
    5.  **Impossible Request:** If the ingredients are nonsensical (e.g., "a shoe, some gravel, and a battery") or just water, respond with a witty, food-related refusal, not a recipe.
    
    **Required Output Format:**

    **Recipe Name:** [Your creative name for the dish]
    
    **Description:** [A brief, appetizing one-sentence description]
    
    **Ingredients Used:**
    * [Ingredient 1 from the user's list]
    * [Ingredient 2 from the user's list]
    * ...

    **Instructions:**
    1.  [Clear, step-by-step instruction 1]
    2.  [Clear, step-by-step instruction 2]
    3.  [...and so on]
    
    **Note:** [Mention any assumed basic staples here (e.g., "I assumed you have salt, pepper, and olive oil.")]

    ---
    Generate the recipe now.
    """
    return prompt_template

# --- Streamlit App UI ---
st.set_page_config(page_title="Day 29: Recipe Agent", layout="centered")
st.title("🧑‍🍳 Day 29: The Recipe Generator Agent")

# --- API Key Input in Sidebar ---
st.sidebar.header("Configuration")
user_api_key = st.sidebar.text_input("Enter your Google API Key:", type="password")

# --- Main App Logic ---
if not user_api_key:
    st.info("Please enter your Google API Key in the sidebar to start.")
    st.stop() # Stop the app if no key is provided

# --- Initialize the LLM (only after key is provided) ---
try:
    # NOTE: I fixed the model name. It's 'gemini-1.5-flash', not '2.5'.
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.7, api_key=user_api_key)
except Exception as e:
    st.error(f"Error initializing the AI model: {e}")
    st.error("This often means the API key is invalid or not enabled for the Gemini API.")
    st.stop() # Stop if the key is bad

# --- Show the rest of the app ---
st.markdown("List your ingredients (one per line or separated by commas), and I'll invent a recipe for you.")

with st.form("recipe_form"):
    ingredients_input = st.text_area("Enter your ingredients:", height=150, 
                                     placeholder="e.g.,\nOnion\nGarlic\nCanned tomatoes\nSpinach\nRice")
    
    submitted = st.form_submit_button("Generate Recipe")

if submitted and ingredients_input:
    with st.spinner("Consulting the culinary muses..."):
        try:
            # Create the prompt
            prompt = create_recipe_prompt(ingredients_input)
            
            # Call the LLM
            response = llm.invoke(prompt)
            
            # Display the result
            st.divider()
            st.subheader("Here's your custom recipe:")
            st.markdown(response.content)
        
        except Exception as e:
            st.error(f"An error occurred while generating the recipe: {e}")

elif submitted and not ingredients_input:
    st.warning("You can't cook with nothing! Please enter some ingredients.")