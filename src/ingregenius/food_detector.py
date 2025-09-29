from ultralytics import YOLO
from pathlib import Path

# Define the path to your trained model weights
# We use Path for better cross-platform compatibility (Windows/Mac/Linux)
MODEL_PATH = Path(__file__).resolve().parent.parent / 'models' / 'IngreGenius_SuperModel_Run13' / 'weights' / 'best.pt'

def get_ingredients_from_image(image_path: str) -> list[str]:
    """
    Takes the path to an image, runs inference using the trained YOLOv8 model,
    and returns a clean list of unique detected ingredient names.

    Args:
        image_path (str): The file path of the image to analyze.

    Returns:
        list[str]: A list of unique ingredient names found in the image.
    """
    # --- Step 1: Check if the model file exists ---
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

    # --- Step 2: Load Your Custom-Trained Model ---
    # This is where you load the 'best.pt' file you generated during training.
    model = YOLO(MODEL_PATH)

    # --- Step 3: Perform Inference on the Image ---
    # The model.predict() method is used for inference.
    results = model.predict(source=image_path, verbose=False) # verbose=False cleans up the output

    # --- Step 4: Extract the Names of Detected Objects ---
    detected_names = set()  # Using a set to automatically handle duplicates

    # The result is a list, but we usually process one image at a time, so we take the first element
    result = results[0]

    # Each detected object has a class ID (cls)
    for box in result.boxes:
        class_id = int(box.cls)
        # result.names gives a dictionary like {0: 'Apple', 1: 'Banana', ...}
        # We use the class_id to look up the object's name.
        object_name = result.names[class_id]
        detected_names.add(object_name)

    return list(detected_names)

# --- This block allows you to test the function directly ---
if __name__ == '__main__':
    # You need a test image. Find one in your dataset's 'valid/images' folder.
    # IMPORTANT: Make sure the relative path is correct for your project structure.
    test_image = '/home/atirmalle/Schreibtisch/Computer_Vision/IngreGenius/Data/Fridge objects.v12i.yolov8/test/images/img8_png.rf.ac8d6693193d5725f27ac49eb2234669.jpg'

    try:
        ingredients = get_ingredients_from_image(test_image)
        if ingredients:
            print("Detected Ingredients:")
            print(ingredients)
        else:
            print("No ingredients were detected in the image.")
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")