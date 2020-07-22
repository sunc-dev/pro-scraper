# -*- coding: utf-8 -*-
"""
Created on Tue Jul 14 11:52:48 2020

@author: csunj
"""
try:
    from selenium import webdriver
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import TimeoutException
    from selenium.common.exceptions import NoSuchElementException
    from selenium.webdriver.common.action_chains import ActionChains
    from selenium.common.exceptions import StaleElementReferenceException
    import re
    import os,sys
    import pandas as pd
    import uuid
    from flatten_json import flatten
    
    sys.path.append(r'C:\Users\csunj\Downloads\getPhotos')
    from config import creds

except Exception as e:
    print("Some Modules are Missing {}".format(e))


root = r'C:\Users\csunj\Downloads\getPhotos'# This is your Project Root
folder = os.path.join(root,'master')

#credentials
email, password = creds()

raw = pd.read_csv(os.path.join(root,folder,'result.csv'))
raw = raw.dropna(subset=['profileUrl'])
raw['Id'] = [str(uuid.uuid4()) for _ in range(len(raw.index))]
items = (raw[['Id','profileUrl']].values.tolist())



urls = raw.profileUrl.to_list()
profiles = {}

driver = webdriver.Chrome(os.path.join(root,'chromedriver.exe'))
#Defined moveTO
driver.maximize_window()
moveTo = ActionChains(driver)

driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

delay = 4 # seconds
try:
      inputName = driver.find_element_by_xpath('//*[@id="username"]')
      inputName.send_keys(email)
      inputPass = driver.find_element_by_xpath('//*[@id="password"]') 
      inputPass.send_keys(password)
      submit = driver.find_element_by_xpath('//*[@id="app__container"]/main/div[2]/form/div[3]/button')
      submit.click()
      
except TimeoutException:
        print("Failed to load")

