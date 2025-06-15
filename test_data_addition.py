#test_data_addition.py
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://face-attendance-real-tim-5f0ac-default-rtdb.firebaseio.com/"
})

ref = db.reference('Students')

data = {
    "12345":
        {
            "name":"Arnav Joshi",
            "major":"ML",
            "starting_year":2023,
            "total_attendance":6,
            "standing":"G",
            "year":3,
            "last_attendance_time":"2025-05-28 00:54:34"
        },

    "32653":
        {
            "name":"Elon Musk",
            "major":"Aeronautics",
            "starting_year":2018,
            "total_attendance":12,
            "standing":"A",
            "year":4,
            "last_attendance_time":"2025-05-29 11:14:34"
        },

    "45623":
        {
            "name":"Keanu Reeves",
            "major":"Assasination",
            "starting_year":2021,
            "total_attendance":2,
            "standing":"B",
            "year":2,
            "last_attendance_time":"2025-02-28 09:21:34"
        },
    "23231":
        {
            "name":"Parminder Kaur",
            "major":"Journalism",
            "starting_year":2021,
            "total_attendance":2,
            "standing":"G",
            "year":2,
            "last_attendance_time":"2025-02-28 09:21:34"
        }
}

for key,value in data.items(): #updating data
    ref.child(key).set(value)


