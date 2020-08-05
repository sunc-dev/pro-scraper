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
    
class schoolCard():
    def __init__(self):
        
        #school body paragraphs
        self.sectionClass = '//*[@id="education-section"]'
        self.seeMorePara = 'inline-show-more-text__button link'
        self.showMoreClass = 'button.pv-profile-section__see-more-inline.pv-profile-section__text-truncate-toggle.link.link-without-hover-state'
        self.singleSpan = 'span:not(.visually-hidden)'
        #school object classes
        self.schoolClass = 'h3.pv-entity__school-name'
        self.listClass = 'li.pv-profile-section__list-item.pv-education-entity.pv-profile-section__card-item'
        self.degreeClass = 'span.pv-entity__comma-item'
        self.fieldClass = 'p.pv-entity__secondary-title.pv-entity__fos'
        self.dateClass = 'p.pv-entity__dates'
       
        
class School(object):
    def __init__(self, school=None, degree=None, field=None, startAt=None, endAt=None):    
        
        self.school: school
        self.degree: degree
        self.field: field
        self.startAt: startAt
        self.endAt: endAt

    def get_schoolItems(self):
        
        school_dict  = {
            
            'School': self.school,
            'Degree': self.degree,
            'Fields': self.field,
            'StartAt': self.startAt,
            'EndAt': self.endAt,
        
        }
        
        return school_dict
    
    def get_school(self, url, driver, wait):
        
        
        try:
            __schoolCard = schoolCard()
            __anchors = getAnchors()
            
            educations=[]

            try:
                schoolListings = __anchors.showMore(driver, __schoolCard.sectionClass, __schoolCard.seeMorePara, __schoolCard.showMoreClass)
               
            except NoSuchElementException:
                print('No listings')
                schoolListings =''
             
            if schoolListings != '':
                #moveEvents = ActionChains(driver)
                #moveEvents.move_to_element(schoolListings).perform()    
            
            
                try:
    
                    schoolLists = schoolListings.find_elements_by_css_selector(__schoolCard.listClass)
    
                    if not schoolLists:
                        print('No school history!')
                    
                    else:
                        
                        for schools in schoolLists:
                            moveEvents = ActionChains(driver)
                            moveEvents.move_to_element(schools).perform()

                            #School classes
                            school= schools.find_element_by_css_selector(__schoolCard.schoolClass)
                            school = school.text
                           
                            try:
                                degree = schools.find_element_by_css_selector(__schoolCard.degreeClass)
                            except NoSuchElementException:
                                degree=''
                                
                            degree = __anchors.getString(driver, degree)
                            
                            try:
                                field = schools.find_element_by_css_selector(__schoolCard.fieldClass)
                                field = field.find_element_by_css_selector(__schoolCard.singleSpan)
                            
                            except NoSuchElementException:
                                field=''
                            
                            field = __anchors.getString(driver, field)

                            try:
                                date = schools.find_element_by_css_selector(__schoolCard.dateClass)
                                date = date.find_element_by_css_selector(__schoolCard.singleSpan)
                            except NoSuchElementException:
                                date =''
                            
                            date = __anchors.getString(driver, date)
                      
                            if date !='':       
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
                        
                            self.school=school
                            self.degree=degree
                            self.field=field
                            self.startAt=startAt
                            self.endAt=endAt
                            
                            print(self.school)
                            print(self.degree)
                            print(self.field)
                            print(self.startAt)
                            print(self.endAt)
                            
                        
                            education = School.get_schoolItems(self)
                            educations.append(education)
                        
                except NoSuchElementException:
                    print(Person.fullName + ' does not have any schooling!')
            
            else:
                print(Person.fullName + ' does not have any schooling!')

        except NoSuchElementException:
            print(Person.fullName + ' does not have any schooling!')

        
        return educations
        
 