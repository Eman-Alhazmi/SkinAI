
# import streamlit as st
# import numpy as np
# import tensorflow as tf
# from PIL import Image
# import keras
# import gdown
# import os
# import tempfile

# # إعداد الصفحة
# st.set_page_config(page_title="SkinAI", layout="wide")
# class_names = ["chickenpox", "hfmd", "measles", "unknown"]

# @st.cache_resource
# def download_and_load_model():
#     file_id = "1LQ4HD_VvWffWkyy3EIfIcRRgoGkmAbMz"  # تأكد أنه بدون "_"
#     url = f"https://drive.google.com/uc?id={file_id}"
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".keras") as tmp_file:
#         gdown.download(url, tmp_file.name, quiet=False)
#         return keras.models.load_model(tmp_file.name)

# try:
#     model = download_and_load_model()
#     st.success("✅ VGG19 model loaded successfully!")
# except Exception as e:
#     st.error(f"❌ Error loading model: {e}")



# # UI Styling
# css = f"""
#     <style>
#     .stApp {{
#         background-image: url("https://i0.wp.com/post.healthline.com/wp-content/uploads/2022/04/hand-foot-and-mouth-disease-body8.jpg?w=1155&h=1528");
#         background-size: cover;
#         background-position: center;
#         font-family: 'Arial', sans-serif;
#     }}
#     .custom-box {{
#         background-color: #A0522D;
#         border-radius: 30px;
#         padding: 40px;
#         max-width: 500px;
#         margin: auto;
#         box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
#         text-align: center;
#     }}
#     .TAKE-PICTURE {{
#         background-color: white;
#         color: #0D0D1C;
#         border-radius: 20px;
#         padding: 10px 20px;
#         font-size: 16px;
#         font-weight: bold;
#         border: none;
#         box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
#         margin: 10px;
#     }}
#     .upload{{
#         background-color: white;
#         color: #0D0D1C;
#         border-radius: 20px;
#         padding: 10px 20px;
#         font-size: 16px;
#         font-weight: bold;
#         border: none;
#         box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
#         margin: 10px;
#     }}
#     .title {{
#         color: black;
#         font-size: 36px;
#         font-weight: 800;
#         margin-bottom: 20px;
#     }}
#     .subtitle {{
#         font-size: 18px;
#         color: #0D0D1C;
#     }}
#     .logo {{
#         position: absolute;
#         top: 20px;
#         right: 20px;
#         max-height: 60px;
#     }}
#     </style>
#     """
# st.markdown(css, unsafe_allow_html=True)


# # Logo and title on left
# st.markdown("""
#     <div style="position: absolute; top: -75px; left: -50px; color: white;">
#         <h1 style="color: black;"><strong>Skin<span style='color:#4F9CDA'>AI</span></strong></h1>
#         <p style="font-size:20px; color:black;">AI-POWERED CHILD<br>SKIN DISEASE DETECTION</p>
#     </div>
# """, unsafe_allow_html=True)

# # Center UI
# # st.markdown('<div class="custom-box"><div class="title">CHECK SKIN</div> <button class="TAKE-PICTURE" onclick="image_data = takePicture()">Take Picture </button> <button class="upload" onclick="uploadPicture()">UPLOAD PICTURE </button>', unsafe_allow_html=True)
# # Function to handle picture taking (could be connected to a camera API)

# st.markdown("""
#     <style>
#         .custom-box {
#             background-color: #f2f2f2;
#             padding: 20px;
#             border-radius: 10px;
#             box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
#             display: flex;
#             flex-direction: column;
#             align-items: center;
#             gap: 10px;
#         }
#         .custom-box .title {
#             font-size: 20px;
#             font-weight: bold;
#             margin-bottom: 10px;
#         }
#         .custom-box button {
#             padding: 10px 20px;
#             background-color: #007bff;
#             color: white;
#             border: none;
#             border-radius: 5px;
#             cursor: pointer;
#         }
#         .custom-box button:hover {
#             background-color: #0056b3;
#         }
#     </style>
#     <div class="custom-box">
#         <div class="title">CHECK SKIN</div>
#     </div>
# """, unsafe_allow_html=True)


# # Upload or take image
# uploaded_file = st.file_uploader("Upload a skin image", type=["jpg", "jpeg", "png"])
# camera_file = st.camera_input("Or take a picture")

