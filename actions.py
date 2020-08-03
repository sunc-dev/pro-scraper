# -*- coding: utf-8 -*-
"""
Created on Sat Jul 25 08:29:39 2020

@author: csunj
"""

try:
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.common.exceptions import StaleElementReferenceException
    from selenium.common.exceptions import ElementNotInteractableException

    import time
 

except Exception as e:
    print("Some Modules are Missing {}".format(e))
    






class getAnchors():
        
        def __init__(self):    
            
            self.profileClass = 'div.profile-detail'
            self.deferClass = 'div.pv-deferred-area.pv-deferred-area--pending'
            self.seeMoreClass = 'line-clamp-show-more-button'
            self.showExpClass = 'pv-profile-section__see-more-inline pv-profile-section__text-truncate-toggle link link-without-hover-state'
            self.showSkillsClass = 'pv-profile-section__card-action-bar pv-skills-section__additional-skills artdeco-container-card-action-bar artdeco-button artdeco-button--tertiary artdeco-button--3 artdeco-button--fluid'

        def getProfile(self,driver):
            __body=''
            try:
            
                __body =  driver.find_element_by_css_selector(self.profileClass)
            
                return __body
            
            except NoSuchElementException:
                print("No hidden views found")
                

        def showSections(self, driver):
            
            try:
                
                __body = self.getProfile(driver)
                
                hiddenViews = __body.find_elements_by_css_selector(self.deferClass)
   
                if not hiddenViews:
                    print('There are no hidden views')
            
                else:
                    try:
                        for section in hiddenViews:
                            moveEvents = ActionChains(driver)
                            moveEvents.move_to_element(section).perform()
                        
                    except StaleElementReferenceException:
                        print('Class was not found')
                               
            except NoSuchElementException:
                print("No hidden views found")
        
        
        def seeMore(self, driver, __element, __button):
            
            try:
                
                __body = getAnchors.getProfile(self, driver)
                
                __elementClass = __body.find_element_by_css_selector(__element)
               
                anchors = __elementClass.find_elements_by_xpath('//*[@id="'+__button+'"]')
                
                for anchor in anchors:
                    anchor.click()
                    
                __elementClass = __body.find_element_by_css_selector(__element)
                __elementText = __elementClass.text
                
            
            except NoSuchElementException:
                print("No hidden views found")
                __elementText = ''
            
            return __elementText


        def showMore(self, driver, __element, __button, ancLink): 
           
            __elementClass=''
           
            try: 
               
               __body = getAnchors.getProfile(self, driver)
               __elementClass = __body.find_element_by_xpath(__element)
               
              
               try:
                   expands = __elementClass.find_elements_by_css_selector(ancLink)

                   if not expands:
                       print('Expands is empty')

                   
                   else:
                       for expand in expands:
                           print(expand.text)
                           time.sleep(2)
                           moveEvents = ActionChains(driver)
                           moveEvents.move_to_element(expand).perform()
                           expand.click()
   
               except NoSuchElementException:
                   print('Nothing to expand')
                   
            
               try:
                   
                   #anchors = __elementClass.find_elements_by_css_selector(__button)
                   anchors = __elementClass.find_elements_by_xpath('//*[@class="'+__button+'" or @id="'+__button+'"]')

                   if not anchors:
                       print('Anchors is empty')

                   else:
                       for anchor in anchors:
                           print(anchor.text)
                           time.sleep(2)
                          
                           try:
                                moveEvents = ActionChains(driver)
                                moveEvents.move_to_element(anchor).perform()
                                anchor.click()
                           
                           except ElementNotInteractableException:
                               print('cant expand further!')
               
               except NoSuchElementException:
                   print('Nothing to expand')
               
                
               
            except NoSuchElementException:
           
               print("No additional content found")
               __elementClass = ''
               
            return __elementClass
        
        