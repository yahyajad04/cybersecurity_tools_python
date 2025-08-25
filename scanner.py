#!/usr/bin/env python
import requests , re , urllib.parse#urllib.parse for python 3
from bs4 import BeautifulSoup

class Scanner:

    def __init__(self,url,ignore_links):
        self.session = requests.Session()
        self.victim = url
        self.final_links = []
        self.ignore_list = ignore_links
    def extract_links(self,victim):
        res = self.session.get(victim)
        return re.findall('(?:href=")(.*?)"' , str(res.content))
    def crawl(self , url=None):
        if url == None :
            url = self.victim
        links = self.extract_links(url)
        for link in links:
            link = urllib.parse.urljoin(url , link)
            if "#" in link :
                link = link.split("#")[0]
            if self.victim in link and link not in self.final_links and link not in self.ignore_list:
                self.final_links.append(link)
                print(link)
                self.crawl(link)

    def extract_forms(self,url):
        response = self.session.get(url)
        parsed_resp = BeautifulSoup(response.content, features='lxml')
        return parsed_resp.findAll("form")

    def submit_form(self,form,value,url):
        action = form.get("action")
        full_url = urllib.parse.urljoin(url, action)
        method = form.get("method")
        inputs = form.findAll("input")
        post_data = {}
        for input in inputs:
            name = input.get("name")
            type = input.get("type")
            form_value = input.get("value")
            if type == "text":
                form_value = value
            post_data[name] = form_value
        if method == "post":
            return self.session.post(full_url, data=post_data)
        return self.session.post(full_url , params = post_data)

    def run(self):
        for link in self.final_links:
            forms = self.extract_forms(link)
            for form in forms:
                print("\n\n[+] Testing form for " + link)
                if self.test_xss_in_form(form , link):
                    print("\n\n[+] XSS Discovered for this link >> " + link + "in this form")
                    print(form)
            if "=" in link:
                print("\n\n[+] Testing " + link)
                if self.test_xss_in_link(link):
                    print("\n\n[+] XSS Discovered for this link >> " + link)


    def test_xss_in_link(self,url):
        xss_text = "<sCript>alert('test')</scriPt>"
        url = url.replace("=" , "=" + xss_text)
        response = self.session.get(url)
        return xss_text in response.content.decode()

    def test_xss_in_form(self,form,url):
        xss_text = "<sCript>alert('test')</scriPt>"
        response = self.submit_form(form , xss_text , url)
        return xss_text in response.content.decode()
