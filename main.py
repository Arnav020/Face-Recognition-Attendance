import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
from datetime import datetime
import firebase_admin
from firebase_admin import db
from firebase_admin import storage
from firebase_admin import credentials


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://face-attendance-real-tim-5f0ac-default-rtdb.firebaseio.com/",
    'storageBucket': "face-attendance-real-tim-5f0ac.firebasestorage.app"
})
bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(3, 640)  # Set width
cap.set(4, 480)  # Set height

imgBackground = cv2.imread('Resources/background.png')

# Importing mode images into a list
folderModepath = 'Resources/Modes'
modePathList = os.listdir(folderModepath)
imgModeList = []
for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModepath, path)))

# Load the encoding file
print("Loading Encode File...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
print("Encode File Loaded Successfully")

modeType = 0
counter = 0
id = -1
imgStudent = []
noFaceCounter = 0
maxNoFaceFrames = 10  # adjust if needed

persistent_id = -1
stable_counter = 0
STABLE_FRAMES = 3
lock_time = None  # to freeze system after attendance is marked

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25) # Making image small for less computation
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS) #Locataion of curr face seen
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame) #encoding that face

    imgBackground[162:162 + 480, 55:55 + 640] = img

    #  freeze screen for 3 seconds after attendance marked
    if lock_time and (datetime.now() - lock_time).total_seconds() < 3:
        cv2.imshow("Face Attendance", imgBackground)
        cv2.waitKey(1)
        continue
    else:
        lock_time = None

    if faceCurFrame:
        noFaceCounter = 0
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace) #compare with known encodings
            faceDist = face_recognition.face_distance(encodeListKnown, encodeFace)
            matchIndex = np.argmin(faceDist) #match is where the distance is min from knwon encodings

            if matches[matchIndex]:
                matched_id = studentIds[matchIndex]
                if matched_id == persistent_id:
                    stable_counter += 1
                else:
                    persistent_id = matched_id
                    stable_counter = 1

                if stable_counter >= STABLE_FRAMES:
                    y1, x2, y2, x1 = faceLoc
                    y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4 #scaling back to orginal size
                    bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1 #offset, offset, height, width
                    imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                    id = studentIds[matchIndex]

                    if counter == 0:
                        cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                        cv2.imshow("Face Attendance", imgBackground)
                        cv2.waitKey(1)
                        counter = 1
            else:
                stable_counter = 0
                persistent_id = -1
    else:
        noFaceCounter += 1
        if noFaceCounter >= maxNoFaceFrames:
            modeType = 0
            counter = 0
            id = -1
            studentInfo = []
            imgStudent = []
            imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

    if counter != 0:

        if counter == 1:
            #Loading student details
            studentInfo = db.reference(f'Students/{id}').get()
            print(studentInfo)
            #Loading Image
            blob = bucket.get_blob(f'Images/{id}.png')
            array = np.frombuffer(blob.download_as_string(), np.uint8)
            imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2BGR)

            if studentInfo:
                # Only switch to mode 1 when details have been fetched
                modeType = 1  
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]  

            datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
            secondsElapsed = (datetime.now() - datetimeObject).total_seconds()
            print(secondsElapsed)

            if secondsElapsed > 30:
                ref = db.reference(f'Students/{id}')
                studentInfo['total_attendance'] += 1
                ref.child('total_attendance').set(studentInfo['total_attendance'])
                ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                lock_time = datetime.now()
            else:
                modeType = 3
                counter = 0
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                lock_time = datetime.now()

        if modeType != 3:

            if 10 < counter < 20:
                modeType = 2
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]

            if counter <= 10:
                cv2.putText(imgBackground, str(studentInfo['total_attendance']), (861, 125),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                cv2.putText(imgBackground, str(studentInfo['major']), (1006, 550),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgBackground, str(id), (1006, 493),
                            cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 255, 255), 1)
                cv2.putText(imgBackground, str(studentInfo['standing']), (910, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(studentInfo['year']), (1025, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)
                cv2.putText(imgBackground, str(studentInfo['starting_year']), (1125, 625),
                            cv2.FONT_HERSHEY_COMPLEX, 0.6, (100, 100, 100), 1)

                (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                offset = (414 - w) // 2 # setting offset to always centre the name irrespective of len
                cv2.putText(imgBackground, str(studentInfo['name']), (808 + offset, 445),
                            cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 50), 1)

                imgBackground[175:175 + 216, 909:909 + 216] = imgStudent

            counter += 1

            if counter >= 20:
                counter = 0
                modeType = 0
                id = -1
                studentInfo = []
                imgStudent = []
                imgBackground[44:44 + 633, 808:808 + 414] = imgModeList[modeType]
                stable_counter = 0
                persistent_id = -1

    cv2.imshow("Face Attendance", imgBackground)
    cv2.waitKey(1)
