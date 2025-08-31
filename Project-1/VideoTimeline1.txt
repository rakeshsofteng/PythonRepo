import cv2
import numpy as np
import os

# ========= User settings =========
VIDEO_PATH = "input.mp4"      # change as needed
OUTPUT_PATH = "output.mp4"    # export file path
WINDOW_NAME = "Mini Video Editor (OpenCV)"
TARGET_WIDTH = 960            # UI width (video will scale to this)
TIMELINE_H = 80               # timeline height in pixels
FONT = cv2.FONT_HERSHEY_SIMPLEX
# =================================

# --- Open video ---
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    raise SystemExit(f"Cannot open video: {VIDEO_PATH}")

total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
fps          = cap.get(cv2.CAP_PROP_FPS) or 30.0
vw           = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
vh           = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
duration_sec = total_frames / fps if fps > 0 else 0

# Scale video to fit TARGET_WIDTH (keep aspect)
scale = TARGET_WIDTH / vw
disp_w = TARGET_WIDTH
disp_h = int(round(vh * scale))

# --- State ---
current_frame = 0           # 0..total_frames-1
playing = True
delete_ranges = []          # list of (start, end) [end exclusive], sorted & non-overlapping
selection_active = False
selection_start_f = None    # frame index where drag started on timeline
selection_end_f = None      # latest frame under mouse while dragging
hover_frame = None          # frame under mouse (for hover indicator)

# --- Helpers for ranges ---
def merge_ranges(ranges):
    if not ranges:
        return []
    ranges = sorted(ranges)
    merged = [ranges[0]]
    for s, e in ranges[1:]:
        last_s, last_e = merged[-1]
        if s <= last_e:               # overlap or touch
            merged[-1] = (last_s, max(last_e, e))
        else:
            merged.append((s, e))
    return merged

def add_delete_range(a, b):
    if a is None or b is None:
        return
    s = max(0, min(a, b))
    e = min(total_frames, max(a, b) + 1)   # make end exclusive, include clicked frame
    if e <= s:
        return
    delete_ranges.append((s, e))
    # merge overlaps/touches
    merged = merge_ranges(delete_ranges)
    delete_ranges.clear()
    delete_ranges.extend(merged)

def point_in_timeline(y):
    return disp_h <= y < disp_h + TIMELINE_H

def frame_to_x(f):
    if total_frames <= 1:
        return 0
    # map [0, total_frames-1] -> [0, disp_w-1]
    return int((f / (total_frames - 1)) * (disp_w - 1))

def x_to_frame(x):
    x = np.clip(x, 0, disp_w - 1)
    if disp_w <= 1:
        return 0
    return int(round((x / (disp_w - 1)) * (total_frames - 1)))

def seek_to_frame(f):
    global current_frame
    f = int(np.clip(f, 0, total_frames - 1))
    cap.set(cv2.CAP_PROP_POS_FRAMES, f)
    current_frame = f

def read_next_frame():
    global current_frame
    ret, frame = cap.read()
    if not ret:
        return None
    current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES)) - 1
    return frame

