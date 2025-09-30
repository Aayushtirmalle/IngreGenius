from ultralytics import YOLO
from pathlib import Path

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
    if not MODEL_PATH.exists():
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")

    model = YOLO(MODEL_PATH)

    results = model.predict(source=image_path, verbose=False)

    detected_names = set()

    result = results[0]

    for box in result.boxes:
        class_id = int(box.cls)
        object_name = result.names[class_id]
        detected_names.add(object_name)

    return list(detected_names)

# --- This block allows testing the function directly ---
if __name__ == '__main__':
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