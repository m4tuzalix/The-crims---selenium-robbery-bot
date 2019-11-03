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

class crims_gang():
    
    def __init__(self, login, password, counter=0):
        self.login = login
        self.password = password
        self.browser = webdriver.Chrome("D:\selenium\chromedriver.exe")
        self.browser.get("https://www.thecrims.com/")
        self.action = ActionChains(self.browser)
        
        
    
        self.log_in()
        self.gang()
        
                 

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

    def gang(self):
        self.current_stamina = self.browser.find_element_by_xpath('//div[@class="user_profile_progressbar progressbar"]//div[@id="stamina-progressbar"]').value_of_css_property("width")
        self.percent_stamina = round(100*float(self.current_stamina[:-2])/128)

        current_toxic = self.browser.find_element_by_xpath('//div[@class="user_profile_progressbar progressbar"]//div[@id="addiction-progressbar"]').value_of_css_property("width")
        percent_toxic = round(100*float(current_toxic[:-2])/128)

        if self.percent_stamina > 24:
            but = WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="menu-sprite-robbery"]')))
            WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
            if but:
                but.click()
                try:
                    gang_rob = WebDriverWait(self.browser, 30).until(EC.element_to_be_clickable((By.XPATH, "//div[@class='content_style main-content ']//div//div[6]//button[@id='gangrobbery-accept']")))
                    WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
                    if gang_rob:
                        gang_rob.click()
                        if self.percent_stamina > 24:
                            self.gang()
                        else:
                            self.restore_stamina()
                            self.restore()

                except TimeoutException:
                    self.gang()
        else:
            self.restore_stamina()
            self.restore()
    

        # #//// checks toxiacation and proceeds
        #     if percent_toxic >= 10:
        #         time.sleep(0.75)
        #         tox = WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH, '//div[@id="menu-hospital"]')))
        #         if tox:
        #             tox.click()
        #             heal = WebDriverWait(self.browser, 20).until(EC.visibility_of_element_located((By.XPATH,"//table[@class='table-top-spacing']//tr//td[2]//button")))
        #             if heal:
        #                 heal.click()
        #                 time.sleep(0.75)
        #                 self.restore_stamina()
        #     else:
        #         time.sleep(0.75)
        #         self.restore_stamina()

    def restore_stamina(self):
        self.random_club = random.randint(1,5)
        
        club = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, '//div[@id="menu-sprite-nightlife"]')))
        if club:
            try:
                club.click()
            except ElementClickInterceptedException:
                WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
                club.click()
                
        WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "text-center")))
        WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
        clubs = WebDriverWait(self.browser, 20).until(EC.element_to_be_clickable((By.XPATH, f'//ul[@class="nightclubs unstyled"]//li[{str(self.random_club)}]//div[@class="well well-small"]//div[2]//button[@class="btn btn-inverse btn-small pull-right"]'))).click()
        if clubs:
            try:
                clubs.click()
            except:
                WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "text-center")))
                WebDriverWait(self.browser, 20).until(EC.invisibility_of_element_located((By.CLASS_NAME, "overlay")))
                clubs.click()
    
    def restore(self):
        self.current_stamina = self.browser.find_element_by_xpath('//div[@class="user_profile_progressbar progressbar"]//div[@id="stamina-progressbar"]').value_of_css_property("width")
        self.percent_stamina = round(100*float(self.current_stamina[:-2])/128)
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
                        self.browser.execute_script("""setTimeout(()=>{
                            document.querySelector("button.btn.btn-inverse.btn-large.pull-right").click();
                            },500);""")
                        self.browser.execute_script("""setTimeout(()=>{
                                document.querySelector("div[id='menu-sprite-robbery'").click();
                        },2000);""")
                        self.gang()
                            
                except ElementClickInterceptedException or StaleElementReferenceException:
                    self.restore_stamina()
                    self.restore()
        except:
            raise
        

if __name__ == "__main__":
    login = "matrioch69" #// put your login here
    password = "69matrioh" #// put your password here
    try:
        app = crims_gang(login, password)
    except:
        try:
            for p in psutil.process_iter():
                if "chrome" in p.name():
                    p.kill()
            app = crims_gang(login, password)
        except psutil.NoSuchProcess:
            app = crims_gang(login, password)