def draw_timeline(canvas):
    # timeline background
    y0 = disp_h
    cv2.rectangle(canvas, (0, y0), (disp_w, y0 + TIMELINE_H), (32, 32, 32), -1)

    # draw deleted ranges
    for s, e in delete_ranges:
        x1, x2 = frame_to_x(s), frame_to_x(min(e, total_frames - 1))
        cv2.rectangle(canvas, (x1, y0), (x2, y0 + TIMELINE_H), (0, 0, 255), -1)

    # selection (dragging)
    if selection_active and selection_start_f is not None and selection_end_f is not None:
        xs = frame_to_x(selection_start_f)
        xe = frame_to_x(selection_end_f)
        x1, x2 = sorted((xs, xe))
        overlay = canvas.copy()
        cv2.rectangle(overlay, (x1, y0), (x2, y0 + TIMELINE_H), (0, 165, 255), -1)  # orange
        alpha = 0.5
        cv2.addWeighted(overlay, alpha, canvas, 1 - alpha, 0, canvas)

    # hover indicator
    if hover_frame is not None:
        hx = frame_to_x(hover_frame)
        cv2.line(canvas, (hx, y0), (hx, y0 + TIMELINE_H - 1), (180, 180, 180), 1)

    # current frame cursor
    cx = frame_to_x(current_frame)
    cv2.line(canvas, (cx, y0), (cx, y0 + TIMELINE_H - 1), (255, 255, 255), 2)

    # ticks & labels (every ~10 seconds or at least 5 ticks)
    ticks = max(5, int(duration_sec // 10) + 1)
    for i in range(ticks + 1):
        f = int(round((i / ticks) * (total_frames - 1)))
        x = frame_to_x(f)
        cv2.line(canvas, (x, y0), (x, y0 + 10), (100, 100, 100), 1)
        t = f / fps
        label = f"{int(t//60)}:{int(t%60):02d}"
        cv2.putText(canvas, label, (max(0, x - 18), y0 + 28), FONT, 0.45, (200, 200, 200), 1, cv2.LINE_AA)

    # help strip
    help_text = "Space=Play/Pause  Click/Drag on timeline=Select  Del/D=Delete  U=Undo  C=Clear  X=Export  Q=Quit"
    cv2.putText(canvas, help_text, (10, y0 + TIMELINE_H - 12), FONT, 0.48, (220, 220, 220), 1, cv2.LINE_AA)

def render_ui(frame_bgr):
    # scale frame
    disp = cv2.resize(frame_bgr, (disp_w, disp_h), interpolation=cv2.INTER_AREA)

    # info bar at top-left
    t = current_frame / fps if fps > 0 else 0
    time_txt = f"{int(t//60)}:{int(t%60):02d}.{int((t*1000)%1000):03d} / {int(duration_sec//60)}:{int(duration_sec%60):02d}"
    info = f"Frame {current_frame+1}/{total_frames}  FPS {fps:.2f}  Cuts {len(delete_ranges)}"
    cv2.putText(disp, time_txt, (10, 24), FONT, 0.7, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(disp, info,     (10, 50), FONT, 0.6, (255, 255, 255), 1, cv2.LINE_AA)

    # create UI canvas with timeline region
    canvas = np.zeros((disp_h + TIMELINE_H, disp_w, 3), dtype=np.uint8)
    canvas[:disp_h] = disp
    draw_timeline(canvas)
    return canvas

# --- Mouse handling ---
def on_mouse(event, x, y, flags, param):
    global selection_active, selection_start_f, selection_end_f, hover_frame
    if point_in_timeline(y):
        f = x_to_frame(x)
        hover_frame = f
        if event == cv2.EVENT_LBUTTONDOWN:
            selection_active = True
            selection_start_f = f
            selection_end_f = f
        elif event == cv2.EVENT_MOUSEMOVE and selection_active:
            selection_end_f = f
        elif event == cv2.EVENT_LBUTTONUP:
            selection_active = False
            selection_end_f = f
        elif event == cv2.EVENT_RBUTTONDOWN:
            # Right-click seeks without selecting
            seek_to_frame(f)
    else:
        hover_frame = None
        # left click on video seeks to nearest frame under current cursor x using current y ignored
        if event == cv2.EVENT_LBUTTONDOWN:
            # no-op outside timeline
            pass

cv2.namedWindow(WINDOW_NAME)
cv2.setMouseCallback(WINDOW_NAME, on_mouse)

# Prime first frame
seek_to_frame(0)
frame = read_next_frame()
if frame is None:
    raise SystemExit("Could not read first frame.")

# --- Main UI loop ---
while True:
    if playing:
        frame = read_next_frame()
        if frame is None:
            # loop or pause at end
            playing = False
            seek_to_frame(total_frames - 1)
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            ret, frame = cap.read()
            if not ret:
                # reopen to be safe
                cap.release()
                cap = cv2.VideoCapture(VIDEO_PATH)
                seek_to_frame(total_frames - 1)
                ret, frame = cap.read()
                if not ret:
                    break
    else:
        # paused: ensure we show the frame at current_frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        ret, frame = cap.read()
        if not ret:
            break

    ui = render_ui(frame)
    cv2.imshow(WINDOW_NAME, ui)

    # Wait ~15ms for key (around 60 FPS UI)
    key = cv2.waitKey(15) & 0xFFFFFFFF

    # Normalize common keys
    if key in (ord('q'), ord('Q')):
        break
    elif key == 32:  # Space
        playing = not playing
    elif key in (127, 255, ord('d'), ord('D')):  # Delete / 'd'
        # add selection if exists; if not dragging, use a tiny range around current frame
        if selection_start_f is not None and selection_end_f is not None and selection_start_f != selection_end_f:
            add_delete_range(selection_start_f, selection_end_f)
        else:
            add_delete_range(current_frame, current_frame)
        # clear selection
        selection_start_f = None
        selection_end_f = None
    elif key in (ord('u'), ord('U')):  # Undo last cut
        if delete_ranges:
            delete_ranges.pop()
    elif key in (ord('c'), ord('C')):  # Clear all cuts
        delete_ranges.clear()
    elif key in (ord('x'), ord('X')):  # Export
        print("Exporting… This may take a bit depending on video length.")
        # Prepare writer
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (vw, vh))
        # Reopen stream from start for export
        cap.release()
        cap = cv2.VideoCapture(VIDEO_PATH)
        fidx = 0
        # Build a fast skip map of frames to drop
        cuts = merge_ranges(delete_ranges[:])
        cut_idx = 0
        skip_s, skip_e = cuts[0] if cuts else (None, None)
        while True:
            ret, fr = cap.read()
            if not ret:
                break
            # advance cut window if needed
            while skip_s is not None and fidx >= skip_e:
                cut_idx += 1
                if cut_idx < len(cuts):
                    skip_s, skip_e = cuts[cut_idx]
                else:
                    skip_s, skip_e = (None, None)
            # write if not inside a cut
            if not (skip_s is not None and skip_s <= fidx < skip_e):
                out.write(fr)

            fidx += 1
            if fidx % max(1, total_frames // 100) == 0:
                pct = int((fidx / total_frames) * 100)
                print(f"Export progress: {pct}%")

        out.release()
        print(f"✅ Exported to {OUTPUT_PATH}")
        # Resume interactive session
        cap.release()
        cap = cv2.VideoCapture(VIDEO_PATH)
        seek_to_frame(min(current_frame, total_frames - 1))
    # Arrow keys for fine seeking (platform dependent codes)
    elif key in (81, 2424832):  # left
        playing = False
        seek_to_frame(current_frame - 1)
    elif key in (83, 2555904):  # right
        playing = False
        seek_to_frame(current_frame + 1)
    elif key in (82, 2490368):  # up: jump back 1s
        playing = False
        seek_to_frame(current_frame - int(fps))
    elif key in (84, 2621440):  # down: jump forward 1s
        playing = False
        seek_to_frame(current_frame + int(fps))

cap.release()
cv2.destroyAllWindows()
