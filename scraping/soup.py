from bs4 import BeautifulSoup
import requests
from urllib.request import urlopen
import ssl



def getSoup(url: str) -> BeautifulSoup:
    context = ssl._create_unverified_context()
    res = urlopen(url,
              context=context)
    bs = BeautifulSoup(res, "html.parser")
    res.close()
    
    return bs