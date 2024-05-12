from datetime import datetime
import gvm
import os
from gvm.protocols.latest import Gmp
from lxml import etree
import base64
import time
import Mail


class Greenbone:

    def __init__(self):
        try:
            time = str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
            print(f"[ℹ] - Connecting to Greenbone {time}")
            self.connection = gvm.connections.UnixSocketConnection(path='/run/gvmd/gvmd.sock')
        except Exception:
            print("[✘] - Connection to Greenbone failed")

        self.username = "admin"
        self.password = "admin"

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def get_report_filename(self):
        return self.report_filename

    def create_target(self, ipaddress):
        with Gmp(connection=self.connection) as gmp:
            gmp.authenticate(username=self.username, password=self.password)
            print(f"[ℹ] - Creating target {ipaddress}")
            # create a unique name by adding the current datetime
            name = f"Suspect Host {ipaddress} {str(datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))}"

            response = gmp.create_target(
                name=name, hosts=[ipaddress], port_list_id="33d0cd82-57c6-11e1-8ed1-406186ea4fc5"
            )
        root = etree.fromstring(response)
        target_id = root.attrib['id']
        print(f"[✔] - Target created - {name} - {target_id}")
        return target_id

    def create_task(self, ipaddress, target_id):
        print(f"[ℹ] - Creating task - Openvas scannner - Full and Fast")
        scan_config_id = "daba56c8-73ec-11df-a475-002264764cea" # Full and Fast
        scanner_id = "08b69003-5fc2-4037-a479-93b440211c73" # Openvas scanner
        with Gmp(connection=self.connection) as gmp:
            gmp.authenticate(username=self.username, password=self.password)
            name = f"Scan Suspect Host {ipaddress}"
            response = gmp.create_task(
                name=name,
                config_id=scan_config_id,
                target_id=target_id,
                scanner_id=scanner_id,
            )
        root = etree.fromstring(response)
        task_id = root.attrib['id']
        print(f"[✔] - Task created - {name} - {task_id}")
        return task_id

    def start_task(self, task_id):
        print(f"[ℹ] - Starting task - {task_id}")
        with Gmp(connection=self.connection) as gmp:
            gmp.authenticate(username=self.username, password=self.password)
            response = gmp.start_task(task_id)
        root = etree.fromstring(response)
        report_id = root.find('report_id').text
        print(f"[✔] - Task started - {task_id}")
        print(f"[ℹ] - Report ID - {report_id}")
        return report_id

    def download_report(self, report_id):
        with Gmp(connection=self.connection) as gmp:
            gmp.authenticate(username=self.username, password=self.password)
            # Check if scan is done
            scan_report = None
            try:
                while (True):
                    scan_report = gmp.get_report(report_id)
                    first_index = scan_report.index('<scan_run_status>')
                    last_index = scan_report.index('</scan_run_status>')
                    status = scan_report[first_index + len('<scan_run_status>'): last_index]
                    print("[ℹ] - Task status: " + status)

                    if status == "Done":
                        print("[✔] - Scan was completed")
                        break
                    else:
                        time.sleep(30)
                    # Get xml of pdf report
                    # c402cc3e-b531-11e1-9163-406186ea4fc5 is for pdf
                scan_report = gmp.get_report(report_id, report_format_id='c402cc3e-b531-11e1-9163-406186ea4fc5')
            except Exception:
                print("[✘] - Scan failed")

        # Save scan report to pdf file
        start_index = scan_report.index('</report_format>')
        last_index = scan_report.index('</report>')
        encoded_report_pdf = scan_report[start_index + len('</report_format>'): last_index]
        decoded_bytes = base64.b64decode(encoded_report_pdf)

        try:
            print("[ℹ] - Saving report")
            os.makedirs("./Reports", exist_ok=True)
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            self.report_filename = "report_" + current_time + ".pdf"
            with open("./Reports/" + self.report_filename, 'wb') as f:
                f.write(decoded_bytes)
            print("[✔] - Report was saved")
        except:
            print("[✘] - Error saving a report")

    def get_task_id(self, task_name):
        with Gmp(connection=self.connection) as gmp:
            gmp.authenticate(username=self.username, password=self.password)
            # Get task_id by task_name
            response = gmp.get_tasks(filter_string=task_name)
            root = etree.fromstring(response)
            task_element = root.find('.//task')
            task_id = task_element.get('id')
            return task_id
