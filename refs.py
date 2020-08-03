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



class refCard():
    def __init__(self):
        
        #ref body paragraphs
        self.sectionClass = '//*[@class="pv-profile-section pv-recommendations-section artdeco-container-card artdeco-card ember-view"]'
        self.seeMorePara = 'line-clamp-show-more-button'
        self.showMoreClass = 'button.pv-profile-section__see-more-inline'
        self.singleSpan = 'span:not(.visually-hidden)'
        self.listClass = 'li.pv-recommendation-entity.ember-view'

        #ref object classes
        self.refClass = 'h3.t-16.t-black.t-bold'
        self.roleClass = 'p.pv-recommendation-entity__headline.t-14.t-black.t-normal.pb1'
        self.contextClass = 'p.t-12.t-black--light.t-normal'
        self.highlightClass = 'div.pv-recommendation-entity__highlights'
       
        
class Ref(object):
    def __init__(self, ref=None, role=None, context=None, highlight=None):    
        
        self.ref: ref
        self.role: role
        self.context: context
        self.highlight: highlight


    def get_refItems(self):
        
        ref_dict  = {
            
            'Reference': self.ref,
            'Ref Role': self.role,
            'Context': self.context,
            'Highlight': self.highlight
        }
        
        return ref_dict
    
    def get_ref(self, url, driver, wait):
        
        
        try:
            __refCard = refCard()
            __anchors = getAnchors()
            
            #stopWords = ['<span>', 
            #                 '</span>',
            #                 '<time>',
            #                 '</time>',
            #                 'No Expiration Date']
            
            Refs=[]
        
            refListings = __anchors.showMore(driver, __refCard.sectionClass, __refCard.seeMorePara, __refCard.showMoreClass)
          
            
            if refListings !='':
                try:
    
                    refLists = refListings.find_elements_by_css_selector(__refCard.listClass)
            
                    if not refLists:
                        print('No ref history!')
                    
                    else:
                        
                        for refs in refLists:
                            #moveEvents = ActionChains(driver)
                            #moveEvents.move_to_element(refs).perform()  
                            #ref classes
                            ref= refs.find_element_by_css_selector(__refCard.refClass)
                            ref=ref.text
                            
                            try:
                                role = refs.find_element_by_css_selector(__refCard.roleClass)
                                role=role.text
                            except NoSuchElementException:
                                role=''
                                
        
                            try:
                                context = refs.find_element_by_css_selector(__refCard.contextClass)
                                context=context.text
                            except NoSuchElementException:
                                context=''
                                
                            try:
                                highlight = refs.find_element_by_css_selector(__refCard.highlightClass)
                                highlight=highlight.text
                            except NoSuchElementException:
                                highlight=''
                                
                            
    
                            self.ref=ref
                            self.role=role
                            self.context=context
                            self.highlight=highlight
                            
                            print(self.ref)
                            print(self.role)
                            print(self.context)
                            print(self.highlight)
                         
                            
                        
                            reference = Ref.get_refItems(self)
                            Refs.append(reference)
                        
                except NoSuchElementException:
                    print(Person.fullName + ' does not have any refs!')
            else: 
                print(Person.fullName + ' does not have any refs history!')

        except NoSuchElementException:
            print(Person.fullName + ' does not have any refs history!')

        
        return Refs
        
 