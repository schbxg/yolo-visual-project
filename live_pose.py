import cv2
from ultralytics import YOLO
import os

# Load the pose model
model_path = 'd:/06-code/yolo/yolo-project/models/yolo11n-pose.pt'
if not os.path.exists(model_path):
    print("Model not found locally, using online version...")
    model = YOLO('yolo11n-pose.pt')
else:
    model = YOLO(model_path)

def nothing(x):
    pass

def start_live_pose():
    # 0 is usually the default webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    # Create a window for trackbars
    window_name = "YOLO11 Live Pose Detection"
    cv2.namedWindow(window_name)
    # Create trackbars for confidence and IoU
    # Values are multiplied by 100 for integer trackbars
    cv2.createTrackbar("Confidence", window_name, 25, 100, nothing)
    cv2.createTrackbar("IoU", window_name, 45, 100, nothing)

    print("Press 'q' to exit the live stream.")

    while True:
        # Read a frame from the webcam
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame.")
            break

        # Get current positions of trackbars
        conf = cv2.getTrackbarPos("Confidence", window_name) / 100.0
        iou = cv2.getTrackbarPos("IoU", window_name) / 100.0

        # Run YOLO pose inference on the frame
        # Using predict instead of track to avoid 'lap' dependency issues for simple pose
        results = model.predict(
            source=frame, 
            conf=conf, 
            iou=iou, 
            show=False, 
            verbose=False
        )

        # Plot the results on the frame
        if results and len(results) > 0:
            annotated_frame = results[0].plot()
            # Display the annotated frame
            cv2.imshow("YOLO11 Live Pose Detection", annotated_frame)
        else:
            cv2.imshow("YOLO11 Live Pose Detection", frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_live_pose()
