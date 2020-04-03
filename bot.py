#!/usr/bin/env python3

from selenium import webdriver
from lcoConfig import fr_code,fr_password,plan_amount
from time import sleep
import re
import csv

class LcoBot():
    def __init__(self, date):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.isLogin = False
        self.date = date
        self.nos = 0
    
    # Login into portal
    def login(self):
        # print("LOGGING IN")
        self.driver.get("https://lcoportal.incablenet.net")
        fr_input = self.driver.find_element_by_xpath('//*[@id="login"]/div[1]/input')
        fr_input.send_keys(fr_code)
        fr_pass = self.driver.find_element_by_xpath('//*[@id="login"]/div[2]/input')
        fr_pass.send_keys(fr_password)
        submit_btn = self.driver.find_element_by_xpath('//*[@id="login"]/button')
        submit_btn.click()
        self.isLogin = True

    # Logout of portal
    def logout(self):
        # print("LOGGING OUT")
        sleep(2)
        self.driver.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul[2]/li[12]/a').click()
        self.isLogin = False

    def subscriberPage(self):
        if(self.nos==15):
            self.logout()
            self.nos = 0
        if not self.isLogin:
            self.login()
        # print("Going to Subscriber Page")
        self.nos = self.nos+1
        try:
            self.driver.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul[2]/li[8]/a').click()
            self.driver.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul[2]/li[8]/ul/li[2]/a').click()
        except:
            print("ERROR loading subscriber! Retrying...")
            sleep(5)
            self.subscriberPage()

    def checkBox(self, account):
        self.subscriberPage()
        # print("CHECKING ACCOUNT")
        account_input = self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/div[2]/div/div/input')
        account_input.clear()
        account_input.send_keys(account)
        submit_btn = self.driver.find_element_by_xpath('//*[@id="subscriberid"]')
        submit_btn.click()
        sleep(5)
        try:
            error = self.driver.find_element_by_xpath("/html/body/div[4]/h4").text
            if len(error)>0:
                return ""
            size = len(self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div/div[2]/div/table').find_elements_by_tag_name("tr"))-1
            pattern = r'Rs.(\d+.\d+)'
            periodPattern = r'..\/(.+) to .+'
            for i in range(size):
                entry = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div/div[2]/div/table/tbody/tr[{}]/td[3]'.format(i+1)).text
                amount = re.search(pattern, entry)[1]
                if(amount in plan_amount):
                    temp = self.driver.find_element_by_xpath('/html/body/div[4]/div[2]/div[2]/div[1]/div/div[2]/div/table/tbody/tr[{}]/td[4]'.format(i+1))
                    temp = temp.find_elements_by_xpath('.//*')
                    details = temp[0]
                    details.click()
                    sleep(1)
                    period = self.driver.find_element_by_xpath('//*[@id="detailsmodal"]/div/div/div[3]/table/tbody/tr/td[4]').text
                    self.driver.find_element_by_xpath('//*[@id="detailsmodal"]/div/div/div[1]/button').click()
                    month = re.search(periodPattern, period)[1]
                    if(month==self.date):
                        # print('FOUND', period.upper(), amount)
                        sleep(1)
                        return period.strip().upper()
        except:
            # print("ERROR OCCURED! Retrying...")
            sleep(5)
            self.checkBox(account)
        
        return ""
