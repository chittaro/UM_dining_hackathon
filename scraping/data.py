from scrape import *
from utils.funcs import *
import importlib
import pandas as pd
import os


diction = getStartDict()
halls = getDHalls()

path = "scraping/hall_HTML/"
dir_list = os.listdir(path)
dir_list

for dir in dir_list:
    getDhallItems(dir, diction)

diningDf = pd.DataFrame(diction)

print(diningDf)