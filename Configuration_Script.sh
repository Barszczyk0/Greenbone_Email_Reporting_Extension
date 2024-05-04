#!/usr/bin/bash

# Bash strcit mode
set -eou pipefail

welcome_menu() {
        RESPONSE=$(dialog \
                --title "Greenbone Email Reporting Configuration" \
                --no-collapse \
        --keep-tite \
                --msgbox "
           .--.
           |__| .-------.
           |=.| |.-----.|
           |--| || BSO ||
           |  | |'-----'|
           |__|~')_____('" \
                0 0 3>&1 1>&2 2>&3 3>&-)
        if [[ RESPONSE -ne 0 ]]; then
                exit
        fi
}

configuration_menu() {
        RESPONSE=$(dialog --title "Configuration"\
                --menu "Configuration options:" 0 0 0\
                1 "Target IP" 2 "Email address" 3 "Schedule automatic scans" 4 "Finish"\
                3>&1 1>&2 2>&3 3>&-)

        case $RESPONSE in
                1)
                        IP=$(dialog --nocancel --inputbox "Please provide IP:" 10 60 "$IP" 3>&1 1>&2 2>&3 3>&-);;
                2)
                        RECIPIENT_EMAIL=$(dialog --nocancel --inputbox "Please provide recipient EMAIL:" 10 60 "$RECIPIENT_EMAIL"  3>&1 1>&2 2>&3 3>&-);;
                3)
                        SCHEDULE=$(dialog --nocancel --form "Please enter the required information" 12 60 5\
                                "Minute (0 - 59):"  1 1 "$MINUTE" 1 30 15 0\
                                "Hour (0 - 23):"  2 1 "$HOUR" 2 30 15 0\
                                "Day of month (1 - 31)" 3 1 "$DAY_OF_MONTH" 3 30 15 0\
                                "Month (1 - 12)" 4 1 "$MONTH" 4 30 15 0\
                                "Day of week (0 - 6)" 5 1 "$DAY_OF_WEEK" 5 30 15 0\
                                3>&1 1>&2 2>&3 3>&-);;
                4)
                        FINISH=1;;
        esac
}


welcome_menu

# Default values
IP=""
RECIPIENT_EMAIL=""
FINISH=0
SCHEDULE=""
MINUTE="0"
HOUR="*"
DAY_OF_MONTH="*"
MONTH="*"
DAY_OF_WEEK="*"

while true; do
        configuration_menu

        # Schedule information
        MINUTE=$(echo "$SCHEDULE" | sed -n 1p)
        HOUR=$(echo "$SCHEDULE" | sed -n 2p)
        DAY_OF_MONTH=$(echo "$SCHEDULE" | sed -n 3p)
        MONTH=$(echo "$SCHEDULE" | sed -n 4p)
        DAY_OF_WEEK=$(echo "$SCHEDULE" | sed -n 5p)

        # Simple validation of provided IP, RECIPIENT_EMAIL and SCHEDULE information
        echo "$IP" | grep -qE '[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}' && \
        echo "$RECIPIENT_EMAIL" | grep -qE "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,10}\b" && \
        [[ $MINUTE = "*" || ( $MINUTE -ge 0 && $MINUTE -le 59 && $MINUTE =~ ^[0-9]+$ ) ]] && \
        [[ $HOUR = "*" || ( $HOUR -ge 0 && $HOUR -le 23 && $HOUR =~ ^[0-9]+$ ) ]] && \
        [[ $DAY_OF_MONTH = "*" || ( $DAY_OF_MONTH -ge 0 && $DAY_OF_MONTH -le 31 && $DAY_OF_MONTH =~ ^[0-9]+$ ) ]] && \
        [[ $MONTH = "*" || ( $MONTH -ge 1 && $MONTH -le 12 && $MONTH =~ ^[0-9]+$ ) ]] && \
        [[ $DAY_OF_WEEK = "*" || ( $DAY_OF_WEEK -ge 0 && $DAY_OF_WEEK -le 6 && $DAY_OF_WEEK =~ ^[0-9]+$ ) ]] && \
        [[ $FINISH -eq 1 ]] && break

        # Error information
        [[ $FINISH -eq 1 ]] && dialog --title "Configuration error" --msgbox "Check all configuration settings" 5 60

        FINISH=0
done


# echo "$MINUTE $HOUR   $DAY_OF_MONTH $MONTH $DAY_OF_WEEK       root    /home/kali/Email_Reporting/test.sh" >> /etc/crontab
