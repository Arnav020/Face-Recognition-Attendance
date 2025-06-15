#evaluate_performance.py
import os
import cv2
import face_recognition
import pickle
from sklearn.metrics import precision_score, recall_score, accuracy_score

# Load known encodings
with open("EncodeFile.p", "rb") as f:
    encodeListKnown, studentIds = pickle.load(f)

test_folder = "TestImages"
y_true = []
y_pred = []

# Process test images
for filename in os.listdir(test_folder):
    if filename.endswith(".png") or filename.endswith(".jpg"):
        true_id = os.path.splitext(filename)[0]
        img_path = os.path.join(test_folder, filename)
        img = cv2.imread(img_path)
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(img_rgb)
        encodings = face_recognition.face_encodings(img_rgb, face_locations)

        if len(encodings) == 0:
            print(f"No face found in {filename}")
            continue

        test_encoding = encodings[0]
        matches = face_recognition.compare_faces(encodeListKnown, test_encoding, tolerance=0.45)
        face_distances = face_recognition.face_distance(encodeListKnown, test_encoding)

        if True in matches:
            best_match_index = face_distances.argmin()
            predicted_id = studentIds[best_match_index]
        else:
            predicted_id = "unknown"

        print(f"{filename} ➤ True: {true_id} | Predicted: {predicted_id}")
        y_true.append(true_id)
        y_pred.append(predicted_id)

# Normalize to binary labels for precision/recall
y_true_binary = [1 if y == y_pred[i] else 0 for i, y in enumerate(y_true)]
y_pred_binary = [1 if y == y_pred[i] else 0 for i, y in enumerate(y_pred)]

precision = precision_score(y_true_binary, y_pred_binary, zero_division=0)
recall = recall_score(y_true_binary, y_pred_binary, zero_division=0)
accuracy = accuracy_score(y_true_binary, y_pred_binary)

print("\n📊 Evaluation Summary:")
print(f"✅ Accuracy : {accuracy * 100:.2f}%")
print(f"✅ Precision: {precision * 100:.2f}%")
print(f"✅ Recall   : {recall * 100:.2f}%")