# # Use uploaded image or camera input
# image_data = uploaded_file if uploaded_file else camera_file

# if image_data is not None:
#     img = Image.open(image_data).convert("RGB")
#     img_resized = img.resize((224, 224))
#     img_array = np.array(img_resized) / 255.0
#     img_input = np.expand_dims(img_array, axis=0)

#     # Predict
#     predictions = model.predict(img_input)
#     predicted_class = class_names[np.argmax(predictions)]
#     confidence = float(np.max(predictions)) * 100

#     # Show result screen
    
#     st.image(img.resize((350, 350)), caption="Uploaded Image", use_column_width=False)
#     st.markdown(f"""
#         <div style='background-color:#FFFFFF;padding:20px;border-radius:15px;text-align:center;margin-top:20px'>
#             <h2 style='color:#FF4444;'>Disease: {predicted_class.upper()}</h2>
#             <p style='font-size:20px; color: black;'>Confidence: {confidence:.2f}%</p>
#         </div>
#     """, unsafe_allow_html=True)

# st.markdown("</div>", unsafe_allow_html=True)


import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
import keras
import gdown
import os
import tempfile

# إعداد الصفحة
st.set_page_config(page_title="SkinAI", layout="wide")
class_names = ["chickenpox", "hfmd", "measles", "unknown"]

@st.cache_resource
def download_and_load_model():
    file_id = "1LQ4HD_VvWffWkyy3EIfIcRRgoGkmAbMz"
    url = f"https://drive.google.com/uc?id={file_id}"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".keras") as tmp_file:
        gdown.download(url, tmp_file.name, quiet=False)
        return keras.models.load_model(tmp_file.name)

try:
    model = download_and_load_model()
    st.success("✅ VGG19 model loaded successfully!")
except Exception as e:
    st.error(f"❌ Error loading model: {e}")

# تنسيق CSS
st.markdown("""
    <style>
        .header {
            text-align: center;
            margin-top: 30px;
        }
        .header h1 {
            font-size: 48px;
            color: #000;
        }
        .header p {
            font-size: 18px;
            color: #555;
        }
        .button-row {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 20px;
        }
        .result-box {
            background-color: #fff;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            margin-top: 30px;
            text-align: center;
        }
        .about {
            background-color: #f9f9f9;
            padding: 40px;
            margin-top: 60px;
            border-radius: 10px;
        }
        .about h2 {
            color: #0D0D1C;
        }
        .about p {
            font-size: 16px;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# العنوان الرئيسي
st.markdown("""
    <div class="header">
        <h1><strong>Skin<span style='color:#4F9CDA'>AI</span></strong></h1>
        <p>AI-Powered Child Skin Disease Detection</p>
    </div>
""", unsafe_allow_html=True)

# رفع أو التقاط الصورة
col_upload, col_camera = st.columns(2)
with col_upload:
    uploaded_file = st.file_uploader("📤 Upload Picture", type=["jpg", "jpeg", "png"])
with col_camera:
    camera_file = st.camera_input("📷 Take Picture")

# استخدام الصورة المختارة
image_data = uploaded_file if uploaded_file else camera_file

if image_data is not None:
    img = Image.open(image_data).convert("RGB")
    img_resized = img.resize((224, 224))
    img_array = np.array(img_resized) / 255.0
    img_input = np.expand_dims(img_array, axis=0)

    # التنبؤ
    predictions = model.predict(img_input)
    predicted_class = class_names[np.argmax(predictions)]
    confidence = float(np.max(predictions)) * 100

    # عرض النتائج
    st.image(img.resize((300, 300)), caption="Uploaded Image", use_column_width=False)

    st.markdown(f"""
        <div class="result-box">
            <h2>Disease: {predicted_class.upper()}</h2>
            <p style="font-size:18px;">Confidence: {confidence:.2f}%</p>
        </div>
    """, unsafe_allow_html=True)

# قسم About Us
st.markdown("""
    <div class="about">
        <h2>About Us</h2>
        <p>
        We are a specialized team dedicated to developing intelligent solutions for children’s care. 
        We use the latest artificial-intelligence techniques to analyze skin images and detect infectious 
        skin diseases with precision and speed. Our goal is to empower parents and healthcare professionals 
        to make early diagnoses of your child’s skin conditions—saving you time and preventing symptoms from worsening.
        </p>
    </div>
""", unsafe_allow_html=True)

