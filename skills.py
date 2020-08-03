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



class skillCard():
    def __init__(self):
        
        #skill body paragraphs
        self.sectionClass = '//*[@class="pv-profile-section pv-skill-categories-section artdeco-container-card artdeco-card ember-view"]'
        self.seeMorePara = 'inline-show-more-text__button link'
        self.showMoreClass = 'button.pv-profile-section__card-action-bar.pv-skills-section__additional-skills'
        self.singleSpan = 'span:not(.visually-hidden)'
        self.listClass = 'div.pv-skill-category-entity__skill-wrapper'

        #skill object classes
        self.skillClass = 'p.pv-skill-category-entity__name'
        self.endorseClass = 'span.pv-skill-category-entity__endorsement-count'

       
        
class Skill(object):
    def __init__(self, skill=None, endorse=None):    
        
        self.skill: skill
        self.endorse: endorse


    def get_skillItems(self):
        
        skill_dict  = {
            
            'Skill': self.skill,
            'Endorsement': self.endorse,
      
        }
        
        return skill_dict
    
    def get_skill(self, url, driver, wait):
        
        
        try:
            __skillCard = skillCard()
            __anchors = getAnchors()
            
            #stopWords = ['<span>', 
             #                '</span>',
              #               '<time>',
               #              '</time>',
                #             'No Expiration Date']
            
            Skills=[]
        
            skillListings = __anchors.showMore(driver, __skillCard.sectionClass, __skillCard.seeMorePara, __skillCard.showMoreClass)
            
            if skillListings !='':
                moveEvents = ActionChains(driver)
                moveEvents.move_to_element(skillListings).perform()  
                try:
                                    
                    skillLists = skillListings.find_elements_by_css_selector(__skillCard.listClass)
                    
                    if not skillLists:
                        print('No skill history!')
                    
                    else:
                        
                        for skills in skillLists:
                            
                            #skill classes
                            skill= skills.find_element_by_css_selector(__skillCard.skillClass)
                            skill=skill.text
                            try:
                                endorse = skills.find_element_by_css_selector(__skillCard.endorseClass)
                                endorse=endorse.text
                            except NoSuchElementException:
                                endorse=''
                            
    
                            self.skill=skill
                            self.endorse=endorse
                            
                            print(self.skill)
                            print(self.endorse)
                         
                            
                        
                            Ability = Skill.get_skillItems(self)
                            Skills.append(Ability)
                        
                except NoSuchElementException:
                    print(Person.fullName + ' does not have any skillificantions!')
            
        except NoSuchElementException:
            print(Person.fullName + ' does not have any skillfication history!')

        
        return Skills
        
 