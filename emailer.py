import imghdr
import os
import smtplib
from email.message import EmailMessage

PASSWORD = os.getenv("MOTION_DETECTOR_PASS")
SENDER = "ktjanzen42@gmail.com"
RECEIVER = "ktjanzen42@gmail.com"


def send_email(img_path):
    email_message = EmailMessage()
    email_message["Subject"] = "Newcomer Detected"
    email_message.set_content("We have company")

    with open(img_path, "rb") as file:
        content = file.read()

    email_message.add_attachment(content,
                                 maintype="image",
                                 subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()


if __name__ == "__main__":
    send_email("image.png")
