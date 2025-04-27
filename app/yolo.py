import streamlit as st
from ultralytics import YOLO
import cv2
import numpy as np
from PIL import Image

model = YOLO(r"C:\Users\Mahdi Mzari\Desktop\hackathon\best.pt")  


def load_image(image_file):
    img = Image.open(image_file)
    img = np.array(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)  
    return img


def predict_class_and_box(img):

    results = model(img)
    

    detections = results[0].boxes.xyxy  
    scores = results[0].boxes.conf  
    classes = results[0].boxes.cls  


    for i, detection in enumerate(detections):
        x_min, y_min, x_max, y_max = detection
        width = x_max - x_min
        height = y_max - y_min
        class_id = int(classes[i])  
        confidence = scores[i]
        if class_id != 2:


      
            img = cv2.rectangle(img, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 0, 255), 2)

        
            label = f"Class {class_id}, Conf: {confidence:.2f}"
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(img, label, (int(x_min), int(y_min)-10), font, 0.5, (0, 0, 255), 2, cv2.LINE_AA)

        else:
      
            pass
        
            break

  
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img




# image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

# if image_file is not None:
  
#     img = load_image(image_file)


#     output_img = predict_class_and_box(img)


#     st.image(output_img, caption="Detected Objects", use_container_width=True)


#     detections = model(output_img)
#     for i, detection in enumerate(detections[0].boxes.xyxy):
#         x_min, y_min, x_max, y_max = detection
#         class_id = int(detections[0].boxes.cls[i])
#         confidence = detections[0].boxes.conf[i]
#         st.write(f"Detection {i+1}:")
#         st.write(f"Class ID: {class_id}, Confidence: {confidence:.2f}")
#         st.write(f"Box Coordinates: [{x_min}, {y_min}, {x_max}, {y_max}]")
#         st.write("-" * 30)





# if image_file is not None:
  
#     img = load_image(image_file)


#     output_img = predict_class_and_box(img)


#     st.image(output_img, caption="Detected Objects", use_container_width=True)


#     detections = model(output_img)
#     for i, detection in enumerate(detections[0].boxes.xyxy):
#         x_min, y_min, x_max, y_max = detection
#         class_id = int(detections[0].boxes.cls[i])
#         confidence = detections[0].boxes.conf[i]
#         st.write(f"Detection {i+1}:")
#         st.write(f"Class ID: {class_id}, Confidence: {confidence:.2f}")
#         st.write(f"Box Coordinates: [{x_min}, {y_min}, {x_max}, {y_max}]")
#         st.write("-" * 30)