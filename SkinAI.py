import streamlit as st
import numpy as np
import tensorflow as tf
from PIL import Image
import keras
import gdown
import os
import tempfile
import datetime
import io
import datetime
import io
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account
import json
import gspread

 # إعداد الصفحة
st.set_page_config(page_title="SkinAI", layout="wide")
class_names = ["chickenpox", "hfmd", "measles", "unknown"]

# @st.cache_resource
# def download_and_load_model():
#      file_id = "1LQ4HD_VvWffWkyy3EIfIcRRgoGkmAbMz"  # تأكد أنه بدون "_"
#      url = f"https://drive.google.com/uc?id={file_id}"
#      with tempfile.NamedTemporaryFile(delete=False, suffix=".keras") as tmp_file:
#          gdown.download(url, tmp_file.name, quiet=False)
#          return keras.models.load_model(tmp_file.name)

# try:
#      model = download_and_load_model()
#      st.success("✅ VGG19 model loaded successfully!")
# except Exception as e:
#      st.error(f"❌ Error loading model: {e}")


Drive_folder_id = "1QjKqimyKX79TCBzyZq8eU0vMbMbs0w1D"

service_account_info = dict(st.secrets["google_service_account"])
scopes = ['https://www.googleapis.com/auth/drive','https://www.googleapis.com/auth/spreadsheets']
credentials = service_account.Credentials.from_service_account_info(service_account_info)
creds_with_scope = credentials.with_scopes(scopes)


def upload_to_drive(image_bytes, folder_id, filename):
    try:
       
        # Build Drive API client
        drive_service = build('drive', 'v3', credentials=creds_with_scope)

        # Prepare metadata and media
        file_metadata = {
            'name': filename,
            'parents': [folder_id]
        }
        media = MediaIoBaseUpload(io.BytesIO(image_bytes), mimetype='image/png')

        # Upload the file
        file = drive_service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()

        # Make it publicly accessible
        file_id = file.get('id')
        drive_service.permissions().create(
            fileId=file_id,
            body={'role': 'reader', 'type': 'anyone'},
        ).execute()

        return f"https://drive.google.com/uc?id={file_id}"
    except Exception as e:
        print(f"Error uploading to Google Drive: {e}")
        return None

def write_to_google_sheet(image_link, timestamp, prediction, confidence):
    try:

        # Authenticate using the service account credentials
        gc = gspread.authorize(creds_with_scope)

        # Open the spreadsheet
        worksheet = gc.open_by_url("https://docs.google.com/spreadsheets/d/1QfT6B7VodasOaiu77yQhmST5w-8NcOtPwZ_aT4NcteM/edit?gid=").get_worksheet_by_id("0")

        # Prepare the data to be written
        data = [image_link, timestamp, prediction, confidence]

        # Write the data as a new row in the sheet
        worksheet.append_row(data)
        print(f"Data successfully written to Google sheet.")
        return True
    except Exception as e:
        print(f"Error writing to Google Sheets: {e}")
        return False

file_id = "1pRUGLcLattWs4MI2U9YFq8ltbbSF7p1_"
tmp_model_path = None  # Initialize tmp_model_path outside the try block

try:
    # Create a temporary file path
    with tempfile.NamedTemporaryFile(delete=False, suffix=".keras") as tmp_file:
        tmp_model_path = tmp_file.name
        print(f"Temporary model file will be saved to: {tmp_model_path}")

    # Download the model from Google Drive using gdown
    print(f"Downloading model from Google Drive ID: {file_id} to c:/Users/emanm/OneDrive/Desktop/python/New folder/task2")
    gdown.download(f"https://drive.google.com/uc?id={file_id}", tmp_model_path, quiet=False)
    print("Download complete.")

    # Load the model
    print(f"Loading model from: {tmp_model_path}")
    model = keras.models.load_model(tmp_model_path)
    print("Model loaded successfully!")
    st.success("VGG19 model loaded successfully!")

except Exception as e:
    st.error(f"An error occurred: {e}")
finally:
    # Clean up the temporary file
    try:
        os.remove(tmp_model_path)
        print(f"Temporary file {tmp_model_path} removed.")
    except OSError as e:
        print(f"Error removing temporary file {tmp_model_path}: {e}")




 # UI Styling
