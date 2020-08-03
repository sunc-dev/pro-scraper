# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 23:19:16 2020

@author: csunj
"""
try:
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.common.exceptions import NoSuchElementException
    import sys

    sys.path.append(r'C:\Users\csunj\Downloads\getPhotos')
    from actions import getAnchors
    
except Exception as e:
    print("Some Modules are Missing {}".format(e))
    
class topCard():
    def __init__(self, urlClass=None, cardClass=None, bodyClass=None,nameClass=None, imgClass=None, headClass=None,  companyClass=None, locClass=None):    

        self.cardClass ='section.pv-top-card'
        self.nameClass='li.inline.t-24' 
        self.imgClass='//div[@class="presence-entity pv-top-card__image presence-entity--size-9 ember-view"]/img'
        self.headClass='h2.mt1.t-18.t-black.t-normal' 
        self.companyClass='//span[@class="text-align-left ml2 t-14 t-black t-bold full-width lt-line-clamp lt-line-clamp--multi-line ember-view"]' 
        self.listClass='ul.pv-top-card--list.pv-top-card--list-bullet.mt1'
        self.locationClass = 'li.t-16.t-black.t-normal'
        self.connectionsClass = 'span.t-16.t-black.t-normal'
        
        
class Person(object):
    def __init__(self,Id=None, linkedInUrl=None, fullName=None, imgUrl=None, headLine=None, company=None, location=None):    
        self.Id=Id
        self.linkedInUrl=linkedInUrl
        self.fullName=fullName
        self.imgUrl=imgUrl
        self.headLine=headLine
        self.company=company
        self.location=location
    
    
    def get_profileItems(self):

        person_dict  = {
                
            'Id': self.Id,
            'Url': self.linkedInUrl,
            'FullName':  self.fullName,
            'ImgUrl': self.imgUrl,
            'Header': self.headLine,
            'Company': self.company,
            'Location': self.location,
            'Connections': self.connections
                
        }
            
        return person_dict
  
    
    def get_profileCard(self, url, driver, wait):
            
        
            __personCard = topCard()
            
            
            try:
                wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, __personCard.cardClass )))    
            
                __topCard = driver.find_element_by_css_selector(__personCard.cardClass)   
            
                name =  __topCard.find_element_by_css_selector(__personCard.nameClass)
                img = __topCard.find_element_by_xpath(__personCard.imgClass)
                headLine = __topCard.find_element_by_css_selector(__personCard.headClass)
                company = __topCard.find_element_by_xpath(__personCard.companyClass)
            
                __listInfo = __topCard.find_elements_by_css_selector(__personCard.listClass)
            
                for objects in __listInfo:
                    location = objects.find_element_by_css_selector(__personCard.locationClass)
                    connections = objects.find_element_by_css_selector(__personCard.connectionsClass)
                
                
        
                self.Id = url[0]
                self.linkedInUrl = url[1]
                self.fullName = name.text
                self.imgUrl = img.get_attribute("src")
                self.headLine = headLine.text
                self.company = company.text
                self.location = location.text
                self.connections = connections.text
            
                
            
            
            except (TimeoutException,NoSuchElementException):
                print("A class was not found!")
    
            
            persons = Person.get_profileItems(self)
            
            return persons
    



class aboutCard():
    def __init__(self, profileClass=None, aboutClass=None, aboutPClass=None, seeMoreClass=None):    
        
        self.profileClass = 'div.profile-detail'
        self.aboutClass = 'section.artdeco-container-card.pv-profile-section.pv-about-section.ember-view'
        self.aboutPClass = 'p.pv-about__summary-text'
        self.seeMoreClass = 'line-clamp-show-more-button'




class About(object):
    def __init__(self, about=None):
        self.about=about
    
    
    def get_aboutItems(self):
        
        about_dict = {
            
            'About' : self.about
            
            }
        
        return about_dict
    
    
    def get_about(self, url, driver, wait):
        
        __aboutCard = aboutCard()
        __anchors = getAnchors()
    
    
        try: 

            about = __anchors.seeMore(driver, __aboutCard.aboutPClass, __aboutCard.seeMoreClass)
            
            print(about)
            
            self.about=about
            
                    
        except NoSuchElementException:
            print(Person.fullName + ' does not have an about section')
    
        abouts = About.get_aboutItems(self)
        
        return abouts
        
 