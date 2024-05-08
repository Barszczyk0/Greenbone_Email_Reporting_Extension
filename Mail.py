import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication


class Mail:

    def send_email(self, sender, recipients, password, msg):
        print("[ℹ] - Sending email")
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        smtp_server.quit()

    def create_msg(self, subject="Greenbone Raport", body="Raport", sender=None, recipients=None):
        print("[ℹ] - Creating email body")
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        msg.attach(MIMEText(body))
        return msg

    def add_attachment(self, attachment_path, file_name, msg):
        print("[ℹ] - Creating attachment")
        with open(attachment_path, "rb") as attachment:
            part = MIMEApplication(attachment.read(), Name=attachment_path)
        part['Content-Disposition'] = f'attachment; filename="{file_name}"'
        msg.attach(part)
        return msg


# subject = "Email Subject"
# body = "This is the body of the text message"
# attachment_path = "./Reports/" + "test.txt"
# file_name = "test.txt"
#
# sender = ""
# recipients = [""]
# password = ""
#
#
# ml = Mail()
# msg = ml.create_msg(sender=sender, recipients=recipients)
# msg = ml.add_attachment(attachment_path, file_name, msg)
# ml.send_email(sender, recipients, password, msg)
# print("[✔] - Email was sent")