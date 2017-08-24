from __future__ import absolute_import
from test_celery.celery import app
from celery.utils.log import get_task_logger
from celery import chain
import time,requests
from pymongo import MongoClient
from bs4 import BeautifulSoup as bs4
from traceback import format_exc
import time
machineIP = "172.16.0.5"
logger = get_task_logger(__name__)
client = MongoClient(machineIP, 27017) # change the ip and port to your mongo database's
db = client.mongodb_test
collection = db.celery_test
post = db.test

@app.task(bind=True, default_retry_delay=5) # set a retry delay, 10 equal to 10s
def articleParsing(self, url):
    try:
        urlID = url.strip().split("/")[-1]
        r = requests.get(url, verify=False)
        logger.info("Parse url{}".format(url))
        articleHtml = r.content.decode("utf-8", "ignore")
        articlePage = bs4(articleHtml)
    except Exception as exc:
        raise self.retry(exc=exc)
    try:
        text = articlePage.find("div", id="main-content").text
        author = articlePage.findAll("span", class_="article-meta-value")[0].text
        label = articlePage.findAll("span", class_="article-meta-value")[1].text
        title = articlePage.findAll("span", class_="article-meta-value")[2].text
        date = articlePage.findAll("span", class_="article-meta-value")[3].text
        # store status code and current time to mongodb
        post.insert({'url':urlID,
                    "title":title,
                    "label":label,
                    "author":author,
                    "date":date,
                    "text":text,
                    "stamp":int(time.time())})
    except:
        logger.error(format_exc())
    return r.status_code

@app.task(bind=True, default_retry_delay=10) # set a retry delay, 10 equal to 10s
def pageParsing(self, url):
    try:
        r = requests.get(url, verify=False)
        pageHtml = r.content.decode("utf-8", "ignore")
        parsedPage = bs4(pageHtml)
        urls = ["https://www.ptt.cc{}".format(a["href"]) 
                for a in parsedPage.find_all("a", class_=None)[1::]]
        for url in urls:
            articleParsing.delay(url)
        
    except Exception as exc:
        raise self.retry(exc=exc)
    return r.status_code

