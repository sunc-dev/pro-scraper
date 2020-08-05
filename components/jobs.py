# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 22:09:00 2020

@author: csunj
"""

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
    from selenium.webdriver.common.action_chains import ActionChains

    import sys

    sys.path.append(r'C:\Users\csunj\Downloads\getPhotos')
    from persons import Person
    from actions import getAnchors
    
except Exception as e:
    print("Some Modules are Missing {}".format(e))
    
class jobCard():
    def __init__(self):    

        #job body classes
        self.sectionClass = '//*[@id="experience-section"]'
        self.seeMorePara = 'inline-show-more-text__button link'
        self.showMoreClass = 'button.pv-profile-section__see-more-inline.pv-profile-section__text-truncate-toggle.link.link-without-hover-state'
        self.listClass = 'li.pv-entity__position-group-pager.pv-profile-section__list-item.ember-view'
        self.listTag = './/li'
        self.listClassBody =  'pv-entity__position-group-pager pv-profile-section__list-item ember-view'
        self.ulClass = 'ul.pv-entity__position-group'
        self.infoClass = 'div.pv-entity__role-details'

        
        #job object classes
        self.past = 't-16 t-black t-bold'
        self.current = 't-14 t-black t-bold'
        self.companyLength = 'h4.t-14.t-black.t-normal'
        self.positionClass = 'li.pv-entity__position-group-role-item'
        self.companyClass = 'p.pv-entity__secondary-title'  
        self.dateClass = 'h4.pv-entity__date-range'
        self.lengthClass = 'span.pv-entity__bullet-item-v2'
        self.localeClass =' h4.pv-entity__location'
        self.noteClass = 'p.pv-entity__description'
        
        #layout classes
        self.spanFilter = 'span:not(.visually-hidden)'


class Job(object):
    def __init__(self, company=None, companylength=None, job=None, length=None, location=None, startAt=None, endAt=None, note=None):    

        self.company = company
        self.companylength = companylength
        self.job = job
        self.length = length
        self.location = location
        self.startAt = startAt
        self.endAt = endAt
        self.note = note
    
    def get_jobItems(self):

        job_dict  = {
                
            'Company': self.company,
            'CompanyLength': self.companylength,
            'Job': self.job,
            'length':  self.length,
            'location': self.location,
            'StartAt': self.startAt,
            'EndAt': self.endAt,
            'Note': self.note

                
        }
        
        return job_dict
    
    def get_jobs(self, url, driver, wait):
        
        try:
            __jobCard = jobCard()
            __anchors = getAnchors()
            
            experiences = []

            joblistings = __anchors.showMore(driver, __jobCard.sectionClass, __jobCard.seeMorePara, __jobCard.showMoreClass)
            
            if joblistings !='':  
                moveEvents = ActionChains(driver)
                moveEvents.move_to_element(joblistings).perform() 
            
            #get all list items   
                try:
                    
                    joblists = joblistings.find_elements_by_css_selector(__jobCard.listClass)
                    
                    for joblisting in joblists:
                        
                        positions=[]
                        
                        positions = joblisting.find_elements_by_css_selector(__jobCard.ulClass)
                        
                        if not positions:
                            
                            #Job details
                            try: 
                                company = joblisting.find_element_by_css_selector(__jobCard.companyClass)
                                company=company.text
                            except NoSuchElementException:
                                company=''
                             
                            try:
                                job = joblisting.find_element_by_xpath('.//h3[@class="'+__jobCard.past+'"]')
                                job = job.text
                            
                            except NoSuchElementException:
                                job=''
                            
                            try:
                                date = joblisting.find_element_by_css_selector(__jobCard.dateClass)
                            except NoSuchElementException:
                                date = ''
                            
                            try:
                                
                                length = joblisting.find_element_by_css_selector(__jobCard.lengthClass)
                                length = length.text
                            except NoSuchElementException:
                                length = ''
                            
                            try:
                                note = joblisting.find_element_by_css_selector(__jobCard.noteClass)
                                note = note.text
                            except NoSuchElementException:
                                note = ''
                            
                            try:
                                location = joblisting.find_element_by_css_selector(__jobCard.localeClass)
                            
                            except NoSuchElementException:
                                location = ''
                    
            
                            #Remove stop words
                            
                            #Date
                            date = __anchors.getString(driver,date)
                            
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
                            
                            #Location
                            location = __anchors.getString(driver,location)


                            self.company = company
                            self.companylength = length
                            self.job = job
                            self.length = length
                            self.location = location
                            self.startAt = startAt
                            self.endAt = endAt
                            self.note = note
                            
                            
                            print(self.company)
                            print(self.companylength)
                            print(self.job)
                            print(self.length)
                            print(self.location)
                            print(self.startAt)
                            print(self.endAt)
                            print(self.note)
                        
                            experience = Job.get_jobItems(self)
                            experiences.append(experience)  
                        
                        else:
                             #Job Details
                            infos = joblisting.find_elements_by_css_selector(__jobCard.infoClass)
                             
                            try:
                                company = joblisting.find_element_by_xpath('.//h3[@class="'+__jobCard.past+'"]')
                            
                            except NoSuchElementException:
                                company=''
                             
                            company = __anchors.getString(driver,company)

                            try:
                                 companylength = joblisting.find_element_by_css_selector(__jobCard.companyLength)
                            except NoSuchElementException:
                                 companylength=''
            
                            companylength = __anchors.getString(driver,companylength)
                             
                            for info in infos:
                                try:
                                 #Job Details 
                                    job = info.find_element_by_xpath('.//h3[@class="'+__jobCard.current+'"]')
                                except NoSuchElementException:
                                    job = ''
                                job = __anchors.getString(driver,job)
                                
                                try:
                                    date = info.find_element_by_css_selector(__jobCard.dateClass)
                                except NoSuchElementException:
                                    date = ''
                                
                                #Date
                                date = __anchors.getString(driver,date)
                                 
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
                            
                                try:
                                    length = info.find_element_by_css_selector(__jobCard.lengthClass)
                                    length = length.text
                                except NoSuchElementException:
                                    length = ''
                            
                                try:
                                    note = info.find_element_by_css_selector(__jobCard.noteClass)
                                    note = note.text
                                
                                except NoSuchElementException:
                                    note = ''
                        
                                #Location
                                try:
                                    location = info.find_element_by_css_selector(__jobCard.localeClass)
                                except NoSuchElementException:
                                    location = ''
                                
                                location = __anchors.getString(driver, location)
                                                
                            
                                self.company = company
                                self.companylength = companylength
                                self.job = job
                                self.length = length
                                self.location = location
                                self.startAt = startAt
                                self.endAt = endAt
                                self.note = note
                                
                                print(self.company)
                                print(self.companylength)
                                print(self.job)
                                print(self.length)
                                print(self.location)
                                print(self.startAt)
                                print(self.endAt)
                                print(self.note)
                        
                                experience = Job.get_jobItems(self)
                                experiences.append(experience)       
                
                except NoSuchElementException:
                    print(Person.fullName + ' does not have any job titles!')
            else:
                print(Person.fullName + ' does not have any experience!')   
            
        
        except NoSuchElementException:
            print(Person.fullName + ' does not have any experience!')
            

        
        return experiences
            
     