css = f"""
     <style>
     .stApp {{
         background-image: url("https://i0.wp.com/post.healthline.com/wp-content/uploads/2022/04/hand-foot-and-mouth-disease-body8.jpg?w=1155&h=1528");
         background-size: cover;
         background-position: center;
         font-family: 'Arial', sans-serif;
     }}
     .custom-box {{
         background-color: #A0522D;
         border-radius: 30px;
         padding: 40px;
         max-width: 500px;
         margin: auto;
         box-shadow: 0px 4px 20px rgba(0,0,0,0.2);
         text-align: center;
     }}
     .TAKE-PICTURE {{
         background-color: white;
         color: #0D0D1C;
         border-radius: 20px;
         padding: 10px 20px;
         font-size: 16px;
         font-weight: bold;
         border: none;
         box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
         margin: 10px;
     }}
     .upload{{
         background-color: white;
         color: #0D0D1C;
         border-radius: 20px;
         padding: 10px 20px;
         font-size: 16px;
         font-weight: bold;
         border: none;
         box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
         margin: 10px;
     }}
     .title {{
         color: black;
         font-size: 36px;
         font-weight: 800;
         margin-bottom: 20px;
     }}
     .subtitle {{
         font-size: 18px;
         color: #0D0D1C;
     }}
     .logo {{
         position: absolute;
         top: 20px;
         right: 20px;
         max-height: 60px;
     }}
     </style>
     """
st.markdown(css, unsafe_allow_html=True)


# # Logo and title on left
st.markdown("""
     <div style="position: absolute; top: -75px; left: -50px; color: white;">
         <h1 style="color: black;"><strong>Skin<span style='color:#4F9CDA'>AI</span></strong></h1>
         <p style="font-size:20px; color:black;">AI-POWERED CHILD<br>SKIN DISEASE DETECTION</p>
     </div>
""", unsafe_allow_html=True)

 # Center UI
 # st.markdown('<div class="custom-box"><div class="title">CHECK SKIN</div> <button class="TAKE-PICTURE" onclick="image_data = takePicture()">Take Picture </button> <button class="upload" onclick="uploadPicture()">UPLOAD PICTURE </button>', unsafe_allow_html=True)
 # Function to handle picture taking (could be connected to a camera API)

st.markdown("""
     <style>
         .custom-box {
             background-color: #f2f2f2;
             padding: 20px;
             border-radius: 10px;
             box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
             display: flex;
             flex-direction: column;
             align-items: center;
             gap: 10px;
         }
         .custom-box .title {
             font-size: 20px;
             font-weight: bold;
             margin-bottom: 10px;
         }
         .custom-box button {
             padding: 10px 20px;
             background-color: #007bff;
             color: white;
             border: none;
             border-radius: 5px;
             cursor: pointer;
         }
         .custom-box button:hover {
             background-color: #0056b3;
         }
     </style>
     <div class="custom-box">
         <div class="title">CHECK SKIN</div>
     </div>
""", unsafe_allow_html=True)


 # Upload or take image
uploaded_file = st.file_uploader("Upload a skin image", type=["jpg", "jpeg", "png"])
camera_file = st.camera_input("Or take a picture")

 # Use uploaded image or camera input
image_data = uploaded_file if uploaded_file else camera_file



if image_data is not None:
     timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
     filename = f"captured_image_{timestamp}.jpg" 
     img = Image.open(image_data).convert("RGB")
     img_resized = img.resize((224, 224))
     img_array = np.array(img_resized) / 255.0
     img_input = np.expand_dims(img_array, axis=0)

     # Predict
     predictions = model.predict(img_input)
     predicted_class = class_names[np.argmax(predictions)]
     confidence = float(np.max(predictions)) * 100

     # Show result screen
    
     st.image(img.resize((350, 350)), caption="Uploaded Image", use_column_width=False)
     st.markdown(f"""
         <div style='background-color:#FFFFFF;padding:20px;border-radius:15px;text-align:center;margin-top:20px'>
             <h2 style='color:#FF4444;'>Disease: {predicted_class.upper()}</h2>
             <p style='font-size:20px; color: black;'>Confidence: {confidence:.2f}%</p>
         </div>
     """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

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


try:
      if isinstance(image_data, bytes):
          image_bytes = image_data
      elif isinstance(image_data, io.BytesIO):
          image_bytes = image_data.getvalue()
      elif hasattr(image_data, 'read'):
          image_bytes = image_data.read()
      else:
          raise ValueError("Unsupported image data type")


      drive_url = upload_to_drive(image_bytes, Drive_folder_id, filename)
      sheet_status = write_to_google_sheet(drive_url,timestamp,predicted_class,confidence)
      if sheet_status :
          st.success(f"Image uploaded to Database!")               
      else:
          st.error("Failed to upload image to Database")
            
except Exception as e:
      st.error(f"Error uploading to Google Drive: {e}")
      print(f"Error uploading to Google Drive: {e}")

