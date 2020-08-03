# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 19:07:17 2020

@author: csunj
"""

try:
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.action_chains import ActionChains

    import sys

    sys.path.append(r'C:\Users\csunj\Downloads\getPhotos')
    from persons import Person
    from actions import getAnchors
    
except Exception as e:
    print("Some Modules are Missing {}".format(e))
    
class volunteerCard():
    def __init__(self):
        
        #volunteer body paragraphs
        self.sectionClass = '//*[@class="pv-profile-section volunteering-section ember-view"]'
        self.seeMorePara = 'inline-show-more-text__button link'
        self.showMoreClass = 'button.pv-profile-section__see-more-inline.pv-profile-section__text-truncate-toggle.link.link-without-hover-state'
        self.singleSpan = 'span:not(.visually-hidden)'
        #volunteer object classes
        self.volunteerClass = 'h3.t-16'
        self.listClass = 'li.pv-profile-section__list-item.pv-volunteering-entity'
        self.orgClass = 'span.pv-entity__secondary-title'
        self.dateClass = 'h4.pv-entity__date-range'
        self.lengthClass = 'span.pv-entity__bullet-item'
        self.causeClass = 'span.pv-volunteer-causes'
        self.noteClass = 'p.pv-entity__description'
        
class Volunteer(object):
    def __init__(self, volunteer=None, org=None, cause=None, startAt=None, endAt=None, length=None, note=None):    
        
        self.volunteer: volunteer
        self.org: org
        self.cause: cause
        self.startAt: startAt
        self.endAt: endAt
        self.length: length
        self.note: note

    def get_volunteerItems(self):
        
        volunteer_dict  = {
            
            'Volunteer': self.volunteer,
            'Organization': self.org,
            'Cause': self.cause,
            'StartAt': self.startAt,
            'EndAt': self.endAt,
            'Length': self.length,
            'Note':self.note
        
        }
        
        return volunteer_dict
    
    def get_volunteer(self, url, driver, wait):
        
        
        try:
            __volunteerCard = volunteerCard()
            __anchors = getAnchors()
            
            stopWords = ['<span>', 
                             '</span>',
                             '<time>',
                             '</time>']
            
            Volunteers=[]

            try:
                volunteerListings = __anchors.showMore(driver, __volunteerCard.sectionClass, __volunteerCard.seeMorePara, __volunteerCard.showMoreClass)
               
            except NoSuchElementException:
                print('No listings')
                volunteerListings =''
             
            if volunteerListings != '':
                #moveEvents = ActionChains(driver)
                #moveEvents.move_to_element(volunteerListings).perform()    
            
            
                try:
    
                    volunteerLists = volunteerListings.find_elements_by_css_selector(__volunteerCard.listClass)
    
                    if not volunteerLists:
                        print('No volunteer history!')
                    
                    else:
                        
                        for volunteers in volunteerLists:
                            
                            #volunteer classes
                            volunteer= volunteers.find_element_by_css_selector(__volunteerCard.volunteerClass)
                            
                            moveEvents = ActionChains(driver)
                            moveEvents.move_to_element(volunteer).perform()
                            
                            volunteer=volunteer.text
                            
                          
                            try:
                                org = volunteers.find_element_by_css_selector(__volunteerCard.orgClass)
                                org = org.text
                            except NoSuchElementException:
                                org=''
                            
                              
                         
                            
                            try:
                                cause = volunteers.find_element_by_css_selector(__volunteerCard.causeClass)
                                cause = cause.text
                            except NoSuchElementException:
                                cause=''
                            
                              
                            
                            
                            try:
                                date = volunteers.find_element_by_css_selector(__volunteerCard.dateClass)
                                date = date.find_element_by_css_selector(__volunteerCard.singleSpan)
                            except NoSuchElementException:
                                date =''
                            
                            if date != '':
                                date = driver.execute_script("return arguments[0].innerHTML;", date)
                                
                                if 'span' in date:
                                    date = (date.partition("</span>")[2]).strip()
    
                                for word in stopWords:
                                    if word in date:
                                        date=date.replace(word,"")
                                    
                                date = date.split(' – ')
                                
                                if len(date)> 2:
                                    startAt = date[0].strip()
                                    endAt = date[1].strip()
                                else:
                                    startAt = date[0].strip()
                                    endAt=''
                                    
                            else:
                                startAt=''
                                endAt=''   
                                
                            
                            try:
                                length = volunteers.find_element_by_css_selector(__volunteerCard.lengthClass)
                                length=length.text
                            except NoSuchElementException:
                                length=''
                    
                            
                            try:
                                note = volunteers.find_element_by_css_selector(__volunteerCard.noteClass)
                                note = note.text
                            except NoSuchElementException:
                                note=''
                                
                            self.volunteer=volunteer
                            self.org=org
                            self.cause=cause
                            self.startAt=startAt
                            self.endAt=endAt
                            self.length=length
                            self.note =note
                            
                            print(self.volunteer)
                            print(self.org)
                            print(self.cause)
                            print(self.startAt)
                            print(self.endAt)
                            print(self.length)
                            print(self.note)
                        
                            volunteer = Volunteer.get_volunteerItems(self)
                            Volunteers.append(volunteer)
                        
                except NoSuchElementException:
                    print(Person.fullName + ' does not have any volunteering!')
            
            else:
                print(Person.fullName + ' does not have any volunteering!')

        except NoSuchElementException:
            print(Person.fullName + ' does not have any volunteering!')

        
        return Volunteers
        
 