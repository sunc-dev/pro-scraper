# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 19:07:17 2020

@author: csunj
"""

try:
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.action_chains import ActionChains

    import sys

    sys.path.append(r'C:\Users\csunj\Downloads\getPhotos')
    from persons import Person
    from actions import getAnchors
    
except Exception as e:
    print("Some Modules are Missing {}".format(e))



class certCard():
    def __init__(self):
        
        #cert body paragraphs
        self.sectionClass = '//*[@id="certifications-section"]'
        self.seeMorePara = 'inline-show-more-text__button link'
        self.showMoreClass = 'button.pv-profile-section__see-more-inline.pv-profile-section__text-truncate-toggle.link.link-without-hover-state'
        self.singleSpan = 'span:not(.visually-hidden)'
        self.listClass = 'li.pv-certification-entity'

        #cert object classes
        self.certClass = 'h3.t-16.t-bold'
        self.adminClass = 'p.t-14'
        self.validClass = 'span.pv-entity__bullet-item-v2'
        self.dateClass = 'p.pv-entity__dates'
       
        
class Cert(object):
    def __init__(self, cert=None, admin=None, issue=None, valid=None):    
        
        self.cert: cert
        self.admin: admin
        self.issue: issue
        self.valid: valid

    def get_certItems(self):
        
        cert_dict  = {
            
            'Certification': self.cert,
            'Administrator': self.admin,
            'IssueAt': self.issue,
            'ValidAt': self.valid,
        
        }
        
        return cert_dict
    
    def get_cert(self, url, driver, wait):
        
        
        try:
            __certCard = certCard()
            __anchors = getAnchors()
                        
            certifications=[]
        
            certListings = __anchors.showMore(driver, __certCard.sectionClass, __certCard.seeMorePara, __certCard.showMoreClass)
            if certListings !='':
                try:
                    
                    certLists = certListings.find_elements_by_css_selector(__certCard.listClass)
                    
                    if not certLists:
                        print('No cert history!')
                    
                    else:
                        
                        for certs in certLists:
                            moveEvents = ActionChains(driver)
                            moveEvents.move_to_element(certs).perform()
                            #cert classes
                            cert= certs.find_element_by_css_selector(__certCard.certClass)
                            cert = cert.text
                            try:
                                admin = certs.find_element_by_css_selector(__certCard.adminClass)
                            except NoSuchElementException:
                                admin=''
                                
                            admin = __anchors.getString(driver, admin)
                            
                            try:
                                issue = certs.find_element_by_css_selector(__certCard.validClass)
                                issue = issue.find_element_by_xpath('..')
                                                
                            except NoSuchElementException:
                                issue=''
                            
                            issue = __anchors.getString(driver, issue)
                            
                            try:
                                valid = certs.find_element_by_css_selector(__certCard.validClass)
                                valid=valid.text
                            except NoSuchElementException:
                                valid =''
                            
                            self.cert=cert
                            self.admin=admin
                            self.issue=issue
                            self.valid=valid
                            
                            print(self.cert)
                            print(self.admin)
                            print(self.issue)
                            print(self.valid)
                            
                        
                            certification = Cert.get_certItems(self)
                            certifications.append(certification)
                        
                except NoSuchElementException:
                    print(Person.fullName + ' does not have any certificantions!')
            
            else:
                print(Person.fullName + ' does not have any certfications!')
        
        except NoSuchElementException:
            print(Person.fullName + ' does not have any certfication history!')

        
        return certifications
        
 