for url in items:
    driver.get(url[1])
    delay = 20 # seconds
    try:
        Id=url[0]
        #Header section
        profile = {}
        load = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'artdeco-toasts__wormhole')))
        name = driver.find_element_by_css_selector('li.inline.t-24.t-black.t-normal.break-words').text
        title = driver.find_element_by_css_selector('h2.mt1.t-18.t-black.t-normal.break-words').text
        img = driver.find_element_by_xpath('//img[@title="'+name+'"]').get_attribute("src")
        wait = WebDriverWait(driver, 15)
        
        
        #Try to look for deferred classes
        #Deferred selector
        profileDetailClass='div.profile-detail'
        defElem = 'div.pv-deferred-area.pv-deferred-area--pending.ember-view'
        deferredBody = ''
        try:
            profileBody =  driver.find_element_by_css_selector(profileDetailClass)
            deferredBody = profileBody.find_elements_by_css_selector(defElem)
   
            if not deferredBody:
                print('Empty list')
            else:
                try:
                    for deferredClass in deferredBody:
                        moveTo.move_to_element(deferredClass).perform()
                except StaleElementReferenceException:
                    print('Element not found')
                    
        except NoSuchElementException:
            print("No defferred class found")
        
        #About section
        try:
            aboutCard=''
            aboutCard = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR,'p.pv-about__summary-text')))       
            print(aboutCard.text)
            if aboutCard !='':
            #aboutCard = driver.find_element_by_css_selector('p.pv-about__summary-text')
                try:
                    moveTo.move_to_element(aboutCard).perform()
                    a = aboutCard.find_element_by_id('line-clamp-show-more-button')
                except NoSuchElementException:
                    print("Element not found")
                    a=''   
            
            if a !='':
                a = wait.until(EC.element_to_be_clickable((By.ID, 'line-clamp-show-more-button')))
                a.click()
 
            about = driver.find_element_by_css_selector('p.pv-about__summary-text').text
        
        except (NoSuchElementException, TimeoutException):
            print("Element not found")        

       #Experience Section
       #Current Company
       
        current=[]
        currentCompany=''
        totalDuration=''
        experienceBody=''
        expHeading=''
        experienceBody = driver.find_element_by_xpath('//*[@id="experience-section"]/ul')
        expHeading = experienceBody.find_elements_by_css_selector('div.pv-entity__company-details')

        #Expand Current Experience
        expandBtn=''
        try:
            expandBtn = experienceBody.find_elements_by_css_selector("button.inline-show-more-text__button")
        except (NoSuchElementException):
            print("No see more buttons")
            expandBtn = ''
        
        if expandBtn != '':
            for btns in expandBtn:
                btns.click()
      
        #Get current company
        for i in expHeading:
            spans = i.find_elements_by_tag_name('span')
            for idx, j in enumerate(spans):
                if idx % 2:
                    print(idx,j.text)
                    current.append(j.text)
                else:
                    pass
        
        currentCompany=current[0]
        totalDuration=current[1]

        #Current Positions
        curExp = {}
                   
        #Current Position Dates
        Role=''
        Date=''
        StartDate=''
        EndDate=''
        Duration=''
        Description=''
        Location=''
        experienceNow=''
        experience =''

        #Selectors
        cRoleElem = 'h3.t-14.t-black.t-bold'
        prevRoleElem = 'h3.t-16.t-black.t-bold'
        entityElem = 'p.pv-entity__secondary-title.t-14.t-black.t-normal'
        dateElem = 'h4.pv-entity__date-range.t-14.t-black--light.t-normal'
        durationElem = 'span.pv-entity__bullet-item-v2'
        descriptionElem = 'p.pv-entity__description.t-14.t-black'
        localeElem =' h4.pv-entity__location.t-14.t-black--light.t-normal.block'
        
        #Filters
        spanFilter=('span:not(.visually-hidden)')
        experienceNow = experienceBody.find_element_by_class_name('pv-entity__position-group')
        experience = experienceNow.find_elements_by_xpath(".//li")
                
        for idx, curExperience in enumerate(experience):
            curRoles = curExperience.find_elements_by_css_selector(cRoleElem)
            curDates = curExperience.find_elements_by_css_selector(dateElem)
            curDurations = curExperience.find_elements_by_css_selector(durationElem)
            curDescriptions = curExperience.find_elements_by_css_selector(descriptionElem)
            
            curLocations = curExperience.find_elements_by_css_selector(localeElem)
            
            
            for curRole, curDate, curDuration in zip(curRoles,curDates, curDurations):
                curRoleSpans =  curRole.find_elements_by_css_selector(spanFilter)
                curDateSpans =  curDate.find_elements_by_css_selector(spanFilter)
                Duration = curDuration.text
                
                for (role, at) in zip(curRoleSpans, curDateSpans):
                    Role = role.text
                    Date = at.text.split(' – ')
                    
                    if Date !='':
                        StartDate = Date[0]
                        EndDate = Date[1]
                    
                    else:
                        StartDate=''
                        EndDate=''
                    
            for curDescription in curDescriptions:
                Description = curDescription.text
                print(Description)
            
            for curLocation in curLocations:
                curlocationSpans = curLocation.find_elements_by_css_selector(spanFilter)
                
                for location in curlocationSpans:
                    Location = location.text
                    print(Location)

            curExp ['Position-'+str(idx)] = {
                'Company': currentCompany,
                'Title': Role,
                'StartDate': StartDate,
                'EndDate':  EndDate,
                'Duration': Duration,
                'Description': Description,
                'Location': Location
                
                }
            
        
        #Past Experience
        experienceWrap =''
        experienceWrap = driver.find_element_by_xpath('//*[@id="experience-section"]')
        #Expand Past Experience:
        expandChevron=''
        try:
            expandChevron = experienceWrap.find_elements_by_css_selector("button.pv-profile-section__see-more-inline.pv-profile-section__text-truncate-toggle.link.link-without-hover-state")
            
        except (NoSuchElementException):
            print("No see more buttons")
            expandChevron = ''
            
        if expandChevron != '':
            for chevs in expandChevron:
                chevs.click()
                
        #Get past experience
        prevExp =  {}
        Role=''
        Date=''
        StartDate=''
        EndDate=''
        Duration=''
        Description=''
        Location=''
        prevExperience=''
        try:
            prevExperience = experienceBody.find_elements_by_xpath(".//li")
            Ids = []
            for i in prevExperience:
                ids = i.get_attribute('id')
                if ids != '':
                    Ids.append(ids)
    
            for idx,i in enumerate(Ids[1:]):
                prevExperiences = experienceBody.find_elements_by_id(i)
                
                for experience in prevExperiences:

                    prevRoles = experience.find_elements_by_css_selector(prevRoleElem)
                    prevCompanies= experience.find_elements_by_css_selector(entityElem)
                    prevDates = experience.find_elements_by_css_selector(dateElem)
                    prevDurations = experience.find_elements_by_css_selector(durationElem)
                    prevDescriptions = experience.find_elements_by_css_selector(descriptionElem)
                    prevLocations = experience.find_elements_by_css_selector(localeElem)
                     
                    for (prevRole,prevCompany,prevDate, prevDuration) in zip(prevRoles,prevCompanies, prevDates, prevDurations):
                        prevDateSpans =  prevDate.find_elements_by_css_selector(spanFilter)
                        print(prevRole.text)
                        print(prevCompany.text)
                        Role = prevRole.text
                        Company = prevCompany.text
                        Duration = prevDuration.text
                        
                        for date in prevDateSpans:
                            print(date.text)
                            Date = date.text.split(' – ')
                                
                            if Date !='':
                                StartDate = Date[0]
                                EndDate = Date[1]
                                
                            else:
                                StartDate=''
                                EndDate=''
                                        
                    for prevDescription in prevDescriptions:
                        Description = prevDescription.text
                        print(Description)
            
                    for prevLocation in prevLocations:
                        locationSpans = prevLocation.find_elements_by_css_selector(spanFilter)
                
                        for location in locationSpans:
                            Location = location.text
                            print(Location)
                            
                            
                    
                    prevExp['Position-'+str(idx)] = {
                            'Company': Company,
                            'Title': Role,
                            'StartDate': StartDate,
                            'EndDate':  EndDate,
                            'Duration': Duration,
                            'Description': Description,
                            'Location': Location
                            }
            
                        
                  
      
        
        except (NoSuchElementException):
            print("Element not found")
            
        #Education
        educ = {}
        Degrees = {}
        Field = {}
        #Selectors
        eduCSS = 'div.pv-entity__summary-info.pv-entity__summary-info--background-section'
        eduElems = 'div.pv-entity__degree-info'
        schoolElems = 'h3.pv-entity__school-name'
        degreeElems = 'p.pv-entity__secondary-title.pv-entity__degree-name'
        fosElems = 'p.pv-entity__secondary-title.pv-entity__fos'
        dateElems = 'p.pv-entity__dates'
        #Filter
        spanSelect = 'span.pv-entity__comma-item'
        spanFilter=('span:not(.visually-hidden)')
        datesFilter = 'time'
        educations = driver.find_element_by_id('education-section')
        
        #Profile Body
        #Expand Education
        certBtnElem = 'button'
        showMoreEduc = 'button.pv-profile-section__see-more-inline.pv-profile-section__text-truncate-toggle'
        certBtns=''
        try:
            certBtns = educations.find_elements_by_css_selector(certBtnElem)
            if not  certBtns:
                if not  certBtns:
                    print('No Elements found')
                    certBtns =''
            else:    
                for certBtn in certBtns:
                    print( certBtn.text)
                
        except (NoSuchElementException):
            print("No see more buttons")
            certBtns = ''
       
        if certBtns !='':
           certBtn = wait.until(EC.element_to_be_clickable((By.CSS_Selector, showMoreEduc)))
           certBtn.click()
        
        #Init Education search
        eduClasses = ''
        eduClasses = educations.find_elements_by_css_selector(eduCSS)
        for idxClass,eduClass in enumerate(eduClasses):
            education = eduClass.find_elements_by_css_selector(eduElems) 
            eduDates = eduClass.find_elements_by_css_selector(dateElems)
            
            
            for idx,(eduItems,eduTimes) in enumerate(zip(education,eduDates)):
                schools = eduItems.find_elements_by_css_selector(schoolElems)
                degrees = eduItems.find_elements_by_css_selector(degreeElems)
                fields = eduItems.find_elements_by_css_selector(fosElems)

                for idxS,school in enumerate(schools):
                    print(idx,school.text)
                    school = school.text
                    
                    for program in degrees:
                        degSpan = program.find_elements_by_css_selector(spanFilter)
                    
                    for deg in degSpan:
                        degree=deg.text
                        print(idx,degree)
                
                    for field in fields:
                        fieldSpan = field.find_elements_by_css_selector(spanFilter)
                    
                        for fos in fieldSpan:
                            Field=fos.text
                            print(idx,Field)
                            
                    Degrees['Degree'+str(idx)] = {
                        'Degree': degree,
                        'FieldofStudy':Field
                        }
                
        
                schoolDates = eduTimes.find_elements_by_css_selector(spanFilter)                
                for attendance in schoolDates:
                    if attendance.text != '':
                        print(attendance.text)
                        attendanceStr = attendance.text.split(' – ')
                        if attendanceStr !='':
                            StartAt = attendanceStr[0]
                            EndAt = attendanceStr[1]
                            print(StartAt)
                            print(EndAt)
                            
                        else:
                            StartAt=''
                            EndAt=''
                            
            educ['Education-'+str(idx)] = {
                    'School': school,
                    'Degrees': degree,
                    'FieldofStudy':Field,
                    'StartAt': StartAt,
                    'EndAt': EndAt
             }
        
        
        #License and Certification
        
        #Elements
        
        certifs= {}
        certificationBody=''
        certElems = 'li.pv-profile-section__sortable-item.pv-certification-entity.ember-view'
        certElem = 'h3'
        issuedByElem = 'p'
        certificationBody = ''
        certList= ''
        certificationBody = driver.find_element_by_id('certifications-section')
        certList = certificationBody.find_elements_by_css_selector(certElems)
        
        
        for idxCert,certifications in enumerate(certList):
            certification = certifications.find_elements_by_css_selector(certElem)
            issuedBy = certifications.find_elements_by_css_selector(issuedByElem)
            for certs in certification:
                cert = certs.text
            for idxBody,issueBody in enumerate(issuedBy):                
                issuedSpan = issueBody.find_elements_by_css_selector(spanFilter)
                for idxIssuer,issuer in enumerate(issuedSpan):
                    if idxBody==0 and idxIssuer==0:
                        institute=issuer.text
                        print(institute)
                    elif (idxBody==1 and idxIssuer==0):
                        issueAt = issuer.text[0:11]
                        print(issueAt)
                    elif (idxBody==1 and idxIssuer==1):
                        validAt= issuer.text
                        print(validAt)
                        
            certifs['certification-'+str(idxCert)] = {
                'Certification': cert,
                'IssuedBy': institute,
                'IssueAt': issueAt,
                'validAt': validAt
                    }

        #Skills Endorsements
        skillsBodyElem = 'section.pv-profile-section.pv-skill-categories-section'
        btnSkillsElem = 'button.pv-profile-section__card-action-bar.pv-skills-section__additional-skills'
        try:
            skillsBody = driver.find_element_by_css_selector(skillsBodyElem)
        
            try:
                btnSkills = skillsBody.find_elements_by_css_selector(btnSkillsElem)
                if not  btnSkills:
                        print('No Elements found')
                        btnSkills =''
                else:    
                    for btnSkills in btnSkills:
                        print( btnSkills.text)
            
            except (NoSuchElementException):
                print("No see more buttons")
                btnSkills = ''
                break
            
            if btnSkills !='':
                btnSkills = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, btnSkillsElem)))
                btnSkills.click()
        
        
            #Skills selector:
            Skills={}
            skillsElem = 'span.pv-skill-category-entity__name-text'
            skillsWrapper = 'div.pv-skill-category-entity__skill-wrapper'
            endorseElem = 'span.pv-skill-category-entity__endorsement-count'
            #Get top skills
            skillsWrap = ''
            skillsWrap = driver.find_elements_by_css_selector(skillsWrapper)
            for idxItems,skillsList in enumerate(skillsWrap):
                skills = skillsList.find_elements_by_css_selector(skillsElem)
                endorses = skillsList.find_elements_by_css_selector(endorseElem)
            
                for idxSkills,Skill in enumerate(skills):
                    skill = Skill.text
            
                endorse='0'
                for idxEndorse,Endorse in enumerate(endorses):
                    endorse = Endorse.text
                    if endorse ==' ':
                        endorse=0
                    else:
                        endorse
            
                print(idxItems,idxSkills,idxEndorse,skill,endorse)
        
                Skills['Skill-'+str(idxItems)] = {
                'Skill': skill,
                'Endorsement': endorse
                    } 
                 
        except (NoSuchElementException):
            print("No skills body text")
            Skills = ''
        
        #Recommendations:
        elemRec = 'button.ml0.artdeco-tab.active.artdeco-tab--selected.ember-view'
        
        try:
            recNum = driver.find_element_by_css_selector(elemRec)
            rec =  re.search(r'\((.*?)\)',recNum.text).group(1)
        except (NoSuchElementException):
            print('No recommendations found')
            rec = ''
            
        #Accompolishments
        #accomplishment selectors
        accomBody = ''
        accompBodyClass = 'section.pv-profile-section.pv-accomplishments-section.artdeco-container-card.ember-view'
        accompClass = 'section.pv-profile-section.pv-accomplishments-block'
        accompCountClass = 'h3.pv-accomplishments-block__count'
        accompTitleClass = 'h3.pv-accomplishments-block__title'
        accompListContent = 'section.pv-accomplishments-block__content.pv-accomplishments-block--expanded'
        accompListClass = 'li.pv-accomplishment-entity'
        accompItemTitle = 'h4.pv-accomplishment-entity__title'
        #language selector
        langProfClass = 'p.pv-accomplishment-entity__proficiency'
        #publication selectors
        pubEntityClass = 'p.t-14'
        pubIssuerClass = 'span.pv-accomplishment-entity__publisher'
        pubDateClass = 'span.pv-accomplishment-entity__date'
        pubDescriptionClass = 'p.pv-accomplishment-entity__description'
        
        #hone & award selector
        entityIssuerClass = 'span.pv-accomplishment-entity__issuer'
        
        #organization selectors
        positionClass ='span.pv-accomplishment-entity__position'
        
        #button selector
        accompBtnClass = 'button.pv-accomplishments-block__expand'

        #Dictionaries
        accsDct = {}
        accDct = {}
        accpDct = {}
        #Expand accomplishment body
        
        try:
            #get acommplishment Ids
            
            accompBody = driver.find_element_by_css_selector(accompBodyClass)
            accompIds= accompBody.find_elements_by_css_selector(accompClass)
            accompIdList = []
            for i in accompIds:
                ids = i.get_attribute('id')
                if ids != '':
                    accompIdList.append(ids)
            
            for idx,accompSecId in enumerate(accompIdList):
                profDct = {}
                
                accompItems = accompBody.find_element_by_id(accompSecId)
                accbtn = accompItems.find_element_by_css_selector(accompBtnClass)
                accbtn.click()
                accompTitle = accompItems.find_element_by_css_selector(accompTitleClass)
                accompCountItem = accompItems.find_element_by_css_selector(accompCountClass)
                accompList = accompItems.find_elements_by_css_selector(accompListClass)
                
                Accomplishment = accompTitle.text
                for idxAcc,accompEntity in enumerate(accompList):                
                    itemTitle = accompEntity.find_element_by_css_selector('span.visually-hidden')
                    accTitle = itemTitle.text
                    aTitle = accompEntity.find_elements_by_css_selector(accompItemTitle)
                    
                   
                    
                    for idxItem,accompItem in enumerate(aTitle):
                        accomp = driver.execute_script("return arguments[0].innerHTML;", accompItem)
                        accomp = (accomp.partition("</span>")[2]).strip()
                        print(idx,idxItem,idxAcc,accomp)
                        print(accTitle)
                    
                    
                    if Accomplishment == 'Languages':
                        profs = accompEntity.find_elements_by_css_selector(langProfClass)
                        for idxProf,proficiency in enumerate(profs):
                            print(idx,idxItem,idxAcc,idxProf,proficiency.text)
                            prof = proficiency.text
                            
                            profDct = {
                            'Proficiency': prof
                            }
                            print(profDct)
                            
                    elif Accomplishment == 'Publications': 
                        pubItems = accompEntity.find_elements_by_css_selector(pubEntityClass)
                        pubDescriptions = accompEntity.find_elements_by_css_selector(pubDescriptionClass)
                        description = ''
    
                        for pubs in pubItems:
                            pubIssuers = pubs.find_elements_by_css_selector(pubIssuerClass)
                            pubDates = pubs.find_elements_by_css_selector(pubDateClass)
                            
                            for idxPub, issuers in enumerate(pubIssuers):
                                issuer = ''
                                issuer = driver.execute_script("return arguments[0].innerHTML;", issuers)
                                issuer = (issuer.partition("</span>")[2]).strip()
                                print(idx,idxAcc, idxPub,issuer)
                        
                            for idxPub, pubDate in enumerate(pubDates):
                                date = ''
                                date = driver.execute_script("return arguments[0].innerHTML;", pubDate)
                                date = (date.partition("</span>")[2]).strip()
                                print(date) 
                            
                            for idxPub, pubDescription in enumerate(pubDescriptions):
                                description = driver.execute_script("return arguments[0].innerHTML;", pubDescription)
                                description = (description.partition("</span>")[2]).strip()
                                print(description) 
                            
                            profDct = {
                                
                                'Issuer': issuer,
                                'Date': date,
                                'Description': description
                                }
                            
                    elif Accomplishment == 'Honor & Award': 
                        institutes = accompEntity.find_elements_by_css_selector(entityIssuerClass)
                        for idxProf,institute in enumerate(institutes):
                             inst = driver.execute_script("return arguments[0].innerHTML;", institute)
                             inst = (inst.partition("</span>")[2]).strip()
                            
                        profDct = {
                        'Institute': inst
                        }
                        print(profDct)
    
                    
                    elif Accomplishment == 'Organization': 
                        pubItems = accompEntity.find_elements_by_css_selector(pubEntityClass)
                        pubDescriptions = accompEntity.find_elements_by_css_selector(pubDescriptionClass)
                        description = ''
    
                        for pubs in pubItems:
                            orgPosition = pubs.find_elements_by_css_selector(positionClass)
                            orgDates = pubs.find_elements_by_css_selector(pubDateClass)
                            
                            for idxPub, positions in enumerate(orgPosition):
                                position = ''
                                position = driver.execute_script("return arguments[0].innerHTML;", positions)
                                position = (position.partition("</span>")[2]).strip()
                                print(idx,idxAcc, idxPub,issuer)
                        
                            for idxPub, orgDate in enumerate(orgDates):
                                date = ''
                                date = driver.execute_script("return arguments[0].innerHTML;", orgDate)
                                date = (date.partition("</span>")[2]).strip()
                                print(date) 
    
                        profDct = {
                        'Position': position,
                        'JoinAt': date
                        }
                        print(profDct)
                           
                    accDct[Accomplishment+' '+str(idxAcc+1)] = {
                        accTitle+' '+str(idxItem+1): accomp,
                        'Info' : profDct
                        }
                 
        except (NoSuchElementException):
            print('No accomplishments found!')
            accDct = {}
        
        
        #Interests
        intDct={}    
        #Interest Selectors
        intSectionClass='section.pv-profile-section.pv-interests-section.artdeco-container-card.ember-view'
        intModalClass='div.artdeco-modal-overlay'
        intSecModalClass='//li[contains(@class, "pv-interests-modal__following")]'
        #List item selector
        intWrap = 'div.entity-list-wrapper'
        intItem = 'h3.pv-entity__summary-title'
        secBtnClass = 'a.pv-profile-section__card-action-bar'
        

        try:
            intBody = driver.find_element_by_css_selector(intSectionClass)
        
            try:
                secBtn = intBody.find_element_by_css_selector(secBtnClass)
                if not  secBtn:
                        print('No Elements found')
                        secBtn =''
         
            except (NoSuchElementException):
                print("No see more buttons")
                secBtn = ''
                
            
            if secBtn !='':
                secBtn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, secBtnClass)))
                secBtn.click()
                
                modalBody = driver.find_element_by_css_selector(intModalClass)
                secControls = modalBody.find_elements_by_xpath(intSecModalClass)
                for secTab in secControls:
                    secTab.click()
                    intWrapper = modalBody.find_elements_by_css_selector(intWrap)
                    intClass = secTab.text
                    for idxInt,interests in enumerate(intWrapper):
                        interest = interests.text
                        print(idxInt,interest)
                
                    intDct[intClass] = {
                    
                    'Interest '+str(idxInt): interest
                    
                    
                    }
                    
            print(intBody.text)
        except (NoSuchElementException):
            print('No interest body found!')
            intDct = {}

        profile = {
            'Id' : Id,
            'Name': name,
            'Role': title,
            'About': about,
            'ImgUrl': img,
            'Company': currentCompany,
            'Duration': totalDuration,
            'CurExperience': curExp,
            'PrevExperience': prevExp,
            'Education': educ,
            'Certification': certifs,
            'Skills': Skills,
            'Recommendations': rec,
            'Accomplishments': accDct
            }

        profiles[Id] = profile
        print(profiles)
        
    except TimeoutException:
        print("Failed to load")
        break



