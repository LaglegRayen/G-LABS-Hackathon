

from llama_index.llms.groq import Groq
from llama_index.embeddings.gemini import GeminiEmbedding
from llama_index.core import Settings, VectorStoreIndex, SimpleDirectoryReader

import os
from dotenv import load_dotenv

llm = Settings.llm = Groq(
    model="llama-3.1-8b-instant",
    api_key= os.getenv("GROQ_CLOUD_API_KEY"),
    temperature=0.7
)


Settings.embed_model = GeminiEmbedding(
    model_name="models/embedding-001",
    api_key= os.getenv("GOOGLE_API_KEY")
)



# # Example of patient data and usage
# # patient_info = "Name: John Doe, Age: 45, Sex: Male, Scan Date: 2025-04-25"
# # diagnosis = "Glioma detected with 93% confidence."
# # tumor_characteristics = "Tumor located in left frontal lobe, size approx 30mm."
# # suggestions = "Recommend immediate neurosurgical consultation."


def generate_report(patient_info, class_type, confidence, X, Y, W, H):
    # system_prompt = f"""
    # You are a medical AI assistant. Write a formal diagnostic report based on the following inputs:
    # - Patient Information: {patient_info}
    # - Image Analysis Result: Tumor Type = {class_type}, Detection Confidence = {confidence}%, Tumor Bounding Box = (X = {X}, Y= {Y}, W={W}, H = {H}).

    # Your report must follow this structure:
    # ---
    # Patient Information:
    # {patient_info}

    # Diagnosis Summary:
    # - Detected tumor type: {class_type}
    # - Detection confidence: {confidence}%

    # Tumor Characteristics:
    # - Provide general characteristics of the detected tumor type (e.g., typical growth rate, aggressiveness, common locations, etc.).
    # - Estimate tumor size based on bounding box width and height (W, H) if available.
    # - Do NOT mention exact X, Y coordinates — just give an approximate idea (like "likely affecting frontal lobe" if appropriate).

    # Clinical Interpretation:
    # - Explain briefly what this tumor type usually means medically.
    # - Mention prognosis hints, risks, and expected clinical behavior.

    # Suggested Next Steps:
    # - Suggest necessary next actions (e.g., further imaging, biopsy, specialist consultation).
    # - Recommend urgent referral if the tumor type is aggressive.
    # - Suggest general advice for both doctors and patients.

    # Notes:
    # - Provide any cautionary notes.
    # - Mention symptoms that would require immediate medical attention.
    # - Advise patient on importance of early intervention.
    # ---
    # Important instructions:
    # - Be professional, clear, medically accurate, and supportive.
    # - Focus on delivering meaningful insights for both doctors and patients.
    # - Avoid raw technical details like coordinates or technical terms unfamiliar to non-specialists.
    # """
    system_prompt = f"""
You are a medical AI assistant. Write a formal diagnostic report based on the following structured inputs:
- Patient Information: {patient_info}
- Image Analysis Result: Tumor Type = {class_type}, Detection Confidence = {confidence}%, Tumor Bounding Box = (X = {X}, Y= {Y}, W={W}, H = {H}).

The report should have the following clear structure, with headers and organized sections:
if type = 45 dont specify it else specify it
==================================================
               MEDICAL DIAGNOSTIC REPORT
==================================================

Patient Information:
--------------------
{patient_info}


Tumor Characteristics:
--------------------
- General description of the detected tumor (growth rate, aggressiveness, common locations).
- Estimated tumor size based on bounding box width and height (W={W}, H={H}).
- Approximate affected brain region if possible (do NOT mention X, Y directly).

Clinical Interpretation:
--------------------
- Medical implications of the detected tumor.
- Prognosis hints, risks, and typical clinical evolution.

Suggested Next Steps:
--------------------
- Recommend immediate actions (biopsy, further imaging, specialist referral).
- Mention if urgent referral is needed.
- Provide supportive advice for doctors and patients.

Notes:
--------------------
- Cautionary advice and urgent warning symptoms.
- Importance of early intervention.

==================================================

Important:
- Be formal, accurate, supportive, and easy to understand.
- Avoid using technical coordinate references or jargon unfamiliar to non-medical readers.
"""


    result = llm.complete(system_prompt)

    return result

    