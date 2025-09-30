import streamlit as st
from pathlib import Path
import time
import base64
from src.ingregenius.ingredients import INGREDIENT_DATABASE
from src.ingregenius.food_detector import get_ingredients_from_image
from src.ingregenius.recipe_generator import generate_two_recipes


# --- Function to Set Background and Theme ---
def set_background_and_theme(image_file):
    """
    Sets a background image, adds an overlay, and injects custom CSS for a full dark theme.
    """
    try:
        with open(image_file, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url("data:image/jpeg;base64,{encoded_string}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            [data-testid="stHeader"] {{
                background-color: transparent;
            }}
            body, .stApp, .stApp h1, .stApp h2, .stApp h3, p, label {{
                color: #FFFFFF !important;
            }}
            .stButton > button {{
                color: white;
                background-color: transparent;
                border: 2px solid white;
                border-radius: 10px;
                transition: all 0.3s ease;
            }}
            .stButton > button:hover {{
                background-color: rgba(255, 255, 255, 0.2);
            }}
            [data-testid="stFileUploadDropzone"] p {{
                color: #FFFFFF !important;
            }}
            .uploadedFileName {{
                color: #FFFFFF !important;
            }}
            [data-testid="stExpander"] summary {{
                color: #FFFFFF !important;
            }}
            [data-testid="stExpander"] summary svg {{
                color: #FFFFFF !important;
            }}
            div[data-baseweb="select"] > div {{
                background-color: rgba(255, 255, 255, 0.1) !important;
                border: 1px solid rgba(255, 255, 255, 0.5) !important;
                color: white !important;
            }}
            div[data-baseweb="select"] > div > div {{
                color: #ccc !important;
            }}
            div[data-baseweb="select"] svg {{
                color: white !important;
            }}
            .st-emotion-cache-1q8d0hz span {{
                 color: white !important;
            }}
            .st-emotion-cache-1o5dclc {{
                background-color: rgba(38, 39, 48, 0.95);
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error(f"Background image not found at path: {image_file}")


set_background_and_theme("./src/ingregenius/background_image.jpg")


def initialize_session_state():
    """Initializes session state variables if they don't exist."""
    if "page" not in st.session_state:
        st.session_state.page = "welcome"
    if "meal_type" not in st.session_state:
        st.session_state.meal_type = ""
    if "detected_ingredients" not in st.session_state:
        st.session_state.detected_ingredients = []
    if "final_ingredients" not in st.session_state:
        st.session_state.final_ingredients = []


def navigate_to(page_name):
    """Callback function to change the current page."""
    st.session_state.page = page_name


def welcome_page():
    st.title("Welcome to IngreGenius! ?")
    st.markdown("### Your AI-powered culinary compass.")
    st.write("Never wonder what to cook again. Just show me your ingredients, and I'll do the rest.")
    st.button("Get Started", on_click=navigate_to, args=("meal_selection",))


def meal_selection_page():
    st.title("What type of meal are you planning?")
    meal_type = st.radio(
        "Select one:",
        ("Breakfast", "Lunch", "Dinner"),
        key="meal_type_radio",
        horizontal=True,
        label_visibility="collapsed"
    )
    if st.button("Next"):
        st.session_state.meal_type = st.session_state.meal_type_radio
        navigate_to("upload")
        st.rerun()


def upload_page():
    st.title(f"Let's make {st.session_state.meal_type}!")
    st.subheader("Upload a picture of your ingredients")
    
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    
    if uploaded_file is not None:
        temp_dir = Path("temp_uploads")
        temp_dir.mkdir(exist_ok=True)
        image_path = temp_dir / uploaded_file.name
        
        with open(image_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
            
        st.image(str(image_path), caption="Image you uploaded.", use_container_width=True)
        
        with st.spinner("Analyzing your ingredients... This might take a moment."):
            detected_items = get_ingredients_from_image(str(image_path))
            st.session_state.detected_ingredients = detected_items
        
        st.success("Analysis complete!")
        time.sleep(1)
        navigate_to("confirmation")
        st.rerun()


def confirmation_page():
    st.title("Ingredient Confirmation")
    
    if not st.session_state.detected_ingredients:
        st.warning("I couldn't detect any ingredients. Please try another picture or add them manually.")
        st.session_state.detected_ingredients = []
    else:
        st.markdown("#### I found the following items:")
        tags = " ".join([f"`{item}`" for item in st.session_state.detected_ingredients])
        st.markdown(tags)

    st.markdown("---")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("All ingredients are recognized", use_container_width=True):
            st.session_state.final_ingredients = st.session_state.detected_ingredients
            navigate_to("recipe")
            st.rerun()
            
    with col2:
        if st.button("Add or remove ingredients", use_container_width=True):
            navigate_to("add_ingredients")
            st.rerun()


def add_ingredients_page():
    st.title("Refine Your Ingredient List")
    st.markdown("Add missing items from your pantry or remove misidentified ones.")
    
    current_ingredients = set(st.session_state.detected_ingredients)
    
    if st.session_state.detected_ingredients:
        items_to_keep = st.multiselect(
            "Detected Items (unselect to remove):",
            options=st.session_state.detected_ingredients,
            default=st.session_state.detected_ingredients
        )
        current_ingredients = set(items_to_keep)

    st.markdown("---")
    st.markdown("#### Add more ingredients:")
    
    added_ingredients = set()
    for category, items in INGREDIENT_DATABASE.items():
        with st.expander(category):
            selections = st.multiselect(f"Select from {category}:", options=items, key=category)
            added_ingredients.update(selections)
            
    final_list = sorted(list(current_ingredients.union(added_ingredients)))
    
    st.markdown("---")
    st.write("#### Your final ingredient list:")
    if final_list:
        tags = " ".join([f"`{item}`" for item in final_list])
        st.markdown(tags)
    else:
        st.warning("Your ingredient list is empty.")
    
    if st.button("Generate Recipes with this list", type="primary", use_container_width=True):
        st.session_state.final_ingredients = final_list
        navigate_to("recipe")
        st.rerun()


def recipe_page():
    st.title("Here are your custom recipes! ??")
    
    if not st.session_state.final_ingredients:
        st.error("No ingredients were selected. Please go back and add some ingredients.")
        if st.button("Go back"):
            navigate_to("add_ingredients")
            st.rerun()
        return

    with st.spinner("Your personal chef (the AI) is thinking..."):
        healthy_recipe, tasty_recipe = generate_two_recipes(
            st.session_state.meal_type,
            st.session_state.final_ingredients
        )
    
    st.balloons()
    
    tab1, tab2 = st.tabs(["  Healthy Dish  ", "  Tasty Dish  "])
    
    with tab1:
        st.markdown(healthy_recipe)
        
    with tab2:
        st.markdown(tasty_recipe)
        
    if st.button("Start Over"):
        for key in st.session_state.keys():
            del st.session_state[key]
        st.rerun()


initialize_session_state()

page_to_show = st.session_state.get("page", "welcome")

if page_to_show == "welcome":
    welcome_page()
elif page_to_show == "meal_selection":
    meal_selection_page()
elif page_to_show == "upload":
    upload_page()
elif page_to_show == "confirmation":
    confirmation_page()
elif page_to_show == "add_ingredients":
    add_ingredients_page()
elif page_to_show == "recipe":
    recipe_page()