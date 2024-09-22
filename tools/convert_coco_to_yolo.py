import json
import os
import argparse

def convert_coco_to_yolo(coco_json_path, output_dir, image_dir):
    """
    Convert COCO format annotations to YOLO format.

    Args:
        coco_json_path (str): Path to the COCO JSON annotations file.
        output_dir (str): Directory where YOLO annotation files will be saved.
        image_dir (str): Directory containing the images (not directly used, 
                         but can be useful for future extensions).

    The output YOLO annotation files will be created with the same base name 
    as the corresponding image files and will contain lines formatted as:
    <class_id> <x_center> <y_center> <width> <height>
    
    Where class_id is 0-indexed, and the coordinates are normalized to 
    the image size.
    """

    # Load COCO JSON file
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Create a dictionary to store image dimensions (width, height)
    image_info = {}
    for img in coco_data['images']:
        image_info[img['id']] = {
            'file_name': img['file_name'],
            'width': img['width'],
            'height': img['height']
        }
    
    # Loop through annotations
    for annotation in coco_data['annotations']:
        image_id = annotation['image_id']
        category_id = annotation['category_id']
        bbox = annotation['bbox']  # COCO format: [x_min, y_min, width, height]
        
        # Get image dimensions
        image_width = image_info[image_id]['width']
        image_height = image_info[image_id]['height']
        
        # Convert COCO format to YOLO format
        x_min, y_min, width, height = bbox
        x_center = (x_min + width / 2) / image_width
        y_center = (y_min + height / 2) / image_height
        norm_width = width / image_width
        norm_height = height / image_height
        
        # Create a label file for the image (same name as image but .txt extension)
        image_name = image_info[image_id]['file_name']
        label_file_name = os.path.splitext(image_name)[0] + '.txt'
        label_file_path = os.path.join(output_dir, label_file_name)
        
        # Write YOLO annotation: [class_id, x_center, y_center, width, height]
        with open(label_file_path, 'a') as label_file:
            label_file.write(f"{category_id - 1} {x_center:.6f} {y_center:.6f} {norm_width:.6f} {norm_height:.6f}\n")

def main():
    parser = argparse.ArgumentParser(description="Convert COCO annotations to YOLO format.")
    parser.add_argument('--coco', type=str, required=True, help='Path to COCO JSON annotations file.')
    parser.add_argument('--output', type=str, required=True, help='Path to output YOLO annotations directory.')
    parser.add_argument('--images', type=str, required=True, help='Path to directory containing the images.')
    
    args = parser.parse_args()
    
    convert_coco_to_yolo(args.coco, args.output, args.images)

if __name__ == "__main__":
    main()