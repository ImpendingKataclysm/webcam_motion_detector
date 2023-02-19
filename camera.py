import streamlit as st
from datetime import datetime
import cv2

st.title("Motion Detector")
start = st.button("Start Camera", key="start")

if start:
    recording = True
    st_image = st.image([])
    camera = cv2.VideoCapture(0)
    stop = st.button("Stop Camera")

    while recording:
        check, timer_frame = camera.read()
        timer_frame = cv2.cvtColor(timer_frame, cv2.COLOR_BGR2RGB)
        now = datetime.now()

        cv2.putText(img=timer_frame, text=now.strftime("%a %d/%m/%y"), org=(30, 80),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 255, 255),
                    thickness=2, lineType=cv2.LINE_AA)
        cv2.putText(img=timer_frame, text=now.strftime("%H:%M:%S"), org=(30, 140),
                    fontFace=cv2.FONT_HERSHEY_PLAIN, fontScale=2, color=(255, 255, 255),
                    thickness=2, lineType=cv2.LINE_AA)
        st_image.image(timer_frame)
