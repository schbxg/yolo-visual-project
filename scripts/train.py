#!/usr/bin/env python3
"""
YOLO Training Script for Docker Environment
"""
import os
import sys
import argparse
import yaml
from datetime import datetime
from ultralytics import YOLO

def parse_args():
    parser = argparse.ArgumentParser(description='YOLO Training Script')
    parser.add_argument('--data', type=str, default='data/dataset.yaml',
                        help='Path to dataset YAML file')
    parser.add_argument('--model', type=str, default='yolov8n.pt',
                        help='Path to model file or model name')
    parser.add_argument('--epochs', type=int, default=10,
                        help='Number of training epochs')
    parser.add_argument('--imgsz', type=int, default=640,
                        help='Input image size')
    parser.add_argument('--batch-size', type=int, default=8,
                        help='Batch size')
    parser.add_argument('--device', type=str, default='0',
                        help='GPU device ID')
    parser.add_argument('--project', type=str, default='yolo_training',
                        help='Project name')
    parser.add_argument('--name', type=str, default='exp',
                        help='Experiment name')
    parser.add_argument('--workers', type=int, default=4,
                        help='Number of worker threads')
    return parser.parse_args()

# Get the directory where this script is located (scripts/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)  # Parent directory (yolo-project/)

def setup_logging():
    """Setup logging"""
    log_dir = os.path.join(PROJECT_DIR, 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'training_{timestamp}.log')
    
    with open(log_file, 'w') as f:
        f.write(f"YOLO Training Started at {timestamp}\n")
        f.write(f"Command: {' '.join(sys.argv)}\n")
        f.write("-" * 50 + "\n")
    
    return log_file

def main():
    args = parse_args()
    log_file = setup_logging()
    
    print(f"🚀 Starting YOLO Training")
    print(f"📊 Dataset: {args.data}")
    print(f"🤖 Model: {args.model}")
    print(f"🎯 Epochs: {args.epochs}")
    print(f"🖼️ Image Size: {args.imgsz}")
    print(f"📦 Batch Size: {args.batch_size}")
    print(f"💻 Device: {args.device}")
    
    # Verify data file exists
    if not os.path.exists(args.data):
        print(f"⚠️ Dataset file not found: {args.data}")
        print("📋 Using default dataset for demonstration...")
        args.data = 'data/dataset.yaml'
        
        # Create demo dataset configuration
        demo_data = {
            'path': '/workspace/data/dataset',
            'train': 'images/train',
            'val': 'images/val',
            'nc': 3,
            'names': ['person', 'car', 'dog']
        }
        
        with open(args.data, 'w') as f:
            yaml.dump(demo_data, f)
        
        print(f"✅ Created demo dataset configuration: {args.data}")
    
    try:
        # Load model
        print("📥 Loading model...")
        model = YOLO(args.model)
        
        # Start training
        print("🏃 Starting training...")
        results = model.train(
            data=args.data,
            epochs=args.epochs,
            imgsz=args.imgsz,
            batch_size=args.batch_size,
            device=args.device,
            project=args.project,
            name=args.name,
            workers=args.workers,
            save=True,
            save_period=5,
            cache=False,
            verbose=True,
            seed=42
        )
        
        print("✅ Training completed successfully!")
        print(f"📁 Results saved to: {results.save_dir}")
        
        # Save training log
        with open(log_file, 'a') as f:
            f.write(f"Training completed successfully at {datetime.now()}\n")
            f.write(f"Results saved to: {results.save_dir}\n")
        
        # Model validation
        print("🔍 Running validation...")
        val_results = model.val()
        print(f"📊 Validation Results:")
        print(f"   mAP50-95: {val_results.box.map:.4f}")
        print(f"   mAP50: {val_results.box.map50:.4f}")
        print(f"   Precision: {val_results.box.mp:.4f}")
        print(f"   Recall: {val_results.box.mr:.4f}")
        
    except Exception as e:
        print(f"❌ Training failed: {str(e)}")
        with open(log_file, 'a') as f:
            f.write(f"Training failed: {str(e)}\n")
        
        # Fallback to demo training with synthetic data
        print("🔄 Falling back to demo training...")
        try:
            model = YOLO('yolov8n.pt')
            # Use COCO dataset for demo
            results = model.train(data='coco128.yaml', epochs=5, imgsz=320, batch_size=8)
            print("✅ Demo training completed successfully!")
        except Exception as demo_e:
            print(f"❌ Demo training also failed: {str(demo_e)}")
            sys.exit(1)

if __name__ == "__main__":
    main()
