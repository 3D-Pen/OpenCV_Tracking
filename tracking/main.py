import numpy as np

from camera import find_available_cameras
from camera import open_cameras
from camera import release_cameras
from camera import retrieve_frames

from image import imgs_show
from image import create_mask
from image import retrieve_x_y_from_max_contour
from image import draw_circle

from user_interface import is_key_pressed

# CONFIG
CAMERA_NUM = 2
TRACKING_THRESHOLDS = [
    {
        "lower": np.array([99, 97, 46]),
        "upper": np.array([215, 167, 115]),
    },
    {
        "lower": np.array([67, 99, 59]),
        "upper": np.array([155, 163, 125]),
    },
]


def main():
    # Setting up cameras
    available_cameras_index = find_available_cameras()

    print("[INFO] available cameras", available_cameras_index)
    if len(available_cameras_index) < CAMERA_NUM:
        print("[ERROR] Not enough cameras available")
        return

    cameras = open_cameras(available_cameras_index[:CAMERA_NUM])
    print("[INFO] Cameras opened")

    # Tracking
    input("[INFO] Press Enter to start tracking")
    print("[INFO] Tracking started")
    print("[INFO] Press 'q' to stop tracking")

    while True:
        frames = retrieve_frames(cameras)

        if np.any([frame is None for frame in frames]):
            print("[ERROR] Could not read frame from camera")
            break

        # Create mask
        masks = create_mask(frames, TRACKING_THRESHOLDS)
        x_y = retrieve_x_y_from_max_contour(masks)

        print("[INFO] 座標", x_y)

        imgs_show(draw_circle(frames, x_y))

        if is_key_pressed("q"):
            break

    # Close cameras
    release_cameras(cameras)
    print("[INFO] Cameras released")


if __name__ == "__main__":
    main()
