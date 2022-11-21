from gettext import install
import cv2  
import numpy as np
import face_recognition
import os
from datetime import datetime
# pip install face_recognition library for encodings
# PIL for images

path = 'images'
images = []
classNames = []
myList = os.listdir(path)
# print(myList)

# code to find number of registered images in file
for item in myList:
    # differentiate imsge from file and store in diffImg
    diffImg = cv2.imread(f'{path}/{item}')
    # appends images in images[] array
    images.append(diffImg)
    # appends images to classNames[] array after removing extensions
    classNames.append(os.path.splitext(item)[0])
print(classNames)


# to find face features from images
def findEncodings(images):
    # to store encodings
    encodeList = []


    for img in images:
        # converting images to black and white
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # calling face_encodings function and passing b&w images as params
        encode = face_recognition.face_encodings(img)[0]
        # appends encodes of images in encodeList[] array
        encodeList.append(encode)
    return encodeList


# for attendance
def markAttendance(name):
    with open('Attendance.csv', 'r+', encoding="mbcs") as f:
        myDataList = f.readlines()


        nameList = []
        for line in myDataList:
            entry = line.split(',')
            # appends name in list from myDataList
            nameList.append(entry[0])

        if name not in nameList:
            # time from system
            now = datetime.now()
            # changing format
            markTime = now.strftime("%m/%d/%Y,%H:%M:%S")
            f.writelines(f'\n{name},{markTime}')



encodeListKnown = findEncodings(images)
print('Encoding Complete')

# initializing web cam
cap = cv2.VideoCapture(0)


while True:
    # result: True or False
    # img: coords
    result, img = cap.read()
    
    # resizing the image
    newImg = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # converting from black and grey to colours
    newImg = cv2.cvtColor(newImg, cv2.COLOR_BGR2RGB)

    # taking face locations
    facesLocFrame = face_recognition.face_locations(newImg)
    
    encodesLocFrame = face_recognition.face_encodings(newImg, facesLocFrame)


    for encodeFace, faceLoc in zip(encodesLocFrame, facesLocFrame):
        # comparision of faces from list known and capture in video
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)

        # print(faceDis)
        # returns indices of min values along axis
        matchIndex = np.argmin(faceDis)

        # if matches then that classname value (name of person) is stored in name in uppercase
        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            
            # print(name)
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4

            # for rectangle
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 255), 2)

             # to print text of person on box
            cv2.putText(img, name, (x1 + 6, y1 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 255), 2)
            markAttendance(name)


    cv2.imshow('FDAS', img)

    key = cv2.waitKey(20)
    # exit on Enter key
    if (key == 13 or key == 27 or key == 81): 
        break