import cv2
import os
import argparse

"""
python script_name.py videos/palace.mp4 output_images
"""

def convert_video_to_images(video_path, output_folder):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Create the output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    frame_count = 0
    while True:
        ret_val, frame = cap.read()
        if ret_val:
            # Save the frame as an image file
            image_name = f"frame_{frame_count:05d}.png"  # Name format: frame_00000.png
            image_path = os.path.join(output_folder, image_name)
            cv2.imwrite(image_path, frame)
            frame_count += 1
        else:
            break
    
    cap.release()
    print(f"Conversion complete! {frame_count} frames saved to {output_folder}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Convert a video into a series of images.')
    
    # Add arguments for the video file path and output folder
    parser.add_argument('video_path', type=str, help='Path to the input video file')
    parser.add_argument('output_folder', type=str, help='Path to the folder where images will be saved')
    
    # Parse the arguments
    args = parser.parse_args()

    # Call the conversion function with the provided arguments
    convert_video_to_images(args.video_path, args.output_folder)
