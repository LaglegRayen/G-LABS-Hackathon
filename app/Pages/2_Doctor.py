import streamlit as st
st.set_page_config(page_title="🧠 Doctor Portal - Brain Tumor Assistant", layout="wide")
    

import pandas as pd
import os
import time
from template import generate_report
from yolo import predict_class_and_box, load_image, model
from pdf_generator import save_report_to_pdf
from streamlit_pdf_viewer import pdf_viewer
import shutil
from datetime import date


notes_dir = r"notes"
reports_dir = r"reports"
os.makedirs(notes_dir, exist_ok=True)
os.makedirs(reports_dir, exist_ok=True)


st.title("🧠 Doctor Portal - Brain Tumor Assistant")

today = date.today()


formatted_date = today.strftime("%Y-%m-%d")

tab1, tab2= st.tabs(["🧪MRI Analysis","📋 Dashboard & Notes"])

with tab1:
    st.header("🧪 MRI Analysis")
    patient_id = st.text_input("Enter Patient ID", key="patient_id_input_tab1")

    if patient_id:
        image_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

        if image_file is not None:
            upload_dir = "uploads"
            
            class_names = ['Glioma', 'Meningioma', 'No Tumor', 'Pituitary']
            conf = []
            predictions = []
            ext = os.path.splitext(image_file.name)[1]
            img = load_image(image_file)
            output_img = predict_class_and_box(img)
            save_path = os.path.join(upload_dir, f"{patient_id}_{formatted_date}.{ext}")
            with open(save_path, "wb") as f:
                f.write(image_file.getbuffer())

            with st.spinner('Analyzing your scan...'):
                time.sleep(2)
            st.image(output_img, caption="Detected Objects", use_container_width=True)
            detections = model(output_img)
            for i, detection in enumerate(detections[0].boxes.xyxy):
                
        
                x_min, y_min, x_max, y_max = detection
                class_id = int(detections[0].boxes.cls[i])
                if class_id not in predictions:
                    predictions.append(class_id)
                    confidence = detections[0].boxes.conf[i]
                conf.append(confidence)
                if class_id == 2:
                    break
            if class_id == 2:
                with st.spinner("No Tumor Detected..."):
                    time.sleep(2)
                st.success("No Tumor Detected")

            # for i in range(len(predictions)):
            #     if predictions[i] == 2:
            #         st.success("No Tumor Detected")
            #         predictions.remove(predictions[i])
            #         conf.remove(conf[i])
            #     else:
            #         st.warning("Type of Tumor Detected: "+ class_names[predictions[i]]+ f" Confidence:  {conf[i]*100:.2f}%")
            else:
                st.subheader("📄 Generate Patient Report")
                report_text = generate_report("MR SOULE M MADI ALI", 45,conf,x_min, y_min, x_max, y_max)
            

                filename = save_report_to_pdf(report_text, f"{patient_id}_{formatted_date}_report.pdf")
                specified_path = os.path.join("reports", f"{patient_id}_{formatted_date}_report.pdf") 
                shutil.copy(filename, specified_path)
                with open(filename, "rb") as f:
                    with st.spinner('Creating your report...'):
                        time.sleep(2)
                    pdf_data = f.read()
                    
                    pdf_viewer(pdf_data)
                # st.download_button("Click to Download your Report", data=pdf_data, file_name=f"{patient_id}_report.pdf", mime="application/pdf")
            
with tab2:
    st.header("📋 Patient Dashboard and Notes")

    
    patient_id = st.text_input("Enter Patient ID", key="patient_id_input_tab2")

    if patient_id:
        st.divider()
        st.subheader("📝 Write Doctor Notes")
            
        
        patient_notes_path = os.path.join(notes_dir, f"{patient_id}_notes.txt")
        with open(patient_notes_path, "r") as f:
            previous_notes = f.read()
        notes = st.text_area("Previous Notes:", previous_notes, height=200)
        if st.button("💾 Save Notes"):
            with open(patient_notes_path, "w") as f:
                    f.write(notes)
            st.success(f"Notes for Patient {patient_id} saved successfully!")
        
        st.divider()
    
 

      
