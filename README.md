# IngreGenius: The AI-Powered Culinary Compass

**Just open your fridge and ask. IngreGenius is a smart kitchen assistant that transforms a photo of your refrigerator's contents into delicious, categorized recipe suggestions.**

## Contents
- [Project Description](#project-description)
- [Getting Started](#getting-started)
- [Core Features](#core-features)
- [Main Goals & Objectives](#main-goals--objectives)
- [How It Works: The Pipeline](#how-it-works-the-pipeline)
- [Technology Stack](#technology-stack)
- [Results or Output](#results-or-output)



## Project Description

This project addresses the common dilemma of "what can I make with what I have?" by bridging the gap between computer vision and natural language processing. IngreGenius first uses a **YOLOv8 object detection model** to identify food items from a user-uploaded image. It then intelligently analyzes this list of ingredients to determine available meal categories (like Breakfast, Lunch, Dinner, or Sweet Dishes) based on key components. Finally, it leverages the **Deepseek large language model** via OpenRouter to generate creative and practical recipes tailored to the user's choice.

## Core Features

-   **AI-Powered Ingredient Detection:** Utilizes a YOLOv8 model to accurately identify and list multiple food items from a single image.
-   **Smart Meal Categorization:** Implements a logic engine to analyze the ingredient list and unlock relevant meal categories. For example, the presence of sugar or fruit unlocks "Sweet Dishes," while eggs suggest "Breakfast."
-   **Dynamic Recipe Generation:** Sends a context-aware prompt to the Deepseek LLM to generate high-quality recipes based on the detected ingredients and the user's chosen meal type.
-   **User-Friendly Interface:** Provides a simple web interface (built with Streamlit) for users to upload an image and receive instant recipe inspiration.

## Main Goals & Objectives

The primary goal of this project is to build a practical, end-to-end AI application that solves a real-world problem. The key objectives are:

1.  **Integrate Multiple AI Models:** To successfully combine a computer vision model (YOLOv8) for perception with a large language model (Deepseek) for creative generation.
2.  **Implement Context-Aware Logic:** To move beyond a simple input-output pipeline by adding an analysis layer that provides intelligent, categorized suggestions to the user.
3.  **Build a Full-Stack Application:** To develop a complete system, from the backend AI processing to a user-facing frontend interface.
4.  **Explore Modern AI Tools:** To gain hands-on experience with state-of-the-art technologies like YOLOv8, large language models, and APIs like OpenRouter.

## How It Works: The Pipeline

1.  **Image Upload:** The user provides a photo of their fridge or pantry.
2.  **Object Detection:** The YOLOv8 model processes the image and outputs a list of detected ingredients.
3.  **Ingredient Analysis:** A backend Python script checks the list for "enabling" ingredients (e.g., eggs, flour, sugar) to determine which meal categories are available.
4.  **User Selection:** The user is presented with the available categories (e.g., "Generate Breakfast Recipe").
5.  **Prompt Engineering:** A specific, contextual prompt is constructed and sent to the Deepseek LLM via the OpenRouter API.
6.  **Recipe Generation:** The LLM creates a tailored recipe, which is then displayed to the user in the interface.

## Technology Stack

-   **Backend:** Python
-   **Computer Vision:** PyTorch, YOLOv8
-   **NLP / Recipe Generation:** Deepseek LLM, OpenRouter API, OpenAI Python Library
-   **Frontend:** Streamlit
-   **Data:** Custom-trained on a public food detection dataset from Roboflow/Kaggle

## Getting Started

For detailed instructions on how to set up and run this project, check out the [Getting Started Guide](GETTING_STARTED.md).

## Results or Output

For detailed results and examples of the project's functionality, check out the [Results or Output Page](RESULTS.md).
