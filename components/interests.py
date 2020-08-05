# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 19:07:17 2020

@author: csunj
"""

try:
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.common.exceptions import TimeoutException
    from selenium.common.exceptions import NoSuchElementException
    from selenium.common.exceptions import ElementNotInteractableException
    from selenium.webdriver.common.action_chains import ActionChains
    import time
    import sys

    sys.path.append(r'C:\Users\csunj\Downloads\getPhotos')
    from persons import Person
    #from actions import getAnchors
    
except Exception as e:
    print("Some Modules are Missing {}".format(e))



class interestCard():
    def __init__(self):
        
        #interest body paragraphs
        self.sectionClass = '//*[@class="pv-profile-section pv-interests-section artdeco-container-card artdeco-card ember-view"]'
        self.seeMorePara = 'a.lt-line-clamp__more'
        self.showMoreClass = 'button.pv-profile-section__see-more-inline'
        self.singleSpan = 'span:not(.visually-hidden)'
        self.listClass = 'div.entity-list-wrapper'
        self.contentClass='div.interest-content'
        self.aClass = 'a.pv-profile-section__card-action-bar.artdeco-container-card-action-bar'
        self.modalClass = 'div.artdeco-modal-overlay'
        self.tabClass='//li[contains(@class, "pv-interests-modal__following")]'

        #interest object classes
        self.titleClass = 'h3.pv-entity__summary-title'
        self.subClass = 'p.pv-entity__occupation'
        self.followerClass = 'p.pv-entity__follower-count'
        self.closeClass= 'button.artdeco-modal__dismiss'
        self.noModalList = 'li.pv-interest-entity'
        
        
class Interest(object):
    def __init__(self, interest=None, group=None, level=None, followers=None, role=None):    
        
        self.interest: interest
        self.group: group
        self.followers:followers
        self.role:role

    def get_interestItems(self):
        
        interest_dict  = {
            
               'Interest': self.interest,
               'Role': self.role,
               'Group': self.group,
               'Followers': self.followers,

        }
        return interest_dict
    
    def get_interest(self, url, driver, wait):
        
        
        try:
            __interestCard = interestCard()
            #__anchors = getAnchors()
            
            stopWords = ['<span>', 
                             '</span>',
                             '<time>',
                             '</time>',
                             'No Expiration Date',
                             'followers',
                             'members']
            
            delay = 10
            
            Interests=[]
            try:
                section = driver.find_element_by_xpath(__interestCard.sectionClass)
        
            except:
                section = []
                
            if not section:
                print('No interests!')
            else:
                try:
                    anchor = section.find_element_by_css_selector(__interestCard.aClass)
                    moveEvents = ActionChains(driver)
                    moveEvents.move_to_element(anchor).perform()
                    
                except NoSuchElementException:
                    print('Could not find anchor to expand interests!')
                    anchor=''
                    
                if anchor !='':
                    try:
                        anchor.click()
    
                    except ElementNotInteractableException:
                        print('cant expand further!')
       
                    modal = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,__interestCard.modalClass)))       
                    
                    try:
                        tabs = modal.find_elements_by_xpath(__interestCard.tabClass)
                    
                    except NoSuchElementException:
                        print('No tabs found!')
                        tabs=''
                   
                    for tab in tabs:
                        
                        try:
                            group = tab.text
                            
                            tab.click()
                            
                            time.sleep(2)
                            wrapper = WebDriverWait(modal, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,__interestCard.listClass)))       
                            wrapper = modal.find_element_by_css_selector(__interestCard.listClass)
                            
                            lists = wrapper.find_elements_by_css_selector(__interestCard.contentClass)
                            
                            for item in lists:
                                
                                
                                try:
                                    interest = item.find_element_by_css_selector(__interestCard.titleClass)
                                    interest = interest.text
                                except NoSuchElementException:
                                    print('No title!')
                                    interest =''
                                
                                try:
                                    role = item.find_element_by_css_selector(__interestCard.subClass)
                                    role = role.text
                                except NoSuchElementException:
                                    print('No role!')
                                    role =''
                                    
                                try:
                                    followers=item.find_element_by_css_selector(__interestCard.followerClass)
                                    followers=followers.text
            
                                    for word in stopWords:
                                        if word in followers:
                                            followers=followers.replace(word,"")
                                    
                                except NoSuchElementException:
                                    print('No role!')
                                    followers =''   
                                
                                
                                self.interest=interest
                                self.group=group
                                self.followers=followers
                                self.role=role
                                
                                print(self.interest)
                                print(self.group)
                                print(self.followers)
                                print(self.role)
                                
                            
                                interests = Interest.get_interestItems(self)
                                Interests.append(interests)
                        
                        except (NoSuchElementException, TimeoutException):
                                print(Person.fullName + ' does not have any interests!')
        
                    try:
                        modal.find_element_by_css_selector(__interestCard.closeClass).click()
                
                    except NoSuchElementException:
                        print('Can not find close button!')
                        
                else:
                    
                    try:
                        lists = section.find_elements_by_css_selector(__interestCard.noModalList)
                        
                        for item in lists:
                            
                            group = ''
                            
                            try:
                                interest = item.find_element_by_css_selector(__interestCard.titleClass)
                                interest = interest.text
                            except NoSuchElementException:
                                print('No title!')
                                interest =''
                            
                            try:
                                role = item.find_element_by_css_selector(__interestCard.subClass)
                                role = role.text
                            except NoSuchElementException:
                                print('No role!')
                                role =''
                                
                            try:
                                followers=item.find_element_by_css_selector(__interestCard.followerClass)
                                followers=followers.text
        
                                for word in stopWords:
                                    if word in followers:
                                        followers=followers.replace(word,"")
                                
                            except NoSuchElementException:
                                print('No role!')
                                followers =''   
                            
                            
                            self.interest=interest
                            self.group=group
                            self.followers=followers
                            self.role=role
                            
                            print(self.interest)
                            print(self.group)
                            print(self.followers)
                            print(self.role)
                            
                        
                            interests = Interest.get_interestItems(self)
                            Interests.append(interests)
                
                    except (NoSuchElementException, TimeoutException):
                        print(Person.fullName + ' does not have any interests!')                                                        

        except NoSuchElementException:
            print(Person.fullName + ' does not have any interests history!')

        
        return Interests
        
 