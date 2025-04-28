from ultralytics import YOLO
import torch

# Load model once when file is imported
model = YOLO('yolov8n.pt')  # 'n' = nano (smallest, fastest), you can also use 'yolov8m.pt', 'yolov8l.pt' if you want better accuracy

def detect_product(image):
    """
    Detect objects from a PIL image using YOLOv8.

    Args:
        image: PIL.Image object

    Returns:
        List of detected labels (e.g., ["Laptop", "Backpack"])
    """
    try:
        # Run inference
        results = model.predict(image, imgsz=640, conf=0.25)  # imgsz = 640, confidence threshold = 25%

        detected_labels = set()

        # Parse results
        for result in results:
            boxes = result.boxes
            if boxes is not None:
                for box in boxes:
                    cls_id = int(box.cls)
                    label = model.names[cls_id]
                    detected_labels.add(label)

        return list(detected_labels)

    except Exception as e:
        print(f"Error in YOLO detection: {e}")
        return []
