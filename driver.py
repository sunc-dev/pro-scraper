# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 12:59:12 2020

@author: csunj
"""

try:
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.webdriver.chrome.options import Options

    import os,sys

    
    sys.path.append(".")
    from initials import Path
    from config import login
    
    
except Exception as e:
    print("Some Modules are Missing {}".format(e))


class loginObjects():
      def __init__(self):
       self.eClass =  '//*[@id="username"]'
       self.pClass = '//*[@id="password"]'
       self.login = '//*[@id="app__container"]/main/div[2]/form/div[3]/button'


#Launch driver instance
def initDriver():
    
    #Initialize states
    lg = loginObjects()
    root = Path().root
    cred = login()
    
    headerUrl = 'https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin'
    #Set options

    
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    options.add_argument('----start-maximized')

    options.add_argument('window-size=1920x1080')
    #Driver location
    driver = webdriver.Chrome(os.path.join(root,'chromedriver.exe'), options=options)
    #Driver state and preferences
    driver.maximize_window()
    events = ActionChains(driver)

    #Load login page
    driver.get(headerUrl)
    
    #Define wait time
    wait = WebDriverWait(driver, 10)

    
    try:
    
        wait.until(EC.presence_of_element_located((By.XPATH, lg.eClass )))    
        
        inputClass = driver.find_element_by_xpath(lg.eClass )
        inputClass.send_keys(cred.email)
        
        inputClass = driver.find_element_by_xpath(lg.pClass) 
        inputClass.send_keys(cred.password)
        
        submit = driver.find_element_by_xpath(lg.login)
        submit.click()
      
    except (TimeoutException,NoSuchElementException):
        print("Page failed to load")
    
    return driver, wait, events



if __name__ == '__main__':
    
    initDriver()
    