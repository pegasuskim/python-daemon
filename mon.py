#!/usr/bin/python
# -*- coding:utf-8 -*-

import os
import time
import smtplib

from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.MIMEText import MIMEText
from email import Encoders
from email import Utils
from email.header import Header

from PEProcess import PEProcess

# pid_list = psutil.get_pid_list()
# print pid_list

#PIDS_DIR_PATH = os.path.abspath(os.path.dirname(__file__)) + '/pid'
# 쉘 스트립트에서 지정한 pid 경로를 맞춰 줌
PIDS_DIR_PATH ="/var/run/data_handler.pid"

print PIDS_DIR_PATH
NOTIFY_RETRY_COUNT = 10
WAIT_TIME = 10

# processes
# global processes

# process state
activate = True

# retry count
retry = 0


smtp_server  = "smtp.gmail.com"
port         = 587

userid = "useremail"
passwd = "pass"

def send_mail(from_user, to_user, cc_users, subject, text, attach):
        COMMASPACE = ", "
        msg = MIMEMultipart("alternative")
        msg["From"] = from_user
        msg["To"]   = to_user
        msg["Cc"] = COMMASPACE.join(cc_users)
        msg["Subject"] = Header(s=subject, charset="utf-8")
        msg["Date"] = Utils.formatdate(localtime = 1)
        msg.attach(MIMEText(text, "html", _charset="utf-8"))

        if (attach != None):
                part = MIMEBase("application", "octet-stream")
                part.set_payload(open(attach, "rb").read())
                Encoders.encode_base64(part)
                part.add_header("Content-Disposition", "attachment; filename=\"%s\"" % os.path.basename(attach))
                msg.attach(part)

        smtp = smtplib.SMTP(smtp_server, port)
        smtp.starttls()
        smtp.login(userid, passwd)
        print "gmail login OK!"
        smtp.sendmail(from_user, cc_users, msg.as_string())
        print "mail Send OK!"
        smtp.close()


def read_file(file_name):
    fullpath = PIDS_DIR_PATH + '/' + file_name
    with open(fullpath) as pid_file:
        pid = pid_file.readline()
        pid = pid.rstrip()
        data = {'fullpath': fullpath, 'pid': pid, 'script_name': file_name}
        return data

def read_pids():
    global ps_data
    print PIDS_DIR_PATH
    pid_files = os.listdir(PIDS_DIR_PATH)
    ps_data = map(read_file, pid_files)
    print ps_data

def prepare():
    global processes
    processes = []

    for data in ps_data:
        process = PEProcess(data)
        processes.append(process)

read_pids()
prepare()

while True:
    for process in processes:
        print process
        if process.is_alive():
            print "alive"
        else:
            process.retry()
            send_mail('user@emailhost','user@emailhost',['user@emailhost','user@emailhost'],"[ERROR Report] Worker dead!!"," Worker dead!!",None)
            print "dead"
    time.sleep(WAIT_TIME)
