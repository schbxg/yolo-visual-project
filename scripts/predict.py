#!/usr/bin/env python3
"""
YOLO Object Detection Inference Script
"""
import os
import argparse
import cv2
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description='YOLO Inference Script')
    parser.add_argument('--model', type=str, default='yolo-project/models/yolov8n.pt',
                        help='Path to model file or model name')
    parser.add_argument('--source', type=str, required=True,
                        help='Input source: image file, video file, or webcam index')
    parser.add_argument('--output', type=str, default='output',
                        help='Output directory for results')
    parser.add_argument('--conf', type=float, default=0.25,
                        help='Confidence threshold')
    parser.add_argument('--device', type=str, default='cpu',
                        help='Device to use (0 for GPU, cpu for CPU)')
    return parser.parse_args()

def run_inference(model_name, source, output_dir, conf=0.25, device='cpu'):
    print(f"🚀 Starting YOLO Inference")
    print(f"📊 Model: {model_name}")
    print(f"📷 Source: {source}")
    
    # Load model
    yolo_model = YOLO(model_name)
    
    # Run inference
    results = yolo_model.predict(source=source, conf=conf, device=device, save=True, project=output_dir, name='exp')
    
    print(f"✅ Inference completed. Results saved in {output_dir}/exp")
    return results

def main():
    args = parse_args()
    os.makedirs(args.output, exist_ok=True)
    run_inference(args.model, args.source, args.output, args.conf, args.device)

if __name__ == "__main__":
    main()
