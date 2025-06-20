# 🎓 Face Recognition Attendance System

> ⚡ Real-time computer vision meets cloud-powered student attendance  
> 🧠 Built with OpenCV · face_recognition · Firebase · Streamlit

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen.svg)

---

## 📁 ELC Category: Real-Time Object Detection and Drawing Effects  
📅 Academic Year: 2024–2025

---

## 📌 Project Overview

This project implements a **real-time face recognition-based attendance system** using computer vision and deep learning.  
It automatically detects and identifies students via webcam feed, retrieves their data from Firebase, and marks attendance upon successful recognition.

➡️ A **Streamlit interface** is also provided to register new students with image and metadata, which updates the local encoding file and Firebase Realtime DB.

---

## ⚙️ Core Features

- ✅ Real-time face detection and recognition (`face_recognition`)
- ✅ Visual UI with animated mode screens via `cvzone`
- ✅ Student data sync with Firebase Realtime Database
- ✅ Student photo upload to Firebase Cloud Storage
- ✅ Attendance protection (no re-marking within 30 seconds)
- ✅ Simple student registration via Streamlit web form
- ✅ Four mode screens:
  - `Mode 0`: Default  
  - `Mode 1`: Display student info  
  - `Mode 2`: Attendance marked  
  - `Mode 3`: Already marked (cooldown)

---

## 🛠️ Tech Stack

- Python 3.12  
- OpenCV  
- face_recognition  
- Firebase (Realtime DB + Cloud Storage)  
- Streamlit  
- NumPy, Pickle  
- scikit-learn (for evaluation)

---

## 🗂️ Project Structure

```text
📁 Images/                → Stored student images (216x216 PNG)
📁 Resources/Modes/       → Mode screen images (0–3)
📁 TestImages/            → Images used for performance evaluation

📄 main.py                → Real-time attendance logic
📄 add_new_student.py     → Streamlit interface for registration
📄 EncodeGenerator.py     → Generates EncodeFile.p
📄 evaluate_performance.py→ Model evaluation script
📄 EncodeFile.p           → Pickled face encodings and IDs
📄 serviceAccountKey.json → 🔒 Firebase credentials (excluded from Git)
📄 requirements.txt       → Project dependencies
📄 README.md              → Project documentation (this file)
