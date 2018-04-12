from urllib.request import urlopen
from urllib.request import urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import random
import re
import sys

"""
get BeautifulSoup object first as bsObj
usage.1.
    Navigation Tree
    .parent
    .previous_sibling[s]
    .next_sibling[s]
    .children
    ..
    bsObj.tag.subTag.anotherSubTag
    e.g.=>
        bsObj.html.body.h1
usage.2.
    bsObj.find(tag,attributes) or bsObj.findAll(tag,attributes)
    e.g.=>
        bsObj.findAll("a", {"class": "s xst"})
        bsObj.findAll({"h1","h2","h3","h4","h5","h6"})
        bsObj.findAll("span", {"class":"green", "class":"red"})
"""

baseurl = "https://bbs.hupu.com"
starturl = "/bxj"
picset = set()
urlset = set(starturl,)
picfile = r"C:\Users\apple\Desktop\hupupic"
nxlist = []

def getbsObj(url):
    try:
        html = urlopen(baseurl+url)
        return BeautifulSoup(html, "lxml")
    except HTTPError as e:
        print(e, baseurl+url)


def downloadpic(url, bsObj):
    print("start scrape img==>", url)
    i = 0
    prefix = url[:-5]
    for img in bsObj.body.findAll(lambda tag: tag.name == "img" and "src" in tag.attrs and "data-h" in tag.attrs and "data-w" in tag.attrs):
        try:
            src = img.attrs["src"].split("?")[0]
            if "placeholder" in src:
                src = img.attrs["data-original"].split("?")[0]
            if src not in picset:
                picset.add(src)
                picname = prefix +"_" + str(i)
                if src.endswith(".jpg") or src.endswith(".png") or src.endswith(".gif"):
                    picname = picname + src[-4:]
                if picname[-4] != '.':
                    picname = picname + ".jpg"
                urlretrieve(src, picfile+"\\"+picname)
                print("download==>", picname)
                i += 1
        except IOError as e:
            print(e)
    print("end scrape img==>", url, "|", str(i), "iamges")



def setNextUrlList(url, bsObj):
    urls = []
    for cot in bsObj.body.findAll(lambda tag: tag.name == "a" and "href" in tag.attrs):
        src = cot.attrs["href"]
        if src and src not in urlset and src[0] == '/' and src[-5:] == ".html":
            urls.append(src)
    if not urls:
        print("final url=>", url)
        sys.exit(1)
    global nxlist
    nxlist = urls


def getNextUrl():
    if not nxlist:
        print("exhausted nxlist")
        sys.exit(1)
    nx = random.choice(nxlist)
    nxlist.remove(nx)
    urlset.add(nx)
    return nx

if __name__ == '__main__':
    nx = starturl
    while len(picset) < 100:
        bsObj = getbsObj(nx)
        while not bsObj:
            nx = getNextUrl()
            bsObj = getbsObj(nx)
        downloadpic(nx, bsObj)
        setNextUrlList(nx, bsObj)
        nx = getNextUrl()

