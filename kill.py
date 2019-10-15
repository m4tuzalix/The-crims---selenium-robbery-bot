from selenium import webdriver
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
        self.browser = webdriver.Chrome("C:\projects\selenium\The-crims---selenium-robbery-hitman\chromedriver.exe")
        self.browser.get("https://www.thecrims.com/")
        self.action = ActionChains(self.browser)
        self.counter = 0
        
    
        
        self.log_in()
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
                           
    def restore_stamina(self):
        self.counter = self.counter + 1
        if self.counter == 1180:
            self.browser.quit()
            sys.exit()
        self.random_club = random.randint(1,5)
        try:
            club = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="menu-nightlife"]')))
            if club:
                try:
                    club.click()
                except ElementClickInterceptedException:
                    WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
                    club.click()
        
            clubs = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH, f'//ul[@class="nightclubs unstyled"]/li[{str(self.random_club)}]/table[@class="table table-condensed"]//button[@class="btn btn-inverse btn-small pull-right"]'))).click()
            if clubs:
                try:
                    clubs.click()
                except TimeoutException or StaleElementReferenceException or ElementClickInterceptedException:
                    kredyt = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='nav-collapse collapse']//ul[@class='nav pull-left']//li[3]//a")))
                    if kredyt:
                        kredyt.click()
                        self.restore_stamina()
        except StaleElementReferenceException or ElementClickInterceptedException:
            self.restore_stamina()


    def kill_people(self):
        people_to_avoid = ["Hitman","Padrino","Godfather", "Mobster", "Desperado", "Kingpin"]
        
        self.current_stamina = self.browser.find_element_by_xpath('//div[@class="user_profile_progressbar progressbar"]//div[@id="stamina-progressbar"]').value_of_css_property("width")
        self.percent_stamina = round(100*float(self.current_stamina[:-2])/128)

        if self.percent_stamina < 50:
            self.restore()
        
        try:
            middle = WebDriverWait(self.browser, 8).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='content_middle']//div[@class='content_style main-content ']//div//div//ul[@class='unstyled inline user_list nightlife_user_list']//li")))
                
            if middle:
                for li in middle:
                    name = li.find_element_by_xpath("//li//div//div[@class='user_list_username']//span//a").text
                    respect = li.find_element_by_xpath("//li//div//div[@class='user_list_respect']").text
                    proffesion = li.find_element_by_xpath("//li//div//div[@class='user_list_level']").text
                    print(name," ",respect[9:]," ",proffesion)
                    if int(respect[9:]) in range(100000,99000000) and not "ykarus" in name:
                        
                        for man in people_to_avoid: #/// array with people to avoid attacking
                            if man in proffesion:
                                self.exit_club()
                        
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
                                    self.if_restore_fail()
                                    self.restore_stamina()
                                    self.kill_people()
                                            
                                except StaleElementReferenceException:
                                    self.if_restore_fail()
                                    self.restore_stamina()
                                    self.kill_people()

                    else:
                        self.exit_club()
                            
                
        except TimeoutException: #/// ff none comes to club then timeoutexception arises - it is treated as repetition of entering the club
            try:
                self.restore_stamina()
                self.kill_people()
            except:
                WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
                self.restore_stamina()
                self.kill_people()
                    
            
    def exit_club(self):
        get_out = WebDriverWait(self.browser, 15).until(EC.element_to_be_clickable((By.XPATH, "//div[@id='content_middle']//div[@class='content_style main-content ']//div//div//button[@class='btn btn-inverse btn-large pull-right']")))
        if get_out:
            get_out.click()
            self.restore_stamina()
            self.kill_people()

    def if_restore_fail(self):
        kredyt = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='nav-collapse collapse']//ul[@class='nav pull-left']//li[3]//a")))
        if kredyt:
            kredyt.click()
    
        
    def restore(self):
        try:
            stamina_number = []
            
            inside_club = WebDriverWait(self.browser, 20).until(EC.presence_of_all_elements_located((By.XPATH,"//table[@class='table table-condensed table-top-spacing']//tbody//tr//td[2]")))
            
            stamina_number.extend([float(elem.text[:-1]) for elem in inside_club]) #// saves each element text as float so it can be compared in next step

            for i in inside_club:
                try:
                    if float(i.text[:-1]) == max(stamina_number):
                        needed_to_100 = 100/max(stamina_number)
                        needed_now = self.percent_stamina/max(stamina_number)
                        final_score = (needed_to_100 - needed_now)
                        i.find_element_by_xpath("./following::td/input[@name='quantity']").click()
                        i.find_element_by_xpath("./following::td/input[@name='quantity']").send_keys(f'{round(final_score)}')
                        i.find_element_by_xpath("./following::td/button[@class='btn btn-inverse btn-small']").click()
        
                        self.exit_club()
                            
                except:
                    raise
        except:
            raise
        

if __name__ == "__main__":
    login = "login" #// put your login here
    password = "password" #// put your password here
    try:
        app = crims_hitman(login, password)
    except:
        try:
            for p in psutil.process_iter():
                if "chrome" in p.name():
                    p.kill()
            app = crims_hitman(login, password)
        except psutil.NoSuchProcess:
            app = crims_hitman(login, password)



