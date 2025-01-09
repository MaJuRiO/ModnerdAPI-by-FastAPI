import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
base_options = python.BaseOptions(model_asset_path='blaze_face_short_range.tflite')
options = vision.FaceDetectorOptions(base_options=base_options)
detector = vision.FaceDetector.create_from_options(options)

def visualize(
    image,
    detection_result
) -> np.ndarray:
    annotated_image = image.copy()
    height, width, _ = image.shape
    confi = list()
    try:
        for detection in detection_result.detections:
            confi.append(detection.categories[0].score)
        most_confi_index = confi.index(max(confi))
        bbox = detection_result.detections[most_confi_index].bounding_box
        #start_point = bbox.origin_x, bbox.origin_y
        #end_point = bbox.origin_x + bbox.width, bbox.origin_y + bbox.height
        annotated_image = annotated_image[bbox.origin_y:bbox.origin_y+bbox.height, bbox.origin_x:bbox.origin_x + bbox.width]
        return annotated_image
    except:
        pass
    
def extract_face(image: np.ndarray, required_size=(224,224)) -> np.ndarray:
    frame_bw = mp.Image(image_format=mp.ImageFormat.SRGB, data=image)
    detection_result = detector.detect(frame_bw)
    image_copy = np.copy(frame_bw.numpy_view())
    annotated_image = visualize(image_copy, detection_result)
    #rgb_annotated_image = cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB)
    extracted_face = cv2.resize(annotated_image,required_size,interpolation = cv2.INTER_LINEAR)
    return extracted_face