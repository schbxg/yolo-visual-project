import cv2
from ultralytics import YOLO
import os
import json
import time

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
    # Create trackbars
    cv2.createTrackbar("Confidence", window_name, 25, 100, nothing)
    cv2.createTrackbar("IoU", window_name, 45, 100, nothing)
    cv2.createTrackbar("Auto Save", window_name, 0, 1, nothing)
    cv2.createTrackbar("Show ID", window_name, 0, 1, nothing)
    cv2.createTrackbar("Kpt Conf", window_name, 50, 100, nothing) # New: Threshold for keypoints

    # Crucial: Give the GUI time to initialize the window before reading trackbars
    cv2.waitKey(1)

    # Create output directory for saved data
    save_dir = "d:/06-code/yolo/yolo-project/output/keypoints"
    os.makedirs(save_dir, exist_ok=True)

    print("Controls:")
    print("  - Press 'q' to exit the live stream.")
    print("  - Press 's' to manual save current keypoints.")
    print("  - Use 'Auto Save' trackbar to toggle automatic saving.")
    print("  - Use 'Show ID' trackbar to overlay keypoint indices.")
    print("  - Use 'Kpt Conf' trackbar to filter points by confidence (JSON & Display).")

    last_save_time = 0

    while True:
        # Read a frame from the webcam
        success, frame = cap.read()
        if not success:
            print("Failed to grab frame.")
            break

        # Safety check for window and trackbars to prevent "Null pointer" crash
        try:
            if cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) < 1:
                print("Window closed by user.")
                break
            
            conf = cv2.getTrackbarPos("Confidence", window_name) / 100.0
            iou = cv2.getTrackbarPos("IoU", window_name) / 100.0
            auto_save = cv2.getTrackbarPos("Auto Save", window_name)
            show_id = cv2.getTrackbarPos("Show ID", window_name)
            kpt_conf_threshold = cv2.getTrackbarPos("Kpt Conf", window_name) / 100.0
        except cv2.error:
            # Fallback if window hasn't fully initialized yet
            conf, iou, auto_save, show_id, kpt_conf_threshold = 0.25, 0.45, 0, 0, 0.5

        # Run YOLO pose inference on the frame
        results = model.predict(
            source=frame, 
            conf=conf, 
            iou=iou, 
            show=False, 
            verbose=False
        )

        # Prepare frame for display
        if results and len(results) > 0:
            display_frame = results[0].plot()
            
            # Overlay Keypoint IDs if enabled
            if show_id == 1 and results[0].keypoints is not None:
                # Get keypoints coordinates and confidence
                kps = results[0].keypoints.xy.cpu().numpy()
                confs = results[0].keypoints.conf.cpu().numpy()
                
                for p_idx, person_kps in enumerate(kps):
                    for i, (x, y) in enumerate(person_kps):
                        conf_val = confs[p_idx][i]
                        # ONLY show index if confidence matches the trackbar
                        if x > 0 and y > 0 and conf_val >= kpt_conf_threshold:
                            cv2.putText(display_frame, str(i), (int(x), int(y)), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        else:
            display_frame = frame.copy()

        # Display the frame
        cv2.imshow(window_name, display_frame)

        # Auto-Save Logic
        current_time = time.time()
        should_save = False
        
        if auto_save == 1 and (current_time - last_save_time) > 0.5: # Throttle to max 2 saves per second
            should_save = True

        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            print("Exiting...")
            break
        elif key == ord('s') or should_save:
            if results and len(results) > 0:
                res = results[0]
                if hasattr(res, 'keypoints') and res.keypoints is not None and len(res.keypoints) > 0:
                    # Get raw data [num_persons, 17, 3]
                    raw_kp_data = res.keypoints.data.cpu().numpy().tolist()
                    filtered_kp_data = []

                    # Filter the data for JSON to match the visual output
                    for person_kps in raw_kp_data:
                        filtered_person = []
                        for kpt in person_kps:
                            x, y, c = kpt
                            # If confidence is too low, zero out the point
                            if c < kpt_conf_threshold:
                                filtered_person.append([0.0, 0.0, c]) # Keep confidence but zero coordinates
                            else:
                                filtered_person.append([x, y, c])
                        filtered_kp_data.append(filtered_person)
                    
                    save_timestamp = time.strftime("%Y%m%d-%H%M%S")
                    ms = int((time.time() % 1) * 1000)
                    base_filename = f"keypoints_{save_timestamp}_{ms:03d}"
                    
                    json_path = os.path.join(save_dir, f"{base_filename}.json")
                    raw_path = os.path.join(save_dir, f"{base_filename}_raw.jpg")
                    res_path = os.path.join(save_dir, f"{base_filename}_result.jpg")
                    
                    try:
                        # 1. Save JSON Keypoints (Filtered)
                        with open(json_path, 'w') as f:
                            json.dump({
                                "timestamp": save_timestamp,
                                "ms": ms,
                                "num_persons": len(res.keypoints),
                                "kpt_conf_threshold": kpt_conf_threshold,
                                "keypoints": filtered_kp_data
                            }, f, indent=4)
                        
                        # 2. Save Raw Image
                        cv2.imwrite(raw_path, frame)
                        
                        # 3. Save Result Image (Annotated)
                        # Use display_frame which has the plots/IDs
                        cv2.imwrite(res_path, display_frame)
                        
                        if not should_save: # Manual save feedback
                            print(f"SUCCESS: Manual save to {base_filename}")
                            feedback_frame = display_frame.copy()
                            cv2.putText(feedback_frame, "SAVED!", (50, 50), 
                                        cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                            cv2.imshow(window_name, feedback_frame)
                            cv2.waitKey(300)
                        else:
                            last_save_time = current_time
                            # Minor blink for auto-save feedback
                            cv2.circle(display_frame, (30, 30), 10, (0, 0, 255), -1)
                            cv2.imshow(window_name, display_frame)
                    except Exception as e:
                        print(f"ERROR saving data: {e}")
                elif not should_save:
                    print("SAVE FAILED: No people detected.")

    # Release the webcam and close windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_live_pose()
