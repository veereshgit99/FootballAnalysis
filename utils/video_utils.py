import cv2

# Read video frames from video_path through capturing frames from video (24 frames per second)
def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    frames = []
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames

# Save video frames to video_path with fps (frames per second)
def save_video(frames, video_path, fps=24):
    height, width, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(video_path, fourcc, fps, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()