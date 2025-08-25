#!/usr/bin/env python

import scapy.all as scapy
import argparse

def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broad = broadcast / arp_request
    answered , unanswered = scapy.srp(arp_broad , timeout = 1)
    client_list = []
    for i in answered :
        client_dict = {"IP": i[1].psrc , "mac": i[1].hwsrc}
        client_list.append(client_dict)
    return client_list


def print_scan(client_list):
    print("     IP\t\t\t\tMAC\n ----------------------------------------------")
    for i in client_list:
        print(" " + i["IP"] + "\t\t" + i["mac"])

def get_range():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t" , "--target" , dest="target" , help="get ip target range")
    options = parser.parse_args()
    return options


options = get_range()
scan_result = scan(options.target)
print_scan(scan_result)