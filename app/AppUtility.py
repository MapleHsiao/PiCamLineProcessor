import cv2
import numpy as np
from time import sleep

from deepface import DeepFace
from PIL import ImageFont, ImageDraw, Image

import requests
import json

# image process
def CapturePicture():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
         result = {"status": "failed", "message": "打開鏡頭失敗"}
         return result

    for i in range(15):
        ret, frame = cap.read()
        sleep(0.1)

    ret, frame = cap.read()

    if ret:
        # cv2.imshow('Capture', frame)
        cv2.imwrite('static/img/instant.jpg', frame)
        result = {"status": "success", "message": "圖片已捕捉"}
    else:
        result = {"status": "failed", "message": "圖片捕捉失敗"}

    cap.release()
    cv2.destroyAllWindows()
    return result

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

    def putText(img, x, y, text, size=70, color=(255, 255, 255)):
        fontpath='app/NotoSansTC-Regular.otf'
        font = ImageFont.truetype(fontpath, size)  # 字形、大小
        imgPil = Image.fromarray(img)  # 转成PIL影像文件
        draw = ImageDraw.Draw(imgPil)  # 开绘图板(定义绘图物件)
        draw.text((x, y), text, fill=color, font=font)  # 加入文字
        return np.array(imgPil)  # 将PIL图像转回NumPy数组，并返回

    img = cv2.imread('static/img/instant.jpg')
    gray =cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #轉灰階

    face_cascade = cv2.CascadeClassifier("app/haarcascade_frontalface_default.xml") #載入人臉模型
    faces = face_cascade.detectMultiScale(gray) #偵測人臉

    try:
        emotion = DeepFace.analyze(img, actions=['emotion'])
        age = DeepFace.analyze(img, actions=['age'])
        race = DeepFace.analyze(img, actions=['race'])
        gender = DeepFace.analyze(img, actions=['gender'])

        gender_info = gender[0]['gender']
        gender_str = f"Woman: {gender_info['Woman']:.2f}%, Man: {gender_info['Man']:.2f}%"

        analysis_results = {
            'status': 'success',
            'emotion' : emotion[0]['dominant_emotion'],
            'age' : age[0]['age'],
            'race' : race[0]['dominant_race'],
            'gender' : gender_str
        }   #return dict
        # print(emotion[0]['dominant_emotion'])
        # print(age[0]['age'])
        # print(race[0]['dominant_race'])
        # print(gender[0]['gender'])  
    except Exception as e:
            print('error in try:', e)
            analysis_results = {
                'status': 'error',
                'message': str(e)
            }
            return analysis_results

    for (x, y, w, h) in faces:
        x1 = x-60
        x2 = x+w+60
        y1 = y-20
        y2 = y+h+60
        face = img[y1:y2, x1:x2]
        try:
            emotion = DeepFace.analyze(face, actions=['emotion'], enforce_detection=False)   #辨識情緒
            img = putText(img, x, y, text_obj[emotion[0]['dominant_emotion']]) #放入文字
        except Exception as e:
            analysis_results = {
                'status': 'error',
                'message': str(e)
            }
            return analysis_results
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 5)  #抓取每個人臉屬性，繪製方框

    # cv2.imshow('oxxostudio', img)
    # cv2.resizeWindow('oxxostudio', 500, 500)
    # cv2.waitKey(0)
    cv2.imwrite('static/img/instant_ok.jpg', img)
    cv2.destroyAllWindows()

    return analysis_results

# servive
def toline(msg):
    url='https://api.line.me/v2/bot/message/push'
    headers={'Content-Type':'Application/Json','Authorization':'Bearer sw1J+KUm02qpsRCP1U09fR69AKDBh0+ejPDqvoj+RSLqJ/5Iy3mSUMUYZHfARGRebzpp0Nz38TQZ2HKSU/O6GLXwOAY+OFVJAZaPBw3oBRrgb3GkHVXEBlCepcfhqKvy1Sl3umtC30NcFOOhIsLgwgdB04t89/1O/w1cDnyilFU='}
    jsonData={
    "to": "Uee02b850afc71558e49411c7730fa108",
    "messages":[
        {
            "type":"text",
            "text":msg
        }
    ]
}
    response = requests.post(url,headers=headers,data=json.dumps(jsonData))
    return response

def format_analysis_results(analysis_results):
    formatted_results = f"""年齡: {analysis_results.get('age', 'N/A')}
情緒: {analysis_results.get('emotion', 'N/A')}
性別: {analysis_results.get('gender', 'N/A')}
種族: {analysis_results.get('race', 'N/A')}
狀態: {analysis_results.get('status', 'N/A')}"""
    
    return formatted_results