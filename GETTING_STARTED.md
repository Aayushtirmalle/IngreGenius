# Getting Started

Follow these simple steps to set up and reproduce the IngreGenius project. No prior coding knowledge is required!

---

## Step 1: Clone the Project Repository

1. Open a terminal.
2. Run the following command to download the project:
   ```
   git clone https://github.com/Aayushtirmalle/IngreGenius.git
   ```
3. Navigate to the project folder:
   ```
   cd IngreGenius
   ```

---

## Step 2: Install Dependency Manager

1. **Install Poetry** (Dependency Manager):
   - Open a terminal (Command Prompt or PowerShell).
   - Run the following command:
     ```
     pip install poetry
     ```


---


## Step 3: Set Up the Environment

1. **Install Dependencies**:
   - Run the following command to install all required libraries:
     ```
     poetry install
     ```

2. **Create an LLM API Key**:
   - Visit [OpenRouter API Keys](https://openrouter.ai/settings/keys).
   - Sign in or create an account if you don’t have one.
   - Generate a new API key to use the "deepseek/deepseek-r1:free" model used in this project.

3. **Set Up API Keys**:
   - Create/Open the `.env` file in the project's root directory.
   - Paste your generated API key in place of the placeholder `LLM_API_KEY`.

   the .env file should look like this 
   ```
    # .env file
    LLM_API_KEY="paste your API Key here"
   ```

---

## Step 4: Run the Application

1. Start the application by running:
   ```
   poetry run streamlit run app.py
   ```
2. Open the link displayed in the terminal (usually `http://localhost:8501`) in your web browser.

---

## Step 5: Use the Application

1. Upload an image of your fridge or pantry.
2. Follow the on-screen instructions to:
   - Confirm detected ingredients.
   - Generate recipes based on your selected meal type.

<em>(Fyi the folder "Images_for_testing" contains some sample images which can be used for testing purpose (but not compulsory))</em>

---

Congratulations! You have successfully set up and run the IngreGenius project.
