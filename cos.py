import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import gvm
from gvm.protocols.latest import Gmp
from gvm.xml import pretty_print
from lxml import etree
import base64
import io
import time
from gvm.connections import UnixSocketConnection
from gvm.protocols.gmp import Gmp
from gvm.transforms import EtreeTransform
from gvm.xml import pretty_print

class Adada:

    def send_email(self, sender, recipients, password, msg):
        smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        smtp_server.login(sender, password)
        smtp_server.sendmail(sender, recipients, msg.as_string())
        smtp_server.quit()

connection = UnixSocketConnection()
transform = EtreeTransform()

with Gmp(connection, transform=transform) as gmp:
    # Retrieve GMP version supported by the remote daemon
    version = gmp.get_version()
    gmp.authenticate('login', 'haslo')

#create task
    task1 = gmp.create_task(name="Test", target_id= "127.0.0.1")

#find created task
    response = gmp.get_tasks(filter_string='Test')
    root = etree.fromstring(response)
    task_element = root.find('.//Test')
    task_id = task_element.get('id')

    #task_id_test = res.xpath('@id')[0]

#start created task
    task1_start = gmp.start_task(task_id)

task1 = gmp.create_task(name="Test", target_id= "127.0.0.1",config_id="daba56c8-73ec-11df-a475-002264764cea", scanner_id="08b69003-5fc2-4037-a479-93b440211c73")
task_id = task1['task_id']
task1_start = gmp.start_task(task_id)