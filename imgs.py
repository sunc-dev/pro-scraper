# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 15:20:13 2020

@author: csunj
"""
try:
    
    import json
    import pandas as pd
    from flatten_json import flatten 
    import urllib
    import os
except Exception as e:
    print("Some Modules are Missing {}".format(e))


def get_image():
    with open('data.txt') as inJson:
        jsonString = json.load(inJson)
        
    data = json.loads(jsonString)
    
    Data  = []   
    for i in data:
        x = flatten(i) 
        Data.append(x)
        
    keyImg = 'Info_Persons_ImgUrl'
    keyName = 'Info_Persons_FullName' 
    noPic = 'data:image/gif' 
    Imgs =[]
    
    for profile in Data:
        imgUrl = profile.get(keyImg)
        Name = profile.get(keyName)
        item = [Name, imgUrl]
        Imgs.append(item)
        
    for img in Imgs:
        name = img[0]
        imgUrl = img[1]
        if noPic in imgUrl:
            imgUrl = ''
        else:
            imgUrl
        if imgUrl != '':
            urllib.request.urlretrieve(imgUrl,
                                       os.path.join('img',name) + '.jpeg')