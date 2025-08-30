import os
import cv2

INPUT_FOLDER = r"C:\DATA\YT\Input"
OUTPUT_FOLDER = r"C:\DATA\YT\Output"
BLUR_ENABLED = True  # Set to False to disable blur
DEL_CLIP_ENABLED = True  # Set to False to disable blur

def blur_area_on_frame(frame, blur_rect, ksize=(25, 25)):
    x, y, w, h = blur_rect
    roi = frame[y:y+h, x:x+w]
    blurred_roi = cv2.GaussianBlur(roi, ksize, 0)
    frame[y:y+h, x:x+w] = blurred_roi
    return frame

def is_in_delete_ranges(current_time, delete_ranges):
    for start, end in delete_ranges:
        if start <= current_time < end:
            return True
    return False

def add_text_and_image_to_video(
    video_path, output_path, text, image_path, position=(0,0),
    text_start=0, text_end=None, img_start=0, img_end=None,
    logo_size=None,
    blur_rect=(200, 200, 200, 200),  # (x, y, w, h)
    blur_start=8, blur_end=15,
    delete_ranges=None  # List of (start_time, end_time) tuples
):
    if not DEL_CLIP_ENABLED or delete_ranges is None:
        delete_ranges = []

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Cannot open video file.")
        return

    overlay_img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    if overlay_img is None:
        print("Error: Cannot open image file.")
        cap.release()
        return

    if logo_size is not None:
        overlay_img = cv2.resize(overlay_img, logo_size, interpolation=cv2.INTER_AREA)

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
    text_y = (height + text_size[1]) // 4
    text_color = (0, 0, 255)

    frame_idx = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    if text_end is None:
        text_end = total_frames / fps
    if img_end is None:
        img_end = total_frames / fps

    img_h, img_w = overlay_img.shape[:2]
    if position[0] + img_w > width or position[1] + img_h > height:
        img_w = min(img_w, width - position[0])
        img_h = min(img_h, height - position[1])
        overlay_img = cv2.resize(overlay_img, (img_w, img_h))

    has_alpha = overlay_img.shape[2] == 4

    while True:
        ret, frame = cap.read()
        if not ret:
            break
        current_time = frame_idx / fps

        # Skip frames in delete_ranges
        if is_in_delete_ranges(current_time, delete_ranges):
            frame_idx += 1
            continue

        # Add text
        if text_start <= current_time <= text_end:
            cv2.putText(frame, text, (text_x, text_y), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

        # Add image
        if img_start <= current_time <= img_end:
            x, y = position
            if has_alpha:
                overlay_rgb = overlay_img[:, :, :3]
                mask = overlay_img[:, :, 3] / 255.0
                for c in range(3):
                    frame[y:y+img_h, x:x+img_w, c] = (
                        overlay_rgb[:, :, c] * mask +
                        frame[y:y+img_h, x:x+img_w, c] * (1 - mask)
                    ).astype('uint8')
            else:
                frame[y:y+img_h, x:x+img_w] = overlay_img

        # Add blur
        if BLUR_ENABLED and blur_start <= current_time <= blur_end:
            frame = blur_area_on_frame(frame, blur_rect)

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()
    print(f"Output saved to {output_path}")

if __name__ == "__main__":
    video_files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    if not video_files:
        print("No video file found in input folder.")
        exit(1)
    video_filename = video_files[0]
    video_path = os.path.join(INPUT_FOLDER, video_filename)
    output_path = os.path.join(OUTPUT_FOLDER, f"output_with_text_and_image_{video_filename}")
    text = input("Enter text to add on top: ")
    image_path = r"C:\DATA\YT\logo.png"
    position = (50, 50)
    
    text_start = 0
    text_end = 10
    
    img_start = 10
    img_end = 25

    logo_size = (100, 100)

    # Blur settings
    blur_rect = (400, 270, 200, 200)  # x, y, w, h
    blur_start = 10
    blur_end = 15

    # Delete ranges: list of (start_time, end_time) in seconds
    delete_ranges = [
        (10, 23),  # Example: delete from 12s to 16s
        (30, 40)  # Add more ranges as needed
    ]

    add_text_and_image_to_video(
        video_path, output_path, text, image_path, position,
        text_start, text_end, img_start, img_end,
        logo_size=logo_size,
        blur_rect=blur_rect,
        blur_start=blur_start,
        blur_end=blur_end,
        delete_ranges=delete_ranges
    )
