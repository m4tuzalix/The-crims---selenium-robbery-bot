from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementClickInterceptedException, ElementNotInteractableException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
import time
import psutil
import os
import shutil
import random


class crims_robber():
    
    def __init__(self, login, password, counter=0):
        self.login = login
        self.password = password
        self.browser = webdriver.Chrome("D:\crims selenium\chromedriver.exe")
        self.browser.get("https://www.thecrims.com/")
        self.action = ActionChains(self.browser)
        self.rob_power = 10
        self.number = 6
        self.counter = None
        
        
        self.log_in()
        self.assassult()
        
        

    def tescik(self):
        self.browser.execute_script("""setTimeout(()=>{
                                 document.querySelector("div[id='menu-sprite-robbery'").click();
                         },1000);""")  

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
    

    def assassult(self):

        current_toxic = self.browser.find_element_by_xpath('//div[@class="user_profile_progressbar progressbar"]//div[@id="addiction-progressbar"]').value_of_css_property("width")
        percent_toxic = round(100*float(current_toxic[:-2])/128)
        try:
            if percent_toxic > 10:
                self.toxic()
            else:
                try:
                    but = WebDriverWait(self.browser, 5).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="menu-sprite-robbery"]')))
                    if but:
                        but.click()
                        
                        select = WebDriverWait(self.browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='content_middle']//div//div[4]//table//tr//td//select[@id='singlerobbery-select-robbery']//option")))
                    
                        if select: #/// all options available under dropdown
                            last = None
                            for option in select: #// gets last iterator
                                if "100" in option.text:
                                    last = option.text
                            stamina_cost = last.index("-")
                            final_stamina_cost = last[int(stamina_cost+2):int(stamina_cost+4)] #/// gets the required cost

                            drop_menu = WebDriverWait(self.browser, 20).until(EC.presence_of_element_located((By.XPATH, "//div[@id='content_middle']//div//div[4]//table//tr//td//select[@id='singlerobbery-select-robbery']")))
                            DropDown = Select(drop_menu)  #/// navigates to drop down menu
                            if DropDown:
                                self.current_stamina = self.browser.find_element_by_xpath('//div[@class="user_profile_progressbar progressbar"]//div[@id="stamina-progressbar"]').value_of_css_property("width")
                                self.percent_stamina = round(100*float(self.current_stamina[:-2])/128)
                                DropDown.select_by_visible_text(last) #//// picks the last element with 100% of chance to rob
                                if self.percent_stamina > int(final_stamina_cost)-1:
                                    try:
                                        stamina_cost = last.index("-") #// gets the index to estimate number position
                                        final_stamina_cost = last[int(stamina_cost+2):int(stamina_cost+4)] #/// gets the required cost
                                        for x in range(round(self.percent_stamina/int(final_stamina_cost))): #// estimates possible tries
                                            WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, "//tr//table//tr//button[@id='singlerobbery-rob']"))).click()
                                        self.assassult()        
                                    except StaleElementReferenceException or ElementClickInterceptedException:
                                        WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
                                        self.assassult()
                                else:
                                    self.restore_stamina()
                                    self.assassult()
                                
                                

                except ElementClickInterceptedException or StaleElementReferenceException:
                    WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
                    self.assassult()
        except:
            raise

        #//// checks toxiacation and proceeds
    def toxic(self):
           
        try:
            self.browser.execute_script("""setTimeout(()=>{
                            document.querySelector("div[id='menu-sprite-hospital'").click();
                            },2000);""")
            heal = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH,"//table[@class='table-top-spacing']//tr//td[2]//button")))
            if heal:
                heal.click()
                time.sleep(2)
                self.assassult()
               
        except ElementClickInterceptedException or StaleElementReferenceException:
            self.assassult()
    
                        
    def restore_stamina(self):
        self.random_club = random.randint(1,5)
        try:
            self.browser.execute_script("""setTimeout(()=>{
                                 document.querySelector("div[id='menu-sprite-nightlife'").click();
                         },500);""") 
                
            clubs = WebDriverWait(self.browser, 20).until(EC.presence_of_all_elements_located((By.XPATH, f'//ul[@class="nightclubs unstyled"]//li[{self.random_club}]//div[@class="well well-small"]')))
            if clubs:
                for club in clubs:
                    club_name = club.find_element_by_xpath("./following::div[@class='nicktext pull-left']")
                    if "party" in str(club_name.text):
                        club_name.find_element_by_xpath("./following::div/button[@class='btn btn-inverse btn-small pull-right']").click()
                        try:
                            flash = WebDriverWait(self.browser, 0.5).until(EC.presence_of_element_located((By.XPATH, "//div[@id='content_middle']//div[@class='content_style main content ']//div[@class='flashpool'//div[@class'error flash__message']]")))
                            self.restore_stamina()
                            break
                        except:
                            self.restore()
                            break
                    else:
                        continue
                            
    

        except ElementClickInterceptedException or StaleElementReferenceException:
            self.restore_stamina()
                
    
    def restore(self):
        current_toxic = self.browser.find_element_by_xpath('//div[@class="user_profile_progressbar progressbar"]//div[@id="addiction-progressbar"]').value_of_css_property("width")
        percent_toxic = round(100*float(current_toxic[:-2])/128)
        self.current_stamina = self.browser.find_element_by_xpath('//div[@class="user_profile_progressbar progressbar"]//div[@id="stamina-progressbar"]').value_of_css_property("width")
        self.percent_stamina = round(100*float(self.current_stamina[:-2])/128)
        if self.percent_stamina < 25:
            try:
                inside_club = WebDriverWait(self.browser, 5).until(EC.element_to_be_clickable((By.XPATH,"//table[@class='table table-condensed table-top-spacing']//tbody//tr//td[4]//button[@class='btn btn-inverse btn-small']")))
                inside_club.click()
                exit_but = WebDriverWait(self.browser, 10).until(EC.element_to_be_clickable((By.XPATH,"//div[@id='page']//div[@id='content']//table[@id='content_table']//tbody//tr//td//div[@id='content_middle']//div[@class='content_style main-content ']//div[3]//div//button[@class='btn btn-inverse btn-large pull-right']")))
                if exit_but:
                    exit_but.click()
                    time.sleep(1.5)
                    self.assassult()  
            except TimeoutException:
                self.restore_stamina()
        else:
            self.assassult()
      

if __name__ == "__main__":
    login = "TwojStaryPedal" #// put your login here
    password = "pedalek" #// put your password here
    try:
        app = crims_robber(login, password)
    except:
        pass
    