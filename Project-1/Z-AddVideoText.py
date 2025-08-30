import os
import cv2

# Constants for input and output folders
INPUT_FOLDER = r"C:\DATA\YT\Input"
OUTPUT_FOLDER = r"C:\DATA\YT\Output"

def add_text_to_video(video_path, output_path, text, start_time=0, end_time=None):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    font_thickness = 2
    text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
    text_x = (width - text_size[0]) // 2
    text_y = (height + text_size[1]) // 3
    text_color = (0, 0, 255)

    frame_idx = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if end_time is None:
        end_time = total_frames / fps

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        current_time = frame_idx / fps
        if start_time <= current_time <= end_time:
            cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)
        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()
    print(f"Output saved to {output_path}")

if __name__ == "__main__":
    # Assume only one video file in input folder
    video_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    if not video_files:
        print("No video file found in input folder.")
        exit(1)
    video_filename = video_files[0]
    video_path = os.path.join(INPUT_FOLDER, video_filename)
    output_path = os.path.join(OUTPUT_FOLDER, f"output_with_text_{video_filename}")
    text = input("Enter text to add on top: ")
    start_time = 0
    end_time = 10
    add_text_to_video(video_path, output_path, text, start_time, end_time)