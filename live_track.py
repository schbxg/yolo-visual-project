import cv2
from ultralytics import YOLO
import os

# Updated to use a general detection model to support "bottle" and other objects
# You can change this to 'yolo11n-pose.pt' for pose-only tracking
model_path = 'd:/06-code/yolo/yolo-project/models/yolo11n.pt'
if not os.path.exists(model_path):
    print("Model not found locally, using online version...")
    model = YOLO('yolo11n.pt')
else:
    model = YOLO(model_path)

def nothing(x):
    pass

def start_live_track():
    # 0 is usually the default webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Create a window for trackbars
    window_name = "YOLO11 ByteTrack Live"
    cv2.namedWindow(window_name)
    
    # Create trackbars for confidence and IoU
    cv2.createTrackbar("Confidence", window_name, 25, 100, nothing)
    cv2.createTrackbar("IoU", window_name, 45, 100, nothing)
    
    # Crucial: Give the GUI time to initialize the window
    cv2.waitKey(1)

    print("Press 'q' to exit the live stream.")

    while True:
        # Read a frame from the webcam
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame.")
            break

        # Double check if window still exists before getting trackbar position
        # This prevents the "Null pointer" error if the user closes the window manually
        try:
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                print("Window closed by user.")
                break
            
            conf = cv2.getTrackbarPos("Confidence", window_name) / 100.0
            iou = cv2.getTrackbarPos("IoU", window_name) / 100.0
        except cv2.error:
            # Fallback if window properties can't be read
            conf, iou = 0.25, 0.45

        # Run ByteTrack tracking on the frame
        # tracker="bytetrack.yaml" enables the ByteTrack algorithm
        # persist=True maintains IDs across frames
        results = model.track(
            source=frame, 
            conf=conf, 
            iou=iou, 
            persist=True,
            tracker="bytetrack.yaml",
            show=False, 
            verbose=False
        )

        # Plot the results on the frame
        if results and len(results) > 0:
            # Plot will now include labels for any detected COCO objects (bottles, people, etc.)
            annotated_frame = results[0].plot()
            cv2.imshow(window_name, annotated_frame)
        else:
            cv2.imshow(window_name, frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_live_track()
