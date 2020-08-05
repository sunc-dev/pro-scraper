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
        
        
            navElems = driver.find_elements_by_xpath('//*[@class="pv-profile-sticky-header pv-profile-sticky-header--is-showing pv-profile-sticky-header--hidden ember-view"  or @id="extended-nav" or @class="msg-overlay-list-bubble msg-overlay-list-bubble--is-minimized msg-overlay-list-bubble--expanded mh4"]')
            for elem in navElems:
                driver.execute_script("arguments[0].style.visibility='hidden'", elem)
        
        
        def seeMore(self, driver, __element, __button):
            
            try:
                
                __body = getAnchors.getProfile(self, driver)
                
                __elementClass = __body.find_element_by_css_selector(__element)
                moveEvents = ActionChains(driver)
                moveEvents.move_to_element(__elementClass).perform()
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
            expands = ''
            anchors = ''
            
            try:   
                
                try: 
                   
                   __body = getAnchors.getProfile(self, driver)
                   __elementClass = __body.find_element_by_xpath(__element)
                   print(__elementClass.text)
                   if __elementClass.is_displayed():
                       print("Element is displayed")
                       __elementClass=__elementClass
                   else: 
                       print("Element is hidden")
                       __elementClass = ''

                except NoSuchElementException:
                    __elementClass = ''
                 
                if __elementClass != '':
                    moveEvents = ActionChains(driver)
                    moveEvents.move_to_element(__elementClass).perform()
                    
                    try:
                         expands = __elementClass.find_elements_by_css_selector(ancLink)
          
                         if not expands:
                             print('Expands is empty')  
                         else:
                             for expand in expands:
                                 
                                 if expand.is_displayed():
                                     print(expand.text)
                                     time.sleep(1)
                                     moveEvents = ActionChains(driver)
                                     moveEvents.move_to_element(expand).perform()
                                     
                                     try:    
                                         expand.click()
                                     
                                     except ElementNotInteractableException:
                                         print('Can not expand further!')
                                         
                                 else:
                                    print('Not displayed')
         
                    except NoSuchElementException:
                        print('Nothing to expand')
                         
                    try:
                         #anchors = __elementClass.find_elements_by_css_selector(__button)
                         anchors = __elementClass.find_elements_by_xpath('//*[@class="'+__button+'" or @id="'+__button+'"]')
                         if not anchors:
                             print('Anchors is empty')
          
                         else:
                             for anchor in anchors:
                                 if anchor.is_displayed():
                                     print(anchor.text)
                                     time.sleep(1)
                                     moveEvents = ActionChains(driver)
                                     moveEvents.move_to_element(anchor).perform()
                                     
                                     
    
                                     try:   
                                         anchor.click()
                                
                                     except ElementNotInteractableException:
                                         print('No anchor to click on.')
                                 else:
                                     print('anchor is not displayed!')
                     
                    except NoSuchElementException:
                        print('Nothing to expand')
                
                else:
                    print('Section not found')
                
               
            except NoSuchElementException:
               print("No content found")
               
            return __elementClass
        
        def getString(self,driver, __var):
                  
            stopWords = ['span','<span>', 
                             '</span>',
                             '<time>',
                             '</time>',
                             'No Expiration Date',
                             '<>',
                             '</>']
            
            if __var != '':
                __var = driver.execute_script("return arguments[0].innerHTML;", __var)
                                
                if any(word in __var for word in stopWords):
                    __var = (__var.partition("</span>")[2]).strip()
                for word in stopWords:
                    if word in __var:
                        __var=__var.replace(word,"")
                        
            return __var
