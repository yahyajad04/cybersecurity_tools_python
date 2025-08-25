#!/usr/bin/env python
import scanner


url = "http://192.168.65.146/dvwa/"
dict = {"username": "admin", "password": "password" , "Login": "submit"}

scan = scanner.Scanner(url , "http://192.168.65.146/dvwa/logout.php")
scan.session.post("http://192.168.65.146/dvwa/login.php" , data = dict)

scan.crawl()
scan.run()