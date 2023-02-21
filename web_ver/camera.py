import glob

import streamlit as st
import cv2
from datetime import datetime
from emailer import send_email

st.title("Motion Detector")
start = st.button("Start Camera", key="start")

if start:
    recording = True
    st_image = st.image([])
    camera = cv2.VideoCapture(0)
    stop = st.button("Stop Camera", key="stop")

    first_frame = None
    status_list = []
    count = 1

    while recording:
        status = 0

        check, timer_frame = camera.read()
        timer_frame = cv2.cvtColor(timer_frame, cv2.COLOR_BGR2RGB)
        now = datetime.now()

        cv2.putText(img=timer_frame, text=now.strftime("%a %d/%m/%y"),
                    org=(30, 80), fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=2, color=(255, 255, 255), thickness=2,
                    lineType=cv2.LINE_AA)
        cv2.putText(img=timer_frame, text=now.strftime("%H:%M:%S"),
                    org=(30, 140), fontFace=cv2.FONT_HERSHEY_PLAIN,
                    fontScale=2, color=(255, 255, 255), thickness=2,
                    lineType=cv2.LINE_AA)

        # Gray/blurred frames for motion detection
        gray_frame = cv2.cvtColor(timer_frame, cv2.COLOR_RGB2GRAY)
        gray_frame_gau = cv2.GaussianBlur(gray_frame, (21, 21), 0)

        # Get first frame of recording for comparison
        if first_frame is None:
            first_frame = gray_frame_gau

        # Compare/contrast current frame with first frame to identify moving objects
        delta_frame = cv2.absdiff(first_frame, gray_frame_gau)
        thresh_frame = cv2.threshold(delta_frame, 30, 255, cv2.THRESH_BINARY)[1]
        dil_frame = cv2.dilate(thresh_frame, None, iterations=2)

        # Draw rectangles around large moving objects in display frame
        contours, check2 = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            if cv2.contourArea(contour) < 10000:
                continue

            x, y, w, h = cv2.boundingRect(contour)
            rectangle = cv2.rectangle(timer_frame, (x, y), (x+w, y+h), (0, 200, 100), 3)

            # Check if there are moving objects
            if rectangle.any():
                status = 1

                cv2.imwrite(f"images/{count}.png", timer_frame)
                all_images = glob.glob("images/*.png")
                img_index = int(len(all_images) / 2)
                img_with_obj = all_images[img_index]
                count += 1

        # Compare current frame with previous one
        status_list.append(status)
        status_list = status_list[-2:]

        # Send email if the previous frame had an object and the current one does not
        if status_list[0] == 1 and status_list[1] == 0:
            send_email()

        st_image.image(timer_frame)
