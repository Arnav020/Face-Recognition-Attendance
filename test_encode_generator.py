#test_encode_generator.py
import cv2
import pickle
import os
import face_recognition_models
# Manually set the model path to fix broken default logic
os.environ["FACE_RECOGNITION_MODEL_PATH"] = face_recognition_models.__path__[0] + "/models"
import face_recognition
import firebase_admin
from firebase_admin import db
from firebase_admin import storage
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://face-attendance-real-tim-5f0ac-default-rtdb.firebaseio.com/",
    'storageBucket':"face-attendance-real-tim-5f0ac.firebasestorage.app"
})


#importing student images into a list
folderPath='Images'
pathList=os.listdir(folderPath)
imgList=[]
studentIds=[]
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath,path))) 
    studentIds.append(os.path.splitext(path)[0]) # os.path.splittext(path)[0] #accesing only 12356 from 123456 + .png

    #Also uploading images to firebase storage
    fileName=f'{folderPath}/{path}'
    bucket=storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)

def findEncodings(imagesList):
    encodeList=[]
    for image in imagesList:
        img=cv2.cvtColor(image,cv2.COLOR_BGR2RGB) #face_recognition uses RGB format
        encode=face_recognition.face_encodings(img)[0] #encode
        encodeList.append(encode)
        
    return encodeList

print("Encoding Started...")
encodeListKnown=findEncodings(imgList)
encodeListKnownWithIds=[encodeListKnown, studentIds]
print("Encoding Complete")

file=open("EncodeFile.p",'wb')
pickle.dump(encodeListKnownWithIds,file) #creating a pickle file for fetching while webcam
file.close()
print("File Saved")