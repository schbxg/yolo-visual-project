import gradio as gr
from ultralytics import YOLO
import PIL.Image as Image
import os
import cv2
import numpy as np

# Load the pose model
model_path = 'd:/06-code/yolo/yolo-project/models/yolo11n-pose.pt'
if not os.path.exists(model_path):
    print(f"Model not found at {model_path}, downloading...")
    model = YOLO('yolo11n-pose.pt')
    model.save(model_path)
else:
    model = YOLO(model_path)

def predict_pose(img, conf_threshold, iou_threshold):
    if img is None:
        return None, "No image received. Please upload or snap a photo."
        
    try:
        # Run inference
        results = model.predict(
            source=img,
            conf=conf_threshold,
            iou=iou_threshold,
            save=False
        )
        
        if not results or len(results) == 0:
            return img, "Model returned no results."

        # Plot results on the image
        r = results[0]
        im_array = r.plot() # BGR numpy array
        
        # Convert BGR to RGB
        im_rgb = im_array[..., ::-1]
        
        num_boxes = len(r.boxes) if hasattr(r, 'boxes') else 0
        status = f"Success! Found {num_boxes} person(s)."
        return Image.fromarray(im_rgb), status
    except Exception as e:
        return img, f"Error: {str(e)}"

# Create the Gradio interface using Blocks for better control
with gr.Blocks(title="🕺 YOLO11 Pose Estimation") as demo:
    gr.Markdown("# 🕺 YOLO11 Pose Estimation Demo")
    
    with gr.Row():
        with gr.Column():
            input_img = gr.Image(label="Input (Upload or Webcam)", type="pil")
            conf_slider = gr.Slider(minimum=0, maximum=1, value=0.25, label="Confidence Threshold")
            iou_slider = gr.Slider(minimum=0, maximum=1, value=0.45, label="IoU Threshold")
            submit_btn = gr.Button("Detect Pose", variant="primary")
        
        with gr.Column():
            output_img = gr.Image(label="Pose Result", type="pil")
            status_text = gr.Textbox(label="Status", interactive=False)
            
    gr.Markdown("""
    ### 💡 Instructions for Webcam:
    1.  Click the **Webcam icon** below the input box (if not already active).
    2.  Look at the camera and click the **White Circle (Camera Icon)** that appears at the bottom of the camera feed.
    3.  Once the photo is snapped, it will appear in the box.
    4.  Click the **'Detect Pose'** button above to see results.
    """)

    # Connect components
    submit_btn.click(
        fn=predict_pose,
        inputs=[input_img, conf_slider, iou_slider],
        outputs=[output_img, status_text]
    )
    
    # Also trigger on change if user prefers live
    input_img.change(
        fn=predict_pose,
        inputs=[input_img, conf_slider, iou_slider],
        outputs=[output_img, status_text]
    )

if __name__ == "__main__":
    print("Launching Gradio Blocks demo...")
    demo.launch(share=False)
