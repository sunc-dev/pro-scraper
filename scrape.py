   # -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 21:05:27 2020
    
@author: csunj
    """
    
try:
 
    from selenium.common.exceptions import TimeoutException
    import sys
    import json
        
    sys.path.append(r'C:\Users\csunj\Downloads\getPhotos')
    from initials import loadData
    from driver import initDriver
    from persons import Person as pr
    from persons import About as ab
    from jobs import Job as jb
    from schools import School as sc
    from volunteers import Volunteer as vr
    from certs import Cert as cr
    from skills import Skill as sk
    from refs import Ref as rf
    from feats import Feat as ft
    from interests import Interest as it

except Exception as e:
    print("Some Modules are Missing {}".format(e))

class Profile(object):
    def __init__(self, Id=None, persons=None, abouts=None, jobs=None, schools=None, volunteers=None, certs=None, skills=None, refs=None, feats=None, interests=None):    
        
        self.Id = Id
        self.persons = persons
        self.abouts = abouts
        self.jobs = jobs
        self.schools = schools
        self.volunteers = volunteers
        self.certs = certs
        self.skills = skills
        self.refs = refs
        self.feats = feats
        self.interests = interests
        
    
    def get_profile(self):
        
        profile_dict = {
            
             
                'Id':self.Id, 
                'Info':{
                    'Persons': self.persons,
                    'About': self.abouts,
                    'Jobs': self.jobs,
                    'School': self.schools,
                    'Volunteer': self.volunteers,
                    'Certificatons': self.certs,
                    'Skills': self.skills,
                    'References': self.refs,
                    'Feats': self.feats,
                    'Interests': self.interests
                    }
                
            }
        
        return profile_dict
        
    def Urls(self):
        init = loadData()
        csv = init.getData('result.csv')
        url = init.getUrls(csv)
            
        return url
        
    def Scrape(self):  
        
        
        d, wait, event = initDriver()
        urls = Profile.Urls(self)
        
        Profiles = []
        
        for url in urls:
            try:
                
                d.get(url[1])
                
                self.Id = url[0]
                self.persons = pr.get_profileCard(pr, url, d, wait)
                self.abouts = ab.get_about(ab, url, d, wait)
                self.jobs = jb.get_jobs(jb, url, d, wait)
                self.schools = sc.get_school(sc,url,d,wait)
                self.volunteers = vr.get_volunteer(vr, url, d, wait)
                self.certs = cr.get_cert(cr, url, d, wait)
                self.skills = sk.get_skill(sk, url, d, wait)
                self.refs = rf.get_ref(rf, url, d, wait)
                self.feats= ft.get_feat(ft,url,d,wait)
                self.interests = it.get_interest(it,url,d,wait)
                
                
                
            except (TimeoutException):
                print("Error in profile")
            
            profile = Profile.get_profile(self)
            Profiles.append(profile)
                
                
            
            
        return Profiles,profile,urls
                
            
        #d.close()
    
if __name__ == '__main__':
    pro = Profile()
    url = pro.Urls()
    Profiles,profile,urls = Profile.Scrape(pro)

    dataJson = json.dumps(Profiles)
    with open('data.txt', 'w') as outJson:
        json.dump(dataJson, outJson)
