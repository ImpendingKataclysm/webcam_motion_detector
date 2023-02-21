import os

password = os.getenv("MOTION_DETECTOR_PASS")
print(password)


def send_email():
    print("Email was sent")
