import os
import roboflow
import random
from pathlib import Path
from dotenv import load_dotenv

# --- Configuration ---
load_dotenv()

ROBOFLOW_API_KEY = os.getenv("ROBOFLOW_API_KEY")
ROBOFLOW_WORKSPACE_ID = os.getenv("WORKSPACE_ID")
ROBOFLOW_PROJECT_ID = os.getenv("PROJECT_ID")

DATASET_PATH = Path("/home/atirmalle/Schreibtisch/Computer_Vision/Data/Dataset(to_be_labelled)/")
# --- End of Configuration ---

def upload_images_to_roboflow(api_key: str, workspace_id: str, project_id: str, dataset_dir: Path):
    """
    Uploads images from a directory structure to a Roboflow project.
    Each sub-directory in dataset_dir is treated as a class label.
    """
    rf = roboflow.Roboflow(api_key=api_key)
    project = rf.workspace(workspace_id).project(project_id)

    print(f"Connected to project: {project.name}")
    print("-" * 30)

    class_dirs = [d for d in dataset_dir.iterdir() if d.is_dir()]
    if not class_dirs:
        print(f"Error: No subdirectories found in {dataset_dir}. Please structure your data correctly.")
        return

    print(f"Found {len(class_dirs)} classes to upload.")

    for class_dir in class_dirs:
        label = class_dir.name.replace("\\", "-").replace(" ", "-").strip()
        print(f"\nProcessing Folder: '{class_dir.name}' -> Using Label: '{label}'")

        image_paths = list(class_dir.glob("*.jpg")) + list(class_dir.glob("*.png"))
        
        if not image_paths:
            print(f"  - No images found. Skipping.")
            continue
            
        print(f"  - Found {len(image_paths)} images. Starting upload...")

        batch_size = 100 
        for i in range(0, len(image_paths), batch_size):
            batch = image_paths[i:i + batch_size]
            
            for image_path in batch:
                try:
                    project.upload(
                        image_path=str(image_path),
                        split=random.choices(["train", "valid", "test"], [0.7, 0.2, 0.1], k=1)[0],
                        tag_names=[label]
                    )
                    print(f"    -> Uploaded: {image_path.name}")
                except Exception as e:
                    print(f"    - FAILED to upload {image_path.name}. Error: {e}")

    print("\n" + "-" * 30)
    print("? Upload process complete. Your next step is to annotate the images in the Roboflow UI.")

if __name__ == "__main__":
    if not all([ROBOFLOW_API_KEY, ROBOFLOW_WORKSPACE_ID, ROBOFLOW_PROJECT_ID]):
        print("Error: Missing environment variables. Check your .env file.")
    elif not DATASET_PATH.exists() or not DATASET_PATH.is_dir():
        print(f"Error: The dataset path '{DATASET_PATH}' does not exist.")
    else:
        upload_images_to_roboflow(
            api_key=ROBOFLOW_API_KEY,
            workspace_id=ROBOFLOW_WORKSPACE_ID,
            project_id=ROBOFLOW_PROJECT_ID,
            dataset_dir=DATASET_PATH
        )