"""
MatMasIt, Apf0x

For all the weebs out there

2021, MIT License

"""

import unicodedata
import re
import urllib.request
import requests
from bs4 import BeautifulSoup
import pathlib

def getImages(galleryUrl,title,iteration,total):
    flag = True
    i = 1
    while flag:
        response = requests.get(galleryUrl+"/"+str(i)+".jpg")
        if response.status_code!=200:
            flag = False
            break
        printProgressBar(iteration, total, i, title)
        pathlib.Path("downloaded/"+slugify(title)).mkdir(parents=True, exist_ok=True)
        file = open("downloaded/"+slugify(title)+"/"+str(i)+".jpg", "wb+")
        file.write(response.content)
        file.close()
        i+=1
def getDataByUrl(url,iteration,total):
    url += "1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}
    request = urllib.request.Request(url, None, headers)  # The assembled request
    try:
        response = urllib.request.urlopen(request)
    except:
        return False
    data = response.read()
    soup = BeautifulSoup(data, 'html.parser')
    title = soup.find('title')
    titleR=title.string.split("- Page 1 » nhentai: hentai doujinshi and manga")[0].strip()
    a=soup.find("img", src=lambda value: value and value.startswith("https://i.nhentai.net/galleries/"))
    listS=a.get("src").split("/")
    galleryUrl=""
    for i in range(len(listS)-1):
        if i!= 0:
            galleryUrl+="/"
        galleryUrl+=listS[i]
    print("")
    printProgressBar(iteration,total,"",titleR)
    getImages(galleryUrl,titleR,iteration,total)
def slugify(value, allow_unicode=True):
    """
    Taken from https://github.com/django/django/blob/master/django/utils/text.py
    Convert to ASCII if 'allow_unicode' is False. Convert spaces or repeated
    dashes to single dashes. Remove characters that aren't alphanumerics,
    underscores, or hyphens. Convert to lowercase. Also strip leading and
    trailing whitespace, dashes, and underscores.
    """
    value = str(value)
    if allow_unicode:
        value = unicodedata.normalize('NFKC', value)
    else:
        value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value.lower())
    return re.sub(r'[-\s]+', '-', value).strip('-_')
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()
def main():
    # Use a breakpoint in the code line below to debug your script.
    urls = open("urls.txt","r").readlines()
    i=1
    total=len(urls)
    for url in urls:
        getDataByUrl(url.strip(),i,total)
        i+=1



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


