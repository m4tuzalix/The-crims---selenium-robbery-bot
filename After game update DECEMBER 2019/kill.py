from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import time
import psutil
import os
import shutil
import random
import sys


class crims_hitman():
    
    def __init__(self, login, password, counter=0):
        self.login = login
        self.password = password
        self.browser = webdriver.Chrome("D:\crims selenium\chromedriver.exe")
        self.browser.get("https://www.thecrims.com/")
        self.action = ActionChains(self.browser)
        self.counter = 0
        self.killed = False #// support variable to set the correct delay once player has been killed (then turns to TRUE) - Used in exit_club()
        self.killers = {}
        
    
        
        self.log_in()
        self.get_killers()
        self.restore_stamina()
        self.kill_people()
        
                

              

    def log_in(self):
        log = self.browser.find_element_by_xpath('//input[@placeholder="Username"]')
        pas = self.browser.find_element_by_xpath('//input[@name="password"]')
        logged = None
        if log:
            try:
                log.send_keys(f'{self.login}')
            except:
                print("problem with login")
        if pas:
            try:
                pas.send_keys(f'{self.password}')
            except:
                print("problem with password")
        if log.get_attribute("value") == f'{self.login}' and pas.get_attribute("value") == f'{self.password}':
            try:
                click_but = self.browser.find_element_by_xpath('//button[@class="btn btn-large btn-inverse"]') 
                click_but.click()
            except:
                print('problem with loging in')

    def get_killers(self):
        url = requests.get("https://www.thecrims.com/stats/killers#/").text #/// scrap people(hitman) from top list
        soup = BeautifulSoup(url, "lxml")

        table = soup.find("table", class_="black_table")
        nicks = table.find_all("span", class_="nicktext")
        kills = table.find_all("td", valign="middle")
        for n,k in zip(nicks,kills):
            self.killers.update({n.text:k.text})
        print("done")
                           
    def restore_stamina(self):
        self.random_club = random.randint(1,5)
        try:
            self.browser.execute_script("""setTimeout(()=>{
                                 document.querySelector("div[id='menu-sprite-nightlife'").click();
                    },500);""") 
            try:
                clubs = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, f'//ul[@class="nightclubs unstyled"]//li[{str(self.random_club)}]//div[@class="well well-small"]//div[2]//button[@class="btn btn-inverse btn-small pull-right"]')))
                if clubs:
                    clubs.click()
                    self.kill_people()
            except:
                raise
        except ElementClickInterceptedException or StaleElementReferenceException or TimeoutException:
            self.restore_stamina()
            self.kill_people()


    def kill_people(self):
        people_to_avoid = ["Hitman","Padrino","Godfather"]
        
        self.current_stamina = self.browser.find_element_by_xpath('//div[@class="user_profile_progressbar progressbar"]//div[@id="stamina-progressbar"]').value_of_css_property("width")
        self.percent_stamina = round(100*float(self.current_stamina[:-2])/128)

        if self.percent_stamina < 50:
            self.restore()
        else:
            try:
                middle = WebDriverWait(self.browser, 8).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='content_middle']//div[@class='content_style main-content ']//div//div//ul[@class='unstyled inline user_list nightlife_user_list']//li")))
                    
                if middle:
                    for li in middle:
                        name = li.find_element_by_xpath("//li//div//div[@class='user_list_username']//span//a").text
                        respect = li.find_element_by_xpath("//li//div//div[@class='user_list_respect']").text
                        proffesion = li.find_element_by_xpath("//li//div//div[@class='user_list_level']").text
                        print(name," ",respect[9:]," ",proffesion)
                        if int(respect[9:]) > 100000:
                            
                            # for man in people_to_avoid: #/// array with people to avoid attacking
                            #     if man in proffesion:
                            #         self.exit_club()
                            for killer,kills in self.killers.items():
                                if name in killer and int(kills) > 100:
                                    self.exit_club()
                                    break
                            
                            choose_victim = WebDriverWait(self.browser, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='content_middle']//div[@class='content_style main-content ']//div//div//div//div[@class='pull-left middle-col-4']//div//div[@id='nightclub-singleassault-select-victim']//button")))
                            if choose_victim:
                                choose_victim.click()
                                get_victim = WebDriverWait(self.browser, 15).until(EC.visibility_of_element_located((By.XPATH, "//div[@id='content_middle']//div[@class='content_style main-content ']//div//div//div//div[@class='pull-left middle-col-4']//div//div[@id='nightclub-singleassault-select-victim']//ul[@class='dropdown-menu']//li//a[@role='button']")))
                                if get_victim:
                                    get_victim.click()
                                kill_him = WebDriverWait(self.browser, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='content_middle']//div[@class='content_style main-content ']//div//div//div//div[@class='pull-left middle-col-4']//div//div//button[@id='nightclub-singleassault-attack']")))
                                if kill_him:
                                    try:
                                        kill_him.click()
                                        print("killed: "+str(name))
                                        self.killed = True
                                        self.exit_club()

                                                
                                    except StaleElementReferenceException:
                                        self.exit_club()

                        else:
                            self.exit_club()
                                
                    
            except TimeoutException: #/// ff none comes to club then timeoutexception arises - it is treated as repetition of entering the club
                try:
                    self.exit_club()
                except:
                    WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
                    self.exit_club()
                    

    def if_restore_fail(self):
        kredyt = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='nav-collapse collapse']//ul[@class='nav pull-left']//li[3]//a")))
        if kredyt:
            kredyt.click()
    
        
    def restore(self):
        current_toxic = self.browser.find_element_by_xpath('//div[@class="user_profile_progressbar progressbar"]//div[@id="addiction-progressbar"]').value_of_css_property("width")
        percent_toxic = round(100*float(current_toxic[:-2])/128)
        self.current_stamina = self.browser.find_element_by_xpath('//div[@class="user_profile_progressbar progressbar"]//div[@id="stamina-progressbar"]').value_of_css_property("width")
        self.percent_stamina = round(100*float(self.current_stamina[:-2])/128)
        if self.percent_stamina < 50:
            try:
                inside_club = WebDriverWait(self.browser, 5).until(EC.presence_of_all_elements_located((By.XPATH,"//table[@class='table table-condensed table-top-spacing']//tbody//tr//td[2]")))
                try:
                    for i in inside_club:
                        i.find_element_by_xpath("./following::td/button[@class='btn btn-inverse btn-small']").click()
                        break
                    self.exit_club()
                except ElementClickInterceptedException or StaleElementReferenceException:
                    self.restore_stamina()
                
            except TimeoutException:
                self.restore_stamina()
        else:
            self.restore_stamina()
        
        
    def exit_club(self):
        delay = 0 #// delay after exiting the club just to let browser to load correctly (1.5 if haven't killed anyone)
        if self.killed:
            delay = 3 #// after killing player browser needs a bit more time to load so 5 seconds
        try:
            get_out = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[@id='page']//div[@id='content']//table[@id='content_table']//tbody//tr//td//div[@id='content_middle']//div[@class='content_style main-content ']//div[3]//div//button[@class='btn btn-inverse btn-large pull-right']")))
            get_out.click()
            time.sleep(delay)
            self.killed = False
            self.restore_stamina()
            self.kill_people()
        except:
            self.restore_stamina()
            self.kill_people()

if __name__ == "__main__":
    login = "login" #// put your login here
    password = "password" #// put your password here
    try:
        app = crims_hitman(login, password)
    except:
        pass
