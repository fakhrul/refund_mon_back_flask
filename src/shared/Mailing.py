#  Reference https://realpython.com/python-send-email/
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from threading import Thread, Lock
import time
from collections import deque
import os


class Mailing:
    def __init__(self):
        super(Mailing, self).__init__()
        self.port = 465  # For starttls
        self.smtp_server = "mail.kaawal.com"
        self.sender_email = "dds@kaawal.com"
        self.receiver_email = "fakhrul@flybots.tech"
        self.password = "Fakhrul@12345"
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

                    context = ssl.create_default_context()

                    with smtplib.SMTP_SSL("mail.kaawal.com", self.port, context=context) as server:
                        server.login(self.sender_email , self.password)
                        # TODO: Send email here
                        server.sendmail(self.sender_email, receiver_email, message.as_string())
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

        self._elements.append(data)

    def dequeue(self):
        return self._elements.popleft()
        
if __name__ == "__main__":
    mail = Mailing()
    time.sleep(1)

    text = """\
    Hi {fname},\r\nasdasd
    How are you? {age}
    Real Python has many great tutorials:
    www.realpython.com""".format(fname = "John", age = 36)

    mail.send('fakhrulazran@gmail.com','test', text, html= text )
    time.sleep(1)
    mail.send('fakhrul@flybots.tech','test', text, html= text )
