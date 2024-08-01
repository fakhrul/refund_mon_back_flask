#  Reference https://realpython.com/python-send-email/
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread, Lock
import time
from collections import deque
import logging
import os


class GMailing:
    def __init__(self):
        super(GMailing, self).__init__()
        self.sender_email = "ddskaawal@gmail.com"
        self.password = "zzdxckqgcoixzinz"
        self._elements = deque()

        t = Thread(target=self.process_email_queue)
        t.daemon = True
        t.start()

    def process_email_queue(self):
         while True:
            try:
                if len(self._elements) > 0:
                    email_info = self.dequeue()
                    text =  email_info["text"]
                    html = email_info["html"]
                    receiver_email = email_info["receipients"]

                    message = MIMEMultipart("alternative")
                    message["Subject"] = email_info["subject"]
                    message["From"] = self.sender_email
                    message["To"] =   ", ".join(email_info["receipients"]) 
                    part1 = MIMEText(text, "plain")
                    part2 = MIMEText( html, "html")
                    message.attach(part1)
                    message.attach(part2)

                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()  # Use TLS encryption
                    server.login(self.sender_email, self.password)
                    server.sendmail(self.sender_email, receiver_email, message.as_string())

                    print(self.sender_email, receiver_email, "DONE")
                    server.quit()
            except Exception as e:
                print(e)
            time.sleep(0.1)



    def send(self, receipients, subject, text, html):
        data = {
            "receipients" : receipients,
            "subject": subject,
            "text" : text,
            "html" : html
        }

        print(f'Insert email in queue for receipients of {receipients} with {subject}')

        self._elements.append(data)

    def dequeue(self):
        return self._elements.popleft()
    

if __name__ == "__main__":
    mail = GMailing()
    time.sleep(1)

    text = """no url"""

    mail.send(['fakhrul@flybots.tech','fakhrulazran@gmail.com'],'Test Email', text, html= text )
    time.sleep(5)
