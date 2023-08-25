import cv2
import numpy as np
from time import sleep

from deepface import DeepFace
from PIL import ImageFont, ImageDraw, Image

def CapturePicture():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
         result = {"status": "failed", "message": "打開鏡頭失敗"}
         return result

    for i in range(30):
        ret, frame = cap.read()
        sleep(0.1)

    ret, frame = cap.read()

    if ret:
        # cv2.imshow('Capture', frame)
        cv2.imwrite('app/facepicture/instant.jpg', frame)
        result = {"status": "success", "message": "圖片已捕捉"}
    else:
        result = {"status": "failed", "message": "圖片捕捉失敗"}

    cap.release()
    cv2.destroyAllWindows()
    return result

# CapturePicture()

def ProcessPicture():
    text_obj={
        'angry': '生氣',
        'disgust': '噁心',
        'fear': '害怕',
        'happy': '開心',
        'sad': '難過',
        'surprise': '驚訝',
        'neutral': '正常'
    }
    def putText(x, y, text, size=70, color=(255, 255, 255)):
        global img
        fontpath='NotoSansTC-Regular.otf'
        font = ImageFont.truetype(fontpath, size) #字形、大小
        imgPil = Image.fromarray(img)   #轉成PIL影像文件
        draw = ImageDraw.Draw(imgPil)   #開繪圖板(定義繪圖物件)
        draw.text((x, y), text, fill=color, font=font)  #加入文字
        img = np.array(imgPil)

    img = cv2.imread('app/facepicture/instant.jpg')
    gray =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #轉灰階

    face_cascade = cv2.CascadeClassifier("app\haarcascade_frontalface_default.xml") #載入人臉模型
    faces = face_cascade.detectMultiScale(gray) #偵測人臉

    try:
        emotion = DeepFace.analyze(img, actions=['emotion'])
        age = DeepFace.analyze(img, actions=['age'])
        race = DeepFace.analyze(img, actions=['race'])
        gender = DeepFace.analyze(img, actions=['gender'])

        print(emotion[0]['dominant_emotion'])
        print(age[0]['age'])
        print(race[0]['dominant_race'])
        print(gender[0]['gender'])  #return dict
    except Exception as e:
            print('error in try:', e) 

    for (x, y, w, h) in faces:
        x1 = x-60
        x2 = x+w+60
        y1 = y-20
        y2 = y+h+60
        face = img[x1:x2, y1:y2]
        try:
            emotion = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)   #辨識情緒
            putText(x, y, text_obj[emotion[0]['dominant_emotion']]) #放入文字
        except Exception as e:
            print('error in try:', e)
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 5)  #抓取每個人臉屬性，繪製方框

    cv2.imshow('oxxostudio', img)
    # cv2.resizeWindow('oxxostudio', 500, 500)
    cv2.waitKey(0)
    cv2.imwrite('app/facepicture/instant_ok.jpg', img)
    cv2.destroyAllWindows()

# CapturePicture()
# ProcessPicture()