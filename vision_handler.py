
import cv2
import numpy as np
import pyautogui
import mss
from transformers import AutoImageProcessor, AutoModelForObjectDetection
from deepface import DeepFace
import pytesseract

# Initialize vision components
object_detector = AutoModelForObjectDetection.from_pretrained(
    "microsoft/faster-rcnn-resnet50-fpn"
)
image_processor = AutoImageProcessor.from_pretrained(
    "microsoft/faster-rcnn-resnet50-fpn"
)
screen_capture = mss.mss()

def capture_camera():
    """Capture frame from camera"""
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return frame if ret else None

def capture_screen(region="full"):
    """Capture screen content"""
    if region == "full":
        return np.array(pyautogui.screenshot())
    else:
        return np.array(screen_capture.grab(get_screen_region(region)))

def detect_objects(image):
    """Detect objects in image"""
    inputs = image_processor(images=image, return_tensors="pt")
    outputs = object_detector(**inputs)
    
    results = []
    for score, label, box in zip(outputs.scores, outputs.labels, outputs.boxes):
        if score > 0.5:
            results.append({
                "label": label,
                "confidence": float(score),
                "box": box.tolist()
            })
    return results

def analyze_faces(image):
    """Analyze faces in image"""
    try:
        return DeepFace.analyze(image, actions=['age', 'gender', 'emotion'])
    except:
        return []