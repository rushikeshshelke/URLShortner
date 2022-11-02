import json
import os

from commonLibs.globalVariables import GlobalVariables

class CommonConfigs:

    def createDir(self,path):
        if os.path.isdir(path) == False:
            os.makedirs(path)
    
    def readJson(self,filename):
        with open(filename,'r') as file:
            return json.load(file)

    def checkURLExists(self, originalURL, current_app):
        resultDict = {}

        if originalURL in GlobalVariables.CACHE_DATA:
            resultDict['original'] = originalURL
            resultDict['shorten'] = GlobalVariables.CACHE_DATA[originalURL]
        else:
            urlData = [
            (
                entries['originalURL'],
                entries['shortenURL']
            )
            for entries in current_app.db.urlshortner.find({"originalURL":originalURL})
        ]
            GlobalVariables.LOGGER.info("MongoDB content : {}".format(urlData))
            if urlData:
                resultDict['original'] = urlData[0][0]
                resultDict['shorten'] = urlData[0][1]
            GlobalVariables.LOGGER.info("Result dict : {}".format(resultDict))
        
        return resultDict
    
    def insertIntoDB(self, originalURL, shortenURL, current_app):

        #Store url in cache
        if len(GlobalVariables.CACHE_DATA) < 10:
            GlobalVariables.CACHE_DATA[originalURL] = shortenURL
        else:
            # remove very first element from order dict
            GlobalVariables.CACHE_DATA.popitem(last=False)
            GlobalVariables.CACHE_DATA[originalURL] = shortenURL

        current_app.db.urlshortner.insert_one({"originalURL":originalURL,"shortenURL":shortenURL})
    
    def getExistingURLIDS(self, current_app):

        urlids = [
            (
                entries['urlid']
            )
            for entries in current_app.db.urlids.find({})
        ]

        GlobalVariables.LOGGER.info("url id's : {}".format(urlids))
    
        return urlids