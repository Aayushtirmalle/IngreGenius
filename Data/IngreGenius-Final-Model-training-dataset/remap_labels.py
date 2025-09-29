# remap_labels.py
from pathlib import Path
import shutil
import yaml  # You might need to install this: pip install pyyaml

# --- CONFIGURATION ---

# 1. Path to your master list of class names.
MASTER_CLASSES_FILE = Path("./Data/IngreGenius-Final-Model-training-dataset/master_classes.txt")

# 2. --- IMPORTANT ---
#    Define your source datasets. Update these paths to the absolute paths
#    of your original dataset's .yaml files.
SOURCE_DATASETS = [
    {
        "name": "Fridge objects.v12i.yolov8",
        "yaml_path": Path("/home/atirmalle/Schreibtisch/Computer_Vision/Data/Fridge objects.v12i.yolov8/data.yaml")
    },
    {
        "name": "Grocery_YOLO_Dataset_Small",
        "yaml_path": Path("/home/atirmalle/Schreibtisch/Computer_Vision/Data/Grocery_YOLO_Dataset_Small/Grocery_YOLO_Dataset_Small/dataset.yaml")
    },
    {
        "name": "IngreGenius-Raw-Uploads.v1i.yolov8",
        "yaml_path": Path("/home/atirmalle/Schreibtisch/Computer_Vision/Data/IngreGenius-Raw-Uploads.v1i.yolov8/data.yaml")
    },
]

# 3. Define a NEW location to save the remapped labels.
#    This keeps your original data safe.
REMAPPED_LABELS_DIR = Path("./Data/IngreGenius-Final-Model-training-dataset/master_labels")

# --- SCRIPT LOGIC ---

def load_class_list_from_txt(file_path):
    """Loads a list of classes from a simple text file."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines() if line.strip()]

def load_class_list_from_yaml(yaml_path):
    """Loads the 'names' list from a YOLO data.yaml file."""
    with open(yaml_path, 'r') as f:
        data = yaml.safe_load(f)
        return data.get('names', [])

if __name__ == "__main__":
    if REMAPPED_LABELS_DIR.exists():
        print(f"Clearing old remapped labels directory: {REMAPPED_LABELS_DIR}")
        shutil.rmtree(REMAPPED_LABELS_DIR)
    
    # Load the master class list and create a mapping from name to new index
    master_classes = load_class_list_from_txt(MASTER_CLASSES_FILE)
    master_map = {name.lower(): i for i, name in enumerate(master_classes)}
    print(f"Loaded {len(master_classes)} master classes.")

    # Loop through each source dataset
    for dataset in SOURCE_DATASETS:
        print(f"\nProcessing dataset: {dataset['name']}...")
        
        original_yaml_path = dataset["yaml_path"]
        if not original_yaml_path.exists():
            print(f"  - ERROR: YAML file not found at {original_yaml_path}. Skipping.")
            continue
            
        original_classes = load_class_list_from_yaml(original_yaml_path)
        dataset_root = original_yaml_path.parent

        label_files = list(dataset_root.rglob("labels/**/*.txt"))
        print(f"Found {len(label_files)} label files to remap.")

        for label_file in label_files:
            new_label_lines = []
            with open(label_file, 'r') as f:
                for line in f.readlines():
                    parts = line.strip().split()
                    if not parts: continue
                    
                    old_class_index = int(parts[0])
                    original_class_name = original_classes[old_class_index].lower()
                    
                    if original_class_name in master_map:
                        new_class_index = master_map[original_class_name]
                        new_line = f"{new_class_index} {' '.join(parts[1:])}"
                        new_label_lines.append(new_line)
                    else:
                        print(f"  - WARNING: Class '{original_class_name}' not in master list. Skipping.")

            # Save the remapped file to a new, parallel directory structure
            relative_path = label_file.relative_to(dataset_root)
            new_label_path = REMAPPED_LABELS_DIR / dataset['name'] / relative_path
            new_label_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(new_label_path, 'w') as f:
                f.write("\n".join(new_label_lines))

    print("\n Label remapping complete!")
    print(f"All new label files are saved in '{REMAPPED_LABELS_DIR}'.")
    print("\nYour next step is to update your training script to use your 'master_data.yaml' file.")