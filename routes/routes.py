import string
import os

from random import choices
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app
from commonLibs.globalVariables import GlobalVariables
from commonLibs.commonConfigs import CommonConfigs
from dotenv import load_dotenv

pages = Blueprint("urlshortner",__name__,template_folder="templates")
load_dotenv()
localHost = os.environ.get("LOCAL_HOST")

@pages.route("/", methods=["GET","POST"])
def shortenURL():
    GlobalVariables.LOGGER.info("Inside url shortner home page.")
    resultDict = {}
    
    if request.method == "POST":
        originalURL = request.form.get("longURL")

        GlobalVariables.LOGGER.info("Original URL : {}".format(originalURL))

        if originalURL == "":
            flash("Invalid URL!!!")
            return redirect(url_for("urlshortner.shortenURL"))
        
        resultDict = CommonConfigs().checkURLExists(originalURL,current_app)

        if len(resultDict) > 0:
            GlobalVariables.LOGGER.info("Shorten URL already exists : {}".format(resultDict))
            resultDict['localhost'] = localHost
            return render_template("shortenURL.html", URL_LIST=resultDict)

        characters = string.digits + string.ascii_letters

        urlids = CommonConfigs().getExistingURLIDS(current_app)
        
        GlobalVariables.LOGGER.info("Existing url ids : {}".format(urlids))
        
        while True:
            urlid = ''.join(choices(characters,k=6))
            
            if len(urlids) == 1:
                if urlid not in urlids[0]:
                    shortenURL = "{}/{}".format(GlobalVariables.HOST_URL,urlid)
                    break
            else:
                shortenURL = "{}/{}".format(GlobalVariables.HOST_URL,urlid)
                break
        
        # insert urlid
        current_app.db.urlids.insert_one({"urlid":urlid})

        resultDict['original'] = originalURL
        resultDict['shorten'] = shortenURL
        resultDict['localhost'] = localHost

        GlobalVariables.LOGGER.info("Shorten URL for original one {} is {}".format(originalURL, shortenURL))
        CommonConfigs().insertIntoDB(originalURL,shortenURL,current_app)

        return render_template("shortenURL.html", URL_LIST=resultDict)

    return render_template("base.html")

@pages.route("/<host>/<id>",methods=["GET"])
def redirectToOriginalURL(host,id):
    shortenURL = "{}/{}".format(host,id)
    GlobalVariables.LOGGER.info("Inside redirect, shortenURL : {}".format(shortenURL))
    load_dotenv()
    urlDATA = [
        (
            entries['originalURL'],
            entries['shortenURL']
        )
        for entries in current_app.db.urlshortner.find({"shortenURL":shortenURL})
    ]

    if len(urlDATA) == 0:
        flash("Invalid URL '{}{}' Could not redirect!!!".format(localHost,shortenURL))
        return redirect(url_for("urlshortner.shortenURL"))
    
    GlobalVariables.LOGGER.info("Redirecting to {} by using {}".format(urlDATA[0][0],urlDATA[0][1]))
    
    return redirect(urlDATA[0][0])