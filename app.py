import streamlit as st
import google.generativeai as genai
from api_key import api_key  

genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.4,
    "top_p": 1,
    "top_k": 32,
    "max_output_tokens": 4096,
}

safety_setting = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

# Medical AI System Prompt
system_prompt = """You are a highly skilled medical AI assistant specializing in the analysis of medical images. 
Your role is to assist in identifying potential abnormalities and providing professional observations, 
 but you do not provide definitive medical diagnoses.  
Your primary responsibilities include:
1. Conducting accurate, detailed, and objective assessments of medical images.
2. Offering clear and professional medical observations based on recognized medical standards.
3. Identifying any abnormalities, anomalies, or areas of concern that require further evaluation.
4. Utilizing precise medical terminology while ensuring explanations remain accessible to healthcare professionals and patients.
5. Adhering strictly to medical ethics, data privacy regulations, and maintaining patient confidentiality.
6. Providing insights that serve as guidance, while reminding users that your analysis should not replace a professional medical diagnosis or consultation.
7. Offering potential differential diagnoses where applicable and suggesting possible next steps based on findings.

Please examine the provided medical image and share your detailed insights.
"""


model = genai.GenerativeModel(model_name="gemini-1.5-flash", 
                              generation_config=generation_config,
                              safety_settings=safety_setting)

# Streamlit UI Setup
st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")

# Load Logo
st.image("logo.png", width=100)

st.title("👨‍⚕️ Vital ❤️ Image 📷 Analytics 📊")
st.subheader("An application that can help users to identify medical images")

# Upload Image
uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", width=300)

submit_button = st.button("🩺 Generate Analysis")

if submit_button:
    if uploaded_file is not None:
        try:
          
            image_data = uploaded_file.getvalue()
            mime_type = uploaded_file.type 

            image_parts = [
                {
                    "mime_type": mime_type,
                    "data": image_data
                }
            ]

            prompt_parts = [image_parts[0], system_prompt]

 # Generate response using Gemini AI
            response = model.generate_content(prompt_parts)

            if response and hasattr(response, "text"):
                st.write("### 🏥 Medical Analysis Report:")
                st.write(response.text)
            else:
                st.error("⚠️ No response received. Please try again.")

        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
    else:
        st.warning("⚠️ Please upload an image before submitting.")
