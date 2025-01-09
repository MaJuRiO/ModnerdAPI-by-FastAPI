import pickle
import cv2
import numpy as np
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, AveragePooling2D, Flatten, Dense, Dropout
from tensorflow.keras.applications import MobileNetV2
import matplotlib.pyplot as plt

from model.facedetection import extract_face

# โหลดไฟล์ Student_id.pkl
with open('Student_id.pkl', 'rb') as f:
    lb = pickle.load(f)

# ตั้งค่าพารามิเตอร์
num_classes = len(lb)  # จำนวนคลาสของคุณ
img_width, img_height = 224, 224

# สร้างโมเดลใหม่ให้เหมือนกับโมเดลที่คุณฝึก
baseModel = MobileNetV2(weights="imagenet", include_top=False, input_tensor=Input(shape=(224, 224, 3)))
headModel = baseModel.output
headModel = AveragePooling2D(pool_size=(7, 7))(headModel)
headModel = Flatten(name="flatten")(headModel)
headModel = Dense(256, activation="relu")(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(128, activation="relu")(headModel)
headModel = Dropout(0.5)(headModel)
headModel = Dense(num_classes, activation="softmax")(headModel)
model = Model(inputs=baseModel.input, outputs=headModel)

# โหลด weights ที่บันทึกไว้
model.load_weights("mask_detector_weights.h5")

def predict(file):
    img = extract_face(file)
    img = cv2.resize(img, (224, 224))
    img = img.astype('float32') / 255.0
    img = np.expand_dims(img, axis=0)
    prediction = model.predict(img)
    predicted_class_idx = np.argmax(prediction)
    predicted_class = lb[predicted_class_idx]
    return predicted_class