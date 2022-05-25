from base64 import b64decode
import face_recognition as fr
import time
import os
import pickle  

def login_check(email, image):
    face_match = 0
    header, encoded = image.split(",", 1)

    with open("New.png", "wb") as f:
        f.write(b64decode(encoded))

    data = pickle.loads(open("data.pickle", "rb").read())

    if email not in data.keys():
        return "This user ID is not registered yet"

    with open("Existing.png", "wb") as f:
        f.write(b64decode(data[email]))
    
    try:
        try:
            got_image = fr.load_image_file("New.png")
            existing_image = fr.load_image_file("Existing.png")
        except Exception as e:
            # print(e.__cause__)
            return "Data does not exist !"

        face_locations = fr.face_locations(got_image)
        if(len(face_locations)==0):
            return "No face detected"
        if(len(face_locations)>1):
            return "Multiple faces detected"
            
        got_image_facialfeatures = fr.face_encodings(got_image)[0]
        existing_image_facialfeatures = fr.face_encodings(existing_image)[0]
        results = fr.compare_faces([existing_image_facialfeatures], got_image_facialfeatures)
        if(results[0]):
            return "Successfully Logged in"
        else:
            return "User ID and face doesn't match!"
    except Exception as e:
        # print(e.__cause__)
        return "Image not clear ! Please try again !"