#! /usr/bin/env python3

import json
import os
import requests
import time
import sys
from datetime import datetime
import json

from time import localtime, strftime

with open('credentials.json', 'r') as f:
    creds = json.load(f)

temp_file_path = ".mastates.tmp"

def getStatusData():
    r = requests.get('https://erp.netzint.de/info/overview.json', auth=(creds["user"], creds["pw"]))
    return r.text.replace("\'", "\"")

def formatStatusData(data):
    return json.loads(data)

def checkFile():
    return os.path.exists(temp_file_path)

def readData():
    with open(temp_file_path) as f:
        data = f.read()
        return json.loads(data)

def saveData(data):
    f = open(temp_file_path, "w")
    f.write(json.dumps(data))
    f.close()

def sendNotification(text):
    #notifiy=osascript -e 'display notification "Lorem ipsum dolor sit amet" with title "Title"'
    #string = "/usr/bin/notify-send -t 15000 'Mitarbeiter Überwachungs Tool' '" + text + "'"
    #string = "osascript -e "display notification \"$text\" with title "Title""
    string = "osascript -e \'display notification \""+ text + "\" with title \"Mitarbeiter Überwachungs Tool\"\'"
    os.system(string.encode("utf-8"))

def compare(old_data, current_data):
    for data in old_data:
        if old_data[data]["xentral_status"] != current_data[data]["xentral_status"]:
            with open("/Users/andy/opt/anwenseinheitsChecker/history.log", "a") as f:
                f.write(strftime("%Y-%m-%d %H:%M:%S", localtime()) + " " + data + " has changed from " + old_data[data]["hr_status"] + " to " + current_data[data]["hr_status"] + "\n")
            name = data.split(".")[0].capitalize() + " " + data.split(".")[1].capitalize()
            timenow=datetime.now().strftime('%H:%M')
            if current_data[data]["hr_status"] == "anwesend":
                sendNotification(f"{name}  has joined the game! [{timenow}]")
            elif current_data[data]["hr_status"] == "abwesend":
                sendNotification(f"{name} has left the game! [{timenow}]")
            elif current_data[data]["hr_status"] == "inPause":
                sendNotification(f"{name} is making a break! [{timenow}]")
            else:
                sendNotification(data + " has changed from " + old_data[data]["hr_status"] + " to " + current_data[data]["hr_status"] + "[" + timenow +"]")


def main():
    if checkFile():
        old_data = readData()
        current_data = getStatusData()
        current_data = formatStatusData(current_data)

        compare(old_data, current_data)

        saveData(current_data)
    else:
        data = getStatusData()
        data = formatStatusData(data)
        saveData(data)

def printTable():
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        d= json.loads(getStatusData())
        print("{:<20} {:<15}".format('Mitarbeiter','Status'))
        for k, v in d.items():
            v['calling'] = ''
            firstname, lastname = k.split(".")
            k = firstname.title() + " " + lastname.title()
            if v['hr_status'] == "anwesend":
                print("\33[33;1m{:<20} \033[32m{:<2}{:<10}{:<2}".format(k, "✅", v['hr_status'], v['calling']))
            if v['hr_status'] == "abwesend":
                print("\33[33;1m{:<20} \033[31m{:<2}{:<10}{:<3}".format(k, "❌", v['hr_status'], v['calling']))
            if v['hr_status'] == "inPause":
                print("\33[33;1m{:<20} \033[34m{:<2}{:<10}{:<2}".format(k, "🤤 ", v['hr_status'], v['calling']))
        #print(maInCall)
        print(current_time)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "table":
            main()
            printTable()
        quit()
    while True:
        print ("entered continius mode")
        try:
          main()
          time.sleep(30)
        except KeyboardInterrupt:
            exit()
        except:
            pass
