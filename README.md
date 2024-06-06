# Greenbone Email Reporting Extension
This project allows to send emails with Greenbone scan reports. Please visit [demo](/Screenshots_demo/DEMO.md) to check how the application looks like.
## Setup
1. Install Greenbone in Kali Linux according to [Greenbone documentation](https://greenbone.github.io/docs/latest/index.html).
2. Perform `git clone ...` in home directory.
3. Ensure Greenbone is active by running `sudo gvm-start`.
4. Modify Greenbone credentials in Setup_Script.sh.
5. Provide credentials for email that would be used to send report in Scan_Starter.py
6. Run the Setup_Script.sh


# Information about project components
## Setup_Script.sh
Setup_Script.sh provides simple TUI (text user interface) to configure: Target IP or Subnet, recipient's email and scheduling information. Program performs basic validation of provided values. If validation failes, scan won't be configured. After that the program creates target and task via `gvm-cli` - the returned Task ID (along with recipient's email address) is used to setup cronjob in `/etc/crontab/`.

## Scan_Starter.py
Scan_Starter.py makes use of Greenbone.py and Mail.py in order to: start configured scan with provided Task ID, retrieve report, create email and send the email with the report to the recipient.

## Dialogrc
File .dialogrc provides custom theme for the configuration menu from Setup_Script.sh.
