# -*- coding: utf-8 -*-
"""
Created on Thu Jul 23 13:25:31 2020

@author: csunj
"""
try:
    import os
    import pandas as pd
    import uuid
    
except Exception as e:
    print("Some Modules are Missing {}".format(e))


class Path():            
    def __init__(self):
       self.root = r'C:\Users\csunj\Downloads\getPhotos'
       self.folder = os.path.join(self.root,'master')

    def pathItems(self):
        return self.root, self.folder
    
class loadData():
    
    def __init__(self):
        self.Id = 'Id'
        self.url = 'profileUrl'
        
    def getData(self, data):
        root, folder = Path().pathItems()
        raw = pd.read_csv(os.path.join(root,folder,data))
        return raw

    def getUrls(self, raw):
        raw = raw.dropna(subset=[self.url])
        raw[self.Id] = [str(uuid.uuid4()) for _ in range(len(raw.index))]
        urls = (raw[[self.Id,self.url]].values.tolist())
        urls = urls[:40]
        return urls


if __name__ == '__main__':
    
    urls = loadData().getData('result.csv')