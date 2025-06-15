#delete_student.py
import os
import pickle
import firebase_admin
from firebase_admin import credentials, db, storage


if not firebase_admin._apps:
    cred = credentials.Certificate("serviceAccountKey.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': "https://face-attendance-real-tim-5f0ac-default-rtdb.firebaseio.com/",
        'storageBucket': "face-attendance-real-tim-5f0ac.firebasestorage.app"
    })

bucket = storage.bucket()


def delete_student(student_id):
    print(f"\nDeleting student: {student_id}\n")

    # 1. Delete from Firebase Realtime Database
    db_ref = db.reference(f"Students/{student_id}")
    if db_ref.get():
        db_ref.delete()
        print(f"Deleted student {student_id} from Firebase Realtime Database.")
    else:
        print(f"No record found for {student_id} in Realtime Database.")

    # 2. Delete from Firebase Storage
    blob = bucket.blob(f"Images/{student_id}.png")
    if blob.exists():
        blob.delete()
        print(f" Deleted image {student_id}.png from Firebase Storage.")
    else:
        print(f" Image not found in Firebase Storage.")

    # 3. Delete from local Images folder
    local_path = f"Images/{student_id}.png"
    if os.path.exists(local_path):
        os.remove(local_path)
        print(f"Deleted {student_id}.png from local Images folder.")
    else:
        print(f"Image not found in local folder.")

    # 4. Remove from EncodeFile.p
    try:
        with open("EncodeFile.p", "rb") as file:
            encodeListKnown, studentIds = pickle.load(file)

        if student_id in studentIds:
            index = studentIds.index(student_id)
            del encodeListKnown[index]
            del studentIds[index]

            with open("EncodeFile.p", "wb") as file:
                pickle.dump([encodeListKnown, studentIds], file)

            print(f"Removed encoding for {student_id}.")
        else:
            print(f"Student ID {student_id} not found in EncodeFile.p")
    except Exception as e:
        print(" Error reading/writing EncodeFile.p:", e)


if __name__ == "__main__":
    sid = input("Enter Student ID to delete: ").strip()
    if sid:
        delete_student(sid)
    else:
        print("Student ID cannot be empty.")
