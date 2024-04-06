from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import ssl

'''
def getSoup(url: str) -> BeautifulSoup:
    
    proxy_addresses = {
        'http': 'http://72.206.181.123:4145',
        'https': 'http://191.96.100.33:3128'
    }

    context = ssl._create_unverified_context()
    res = urlopen(url, context = context, )
    bs = BeautifulSoup(res, "html.parser")
    res.close()
    
    return bs

'''

# TODO: find way to automate curling process (need to update textfile every day)
def getSoup(path: str, file: str) -> BeautifulSoup:

    data = open(path + file, "r")
    bs = BeautifulSoup(data, "html.parser")
    data.close()

    return bs