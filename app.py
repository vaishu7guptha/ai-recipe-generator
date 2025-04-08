# (Paste your entire code here)
import streamlit as st
from openai import OpenAI
import re
import time
from typing import Dict, Optional

# Setup page configuration
st.set_page_config(page_title="AI Recipe Generator 🍲", page_icon="🍽️", layout="centered")

# Inject CSS for styling
st.markdown("""
 <style>
 .main {
     background-color: #fdfcfb;
     padding: 20px;
 }
 h1, h2, h3 {
     color: #333333;
 }
 .stTextInput>div>div>input {
     font-size: 18px;
     padding: 10px;
 }
 .stButton>button {
     background-color: #f77f00;
     color: white;
     padding: 10px 24px;
     border-radius: 12px;
     font-size: 16px;
 }
 .stButton>button:hover {
     background-color: #fcbf49;
     color: black;
 }
 </style>
""", unsafe_allow_html=True)

# Initialize OpenRouter client with your API key (hardcoded for testing)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="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",
)

def openrouter_chat_completion(prompt: str) -> Optional[str]:
    try:
        # Call the chat completions endpoint with extra headers (customize as needed)
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "<YOUR_SITE_URL>",   # Optional: e.g., "https://myrecipesite.com"
                "X-Title": "<YOUR_SITE_NAME>"          # Optional: e.g., "My Recipe Generator"
            },
            extra_body={},
            model="meta-llama/llama-3.3-70b-instruct:free",
            messages=[{"role": "user", "content": prompt}],
            temperature=1,
            max_completion_tokens=1024,
            top_p=1,
            stream=False,  # Change to True to handle streaming responses if desired
            stop=None,
        )
        # Return generated text from the first choice
        return completion.choices[0].message.content
    except Exception as e:
        st.error(f"OpenRouter API error: {e}")
        return None

def generate_recipe(ingredients: str) -> Optional[Dict]:
    # Create a prompt that instructs the model to generate a structured recipe output
    prompt = f"""Generate a detailed and creative recipe using the following ingredients: {ingredients}.
Format the response exactly like this:
Title: <Recipe Title>
Ingredients:
- item1
- item2
Instructions:
1. step1
2. step2
"""
    response_text = openrouter_chat_completion(prompt)
    if response_text:
        return parse_recipe(response_text)
    return None

def parse_recipe(response_text: str) -> Dict:
    # Use regular expressions to parse the structured output
    title_match = re.search(r"Title:\s*(.+)", response_text)
    ingredients_matches = re.findall(r"-\s*(.+)", response_text)
    instructions_matches = re.findall(r"\d+\.\s*(.+)", response_text)
    
    return {
        "title": title_match.group(1).strip() if title_match else "Delicious Dish",
        "ingredients": [i.strip() for i in ingredients_matches] if ingredients_matches else [],
        "instructions": [i.strip() for i in instructions_matches] if instructions_matches else []
    }

def display_recipe(recipe: Dict):
    st.success("Here's your recipe!")
    # Display a dynamic image based on the ingredients
    st.image(f"https://source.unsplash.com/800x400/?{', '.join(recipe['ingredients'])},food", use_column_width=True)
    st.markdown(f"### Title: {recipe['title']}")
    st.markdown("#### Ingredients:")
    st.markdown("\n".join([f"- {item}" for item in recipe['ingredients']]))
    st.markdown("#### Instructions:")
    for idx, step in enumerate(recipe['instructions'], 1):
        st.markdown(f"**Step {idx}:** {step}")
    
    recipe_text = (
        f"Title: {recipe['title']}\n\nIngredients:\n" +
        "\n".join([f"- {i}" for i in recipe['ingredients']]) +
        "\n\nInstructions:\n" +
        "\n".join([f"{i+1}. {s}" for i, s in enumerate(recipe['instructions'])])
    )
    st.download_button("📄 Download Recipe", recipe_text, file_name="recipe.txt")

def main():
    st.title("🍕 Recipe Generator")
    st.subheader("Enter ingredients and get a custom recipe!")
    
    user_input = st.text_input("Enter ingredients (comma-separated):", "chicken, pasta, tomatoes")
    
    if st.button("Generate Recipe"):
        cleaned_input = user_input.strip()
        if cleaned_input:
            with st.spinner("Cooking up a recipe for you..."):
                time.sleep(2)  # Simulate some delay
                recipe = generate_recipe(cleaned_input)
            if recipe:
                display_recipe(recipe)
            else:
                st.error("Recipe generation failed. Please try again.")
        else:
            st.warning("Please enter some ingredients to generate a recipe.")
    
    st.markdown("---")
    st.markdown("Made with ❤️ by Vaishnavi Bejgam")

if __name__ == "__main__":
    main()
