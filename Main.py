# import base64
import os
# import smtplib
# import time
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.application import MIMEApplication

import gvm
from gvm.protocols.latest import Gmp
# from lxml import etree


class Greenbone:
    def __init__(self):
        self.connection = gvm.connections.UnixSocketConnection(path='/run/gvmd/gvmd.sock')
        self.gmp = gvm.protocols.latest.Gmp(connection=self.connection)
        self.gmp.authenticate(username='admin2', password='5e3df563-3abe-437f-97d3-1055fd9c6446')
        print(self.connection)
        print(self.gmp.get_version())
        task1 = self.gmp.create_task(name="Test", target_id= "127.0.0.1", config_id="daba56c8-73ec-11df-a475-002264764cea", scanner_id="08b69003-5fc2-4037-a479-93b440211c73")
        print(task1)
        # task_id = task1[1]

        # response = self.gmp.get_tasks(filter_string='Test')
        # root = etree.fromstring(response)
        # task_element = root.find('.//task')
        # task_id = task_element.get('id')
        # print("Task id: " + task_id)
        #
        # task1_start = self.gmp.start_task(task_id)
        # print("Task start:" + task1_start)



        # self.gmp.create_scanner()
        # self.gmp.create_config

if __name__ == "__main__":
    target_ip = os.getenv("TARGET_IP")
    mail_sender = os.getenv("MAIL_SENDER")
    mail_recipients = os.getenv("MAIL_RECIPIENTS")
    mail_password = os.getenv("MAIL_PASSWORD")
    schedule = os.getenv("SCAN_SCHEDULE")

    greenbone = Greenbone()