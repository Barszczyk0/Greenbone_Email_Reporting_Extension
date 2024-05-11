import sys
import Mail
import Greenbone

if __name__ == "__main__":
    task_id = None
    recipient_email = []
    if len(sys.argv) == 2:
        task_id = sys.argv[1]
        recipient_email = [sys.argv[2]]
    else:
        print("No parameters passed.")

    gb = Greenbone.Greenbone()

    report_id = gb.start_task(task_id)
    gb.download_report(report_id)

    file_name = gb.get_report_filename()

    subject = "Greenbone Report"
    body = "Scan Report"
    attachment_path = "./Reports/" + file_name

    sender = ""
    password = ""

    ml = Mail.Mail()
    msg = ml.create_msg(sender=sender, recipients=recipient_email)
    msg = ml.add_attachment(attachment_path, file_name, msg)
    ml.send_email(sender, recipient_email, password, msg)
