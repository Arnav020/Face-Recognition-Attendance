#add_new_student.py
import streamlit as st
import cv2
import numpy as np
import face_recognition
import os
import pickle
from datetime import datetime
import firebase_admin
from firebase_admin import credentials, db, storage

if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://face-attendance-real-tim-5f0ac-default-rtdb.firebaseio.com/",
        'storageBucket': "face-attendance-real-tim-5f0ac.firebasestorage.app"
    })

bucket = storage.bucket()


st.title("👤 Add New Student - Face Attendance System")

st.markdown("""
> ⚠️ **Note:** You can either upload a `.png` image or use your webcam.  
> The image name **should match your Student ID**, e.g., `12345.png`
""")

with st.form("student_form", clear_on_submit=False):
    student_id = st.text_input("Student ID")
    name = st.text_input("Full Name")
    major = st.text_input("Major")
    year = st.number_input("Year", min_value=1, max_value=6)
    standing = st.selectbox("Standing", ["A", "B", "G"])
    starting_year = st.number_input("Starting Year", min_value=2000, max_value=datetime.now().year)

    image_file = st.file_uploader("Upload Student Image (.png only)", type=["png"])
    st.markdown("**OR**")
    live_image = st.camera_input("Capture Photo via Webcam")

    submitted = st.form_submit_button("➕ Add Student")

# Submission Logic
if submitted:
    if not (student_id and name and major and (image_file or live_image)):
        st.error("🚫 Please fill all fields and upload or capture a valid image.")
    else:
        # Choose image source
        source = image_file if image_file else live_image
        img_bytes = np.asarray(bytearray(source.read()), dtype=np.uint8)
        img = cv2.imdecode(img_bytes, cv2.IMREAD_COLOR)

        if img is None:
            st.error("🚫 Could not read image.")
        else:
            img_resized = cv2.resize(img, (216, 216))
            img_path = f"Images/{student_id}.png"
            cv2.imwrite(img_path, img_resized)
            st.image(img_resized, caption="✅ Resized to 216x216", channels="BGR")

            # Upload to Firebase Storage
            blob = bucket.blob(f"Images/{student_id}.png")
            blob.upload_from_filename(img_path)

            # Update Firebase DB
            ref = db.reference(f"Students/{student_id}")
            ref.set({
                "name": name,
                "major": major,
                "starting_year": starting_year,
                "total_attendance": 0,
                "standing": standing,
                "year": year,
                "last_attendance_time": "2000-01-01 00:00:00"
            })

            # Update encodings
            with open("EncodeFile.p", "rb") as f:
                encodeListKnown, studentIds = pickle.load(f)

            rgb_img = cv2.cvtColor(img_resized, cv2.COLOR_BGR2RGB)
            encodings = face_recognition.face_encodings(rgb_img)

            if len(encodings) == 0:
                st.error("🚫 No face detected in the image. Use a clearer photo.")
            else:
                encodeListKnown.append(encodings[0])
                studentIds.append(student_id)
                with open("EncodeFile.p", "wb") as f:
                    pickle.dump([encodeListKnown, studentIds], f)
                st.success(f"✅ {name} added successfully!")
