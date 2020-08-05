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
    from selenium.common.exceptions import ElementNotInteractableException

    import sys

    sys.path.append(r'C:\Users\csunj\Downloads\getPhotos')
    from persons import Person
    from actions import getAnchors
    
except Exception as e:
    print("Some Modules are Missing {}".format(e))



class featCard():
    def __init__(self):
        
        #feat body paragraphs
        self.sectionClass = '//*[@class="pv-profile-section pv-accomplishments-section artdeco-container-card artdeco-card ember-view"]'
        self.seeMorePara = 'a.lt-line-clamp__more'
        self.showMoreClass = 'button.pv-profile-section__see-more-inline'
        self.chevClass = 'button.pv-accomplishments-block__expand'
        self.singleSpan = 'span:not(.visually-hidden)'
        self.listClass = 'section.pv-profile-section.pv-accomplishments-block'
        self.subClass='li:not(.artdeco-entity-pile__entity)'

        #feat object classes
        self.featTitleClass = 'h3.pv-accomplishments-block__title'
        self.featClass = 'h4.pv-accomplishment-entity__title'
        self.levelClass = 'p.pv-accomplishment-entity__proficiency'
        self.publishClass = 'span.pv-accomplishment-entity__publisher'
        self.highlightClass = 'p.pv-accomplishment-entity__description'
        self.adminClass = 'span.pv-accomplishment-entity__issuer'
        self.roleClass ='span.pv-accomplishment-entity__position'
        self.dateClass = 'span.pv-accomplishment-entity__date'
        
class Feat(object):
    def __init__(self, feat=None, featType=None, level=None, highlight=None, admin=None, role=None, date=None):    
        
        self.feat: feat
        self.featType: featType
        self.level: level
        self.highlight: highlight
        self.admin: admin
        self.role: role
        self.date: date

    def get_featItems(self):
        
        feat_dict  = {
            
               'Feat': self.feat,
               'FeatType': self.featType,
               'Level': self.level,
               'Highlight': self.highlight,
               'Admin': self.admin,
               'Role': self.role,
               'CompleteAt': self.date
        }
        
        return feat_dict
    
    def get_feat(self, url, driver, wait):
        
        
        try:
            __featCard = featCard()
            __anchors = getAnchors()

            Feats=[]
            featListings = driver.find_element_by_xpath(__featCard.sectionClass)
        
            
            try:

                featLists = featListings.find_elements_by_css_selector(__featCard.listClass)

                if not featLists:
                    print('No feat history!')
                
                else:
                    
                    for sections in featLists:
                        
                        group=''
                        
                        #Find 
                        try:
                            featChev = sections.find_element_by_css_selector(__featCard.chevClass)
                        except NoSuchElementException:
                            featChev=''
                            
                        if featChev !='':
                            try:
                                featChev.click()

                            except ElementNotInteractableException:
                                print('cant expand further!')

                        try:
                            featType= sections.find_element_by_css_selector(__featCard.featTitleClass)
                            featType=featType.text
                        except NoSuchElementException:
                            print('No feat group')        
                        
                        group = sections.find_elements_by_css_selector(__featCard.subClass)
                        
                        for feats in group:
                            #feat classes
                            
                                
                            try:   
                                feat=feats.find_element_by_css_selector(__featCard.featClass)
                            except NoSuchElementException:
                                print('No feat')
                                feat=''    
                                
                            feat = __anchors.getString(driver, feat)    
                                
                            try:
                                level = feats.find_element_by_css_selector(__featCard.levelClass)
                                level = level.text
                            except NoSuchElementException:
                                print('No proficiency')
                                level =''
                            
                            try:
                                highlight = feats.find_element_by_css_selector(__featCard.highlightClass)
                               
                            except NoSuchElementException:
                                print('No note highlights')
                                highlight=''
                            
                            highlight = __anchors.getString(driver, highlight)
                                
                            try:    
                                admin= feats.find_element_by_css_selector(__featCard.adminClass)
                            except NoSuchElementException:
                                print('No issuer')
                                admin =''
                            
                            admin = __anchors.getString(driver, admin)
                                
                            try:    
                                role = feats.find_element_by_css_selector(__featCard.roleClass)                            
                            except NoSuchElementException:
                                print('No role')
                                role=''
                            
                            role = __anchors.getString(driver,role)
                                
                            try:    
                                date = feats.find_element_by_css_selector(__featCard.dateClass)
                                
                            except NoSuchElementException:
                                print('No date')
                                date=''
                            
                            date = __anchors.getString(driver, date)
                            
                            self.feat=feat
                            self.featType=featType
                            self.level=level
                            self.highlight=highlight
                            self.admin= admin
                            self.role= role
                            self.date=date
                            
                            print(self.feat)
                            print(self.featType)
                            
                        
                            featItem = Feat.get_featItems(self)
                            Feats.append(featItem)
                    
            except NoSuchElementException:
                print(Person.fullName + ' does not have any feats!')
        
        except NoSuchElementException:
            print(Person.fullName + ' does not have any feats history!')

        
        return Feats
        
 