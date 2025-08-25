#!/usr/bin/env python
import requests , re , urlparse#urllib.parse for python 3

def extract_links(victim):
    res = requests.get(victim)
    return re.findall('(?:href=")(.*?)"' , res.content)


final_links = []
victim = "http://192.168.65.146/mutillidae/"

def crawl(url):
    links = extract_links(url)
    for link in links:
        link = urlparse.urljoin(url , link)
        if "#" in link :
            link = link.split("#")[0]
        if victim in link and link not in final_links:
            final_links.append(link)
            print(link)
            crawl(link)

crawl(victim)