==============================
🎓 FACE RECOGNITION ATTENDANCE SYSTEM
==============================

📁 ELC Category: Real-Time Object Detection and Drawing Effects  
📅 Academic Year: 2024–2025

──────────────────────────────
📌 PROJECT OVERVIEW
──────────────────────────────

This project implements a real-time face recognition-based attendance system using computer vision and deep learning. 
It automatically detects and identifies students via webcam feed, retrieves their data from Firebase, and marks attendance upon successful recognition.

A Streamlit-based interface is also provided to register new students with image and metadata, which updates the local encoding file and Firebase database/storage.

──────────────────────────────
⚙️ CORE FEATURES
──────────────────────────────

✅ Real-time face detection and recognition using `face_recognition`  
✅ Visual feedback with animated UI (4 Modes) using `cvzone`  
✅ Student data sync with Firebase Realtime Database  
✅ Student photos stored in Firebase Cloud Storage  
✅ Attendance counter and time-based re-entry protection  
✅ Add new students via simple web form (`Streamlit`)  
✅ Mode screens for:
   • 0: Active/default  
   • 1: Info screen with student details  
   • 2: Attendance marked  
   • 3: Already marked (cooldown)

──────────────────────────────
🛠️ TECH STACK
──────────────────────────────

• Python  
• OpenCV  
• face_recognition  
• cvzone  
• Firebase (Realtime Database + Storage)  
• Streamlit (for registration UI)  
• NumPy, Pickle  
• scikit-learn (for evaluation)

──────────────────────────────
🗂️ PROJECT STRUCTURE
──────────────────────────────

📁 Images/                → Stored student images (216x216 PNG)  
📁 Resources/Modes/       → Mode screen images (mode 0 to 3)  
📁 TestImages/            → Test images used for evaluation  
📄 main.py                → Main attendance system logic (real-time)  
📄 add_new_student.py     → Streamlit interface for student registration  
📄 EncodeGenerator.py     → Generates encoding pickle file (initial setup)  
📄 evaluate_performance.py→ Script to test recognition accuracy  
📄 EncodeFile.p           → Pickled face encodings + IDs  
📄 serviceAccountKey.json → Firebase access credentials  
📄 requirements.txt       → Python dependencies  
📄 readme.txt             → Project description (this file)

──────────────────────────────
📊 EVALUATION METRICS
──────────────────────────────

The system was evaluated using 6 test images in the `TestImages` folder.

Recognition Results:
---------------------
12332.png ➤ True: 12332 | Predicted: unknown  
12345.png ➤ True: 12345 | Predicted: 12345  
23231.png ➤ True: 23231 | Predicted: 23231  
32653.png ➤ True: 32653 | Predicted: 32653  
45623.png ➤ True: 45623 | Predicted: 45623  
55666.png ➤ True: 55666 | Predicted: 55666  

Metrics:
---------
✅ Accuracy : 83.33%  
✅ Precision: 83.33%  
✅ Recall   : 100.00%

These metrics were computed using `evaluate_performance.py` and scikit-learn.

──────────────────────────────
📦 HOW TO RUN
──────────────────────────────

1. Run `add_new_student.py` with Streamlit:
   > streamlit run add_new_student.py  
   → Fill form, upload image (216x216 PNG), submit

2. Run attendance system:
   > python main.py  
   → Automatically detects and recognizes students

3. Evaluate model (optional):
   > python evaluate_performance.py  
   → Outputs recognition accuracy/precision/recall

──────────────────────────────
📌 NOTES
──────────────────────────────

• All uploaded images must be named exactly as Student ID (e.g., `12345.png`)  
• Images must be clear, front-facing, and single face only  
• Only `.png` format supported in registration  
• Attendance won't re-mark same student within 30 seconds

──────────────────────────────
✅ READY FOR SUBMISSION
──────────────────────────────

This project fully complies with the ELC 2024–25 problem statement and demonstrates real-time computer vision, cloud integration, and performance evaluation.

