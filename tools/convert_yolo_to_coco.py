import os
import json
import argparse
from PIL import Image

"""
python yolo_to_coco.py --yolo_annotations path/to/yolo/annotations \
                       --images_dir path/to/images \
                       --output_json path/to/output/coco_annotations.json \
                       --categories "person,car,dog"
"""

def yolo_to_coco_bbox(bbox, img_width, img_height):
    """
    Convert YOLO bbox format (center_x, center_y, width, height)
    to COCO format (x_min, y_min, width, height).
    
    YOLO format is normalized, so denormalize using image dimensions.
    """
    center_x, center_y, bbox_width, bbox_height = bbox
    x_min = (center_x - bbox_width / 2) * img_width
    y_min = (center_y - bbox_height / 2) * img_height
    width = bbox_width * img_width
    height = bbox_height * img_height
    return [x_min, y_min, width, height]

def convert_yolo_to_coco(yolo_annotations_path, images_dir, output_json_path, category_names):
    """
    Convert YOLO annotations to COCO format and save to a JSON file.
    
    Args:
    - yolo_annotations_path: path to the folder containing YOLO .txt files.
    - images_dir: path to the folder containing the corresponding images.
    - output_json_path: path to save the output COCO annotations JSON file.
    - category_names: list of category names corresponding to class ids in YOLO.
    """
    coco_output = {
        "images": [],
        "annotations": [],
        "categories": []
    }
    
    # Add categories
    for i, category_name in enumerate(category_names):
        coco_output['categories'].append({
            "id": i,
            "name": category_name,
            "supercategory": "none"
        })
    
    annotation_id = 0  # unique ID for each annotation
    for idx, yolo_file in enumerate(os.listdir(yolo_annotations_path)):
        if not yolo_file.endswith(".txt"):
            continue

        # Get the corresponding image file
        image_file = yolo_file.replace(".txt", ".jpg")
        image_path = os.path.join(images_dir, image_file)
        
        # Open the image to get its dimensions
        img = Image.open(image_path)
        img_width, img_height = img.size
        
        # Add image information to COCO output
        image_id = idx
        coco_output['images'].append({
            "id": image_id,
            "file_name": image_file,
            "width": img_width,
            "height": img_height
        })
        
        # Read YOLO annotations
        yolo_file_path = os.path.join(yolo_annotations_path, yolo_file)
        with open(yolo_file_path, 'r') as f:
            lines = f.readlines()
        
        # Parse each line in YOLO annotation file
        for line in lines:
            class_id, center_x, center_y, bbox_width, bbox_height = map(float, line.split())
            # Convert YOLO bbox to COCO format
            coco_bbox = yolo_to_coco_bbox([center_x, center_y, bbox_width, bbox_height], img_width, img_height)
            
            # Add annotation to COCO output
            coco_output['annotations'].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": int(class_id),
                "bbox": coco_bbox,
                "area": coco_bbox[2] * coco_bbox[3],  # width * height
                "iscrowd": 0
            })
            annotation_id += 1

    # Save COCO format annotations to a JSON file
    with open(output_json_path, 'w') as output_json_file:
        json.dump(coco_output, output_json_file, indent=4)

def parse_args():
    """
    Parse command line arguments.
    """
    parser = argparse.ArgumentParser(description="Convert YOLO annotations to COCO format.")
    parser.add_argument("--yolo_annotations", type=str, required=True, help="Path to YOLO annotations folder")
    parser.add_argument("--images_dir", type=str, required=True, help="Path to images folder")
    parser.add_argument("--output_json", type=str, required=True, help="Path to save the output COCO JSON file")
    parser.add_argument("--categories", type=str, required=True, help="Comma-separated category names (e.g., 'person,car,dog')")
    
    return parser.parse_args()

def main():
    # Parse command line arguments
    args = parse_args()
    
    # Get list of category names
    category_names = args.categories.split(',')
    
    # Convert YOLO to COCO format
    convert_yolo_to_coco(args.yolo_annotations, args.images_dir, args.output_json, category_names)

if __name__ == "__main__":
    main()
