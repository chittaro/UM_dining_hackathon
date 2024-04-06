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
    getDhallItems(path, dir, diction)

diningDf = pd.DataFrame(diction)

#print(diningDf)

#pull from "menu items" if it says "vegan" in the name
#pass a list? of keys? 
dining_hall = "temp"

def vegan_options(diningDf, dining_hall):
    #find a way to sift by dhall and only return items in that dhall
    vegan_ops = diningDf[diningDf["Dining_Hall"].str.contains(r'mosher-jordan') == True] #was going to sift thru dhall but didnt have time
    vegan_ops = diningDf[diningDf["Menu_Item"].str.contains(r'Vegan') == True] #will it get uppercase vegan...
    vegan_ops.drop_duplicates(subset=['Menu_Item'], inplace = True)
    vegan_ops = vegan_ops.nlargest(15, 'Calories')
    #result = vegan_ops.to_html()
    return(vegan_ops)





print(vegan_options(diningDf, dining_hall))

def high_protein(diningDf, dining_hall):
    sorted_byprot = diningDf[diningDf["Dining_Hall"].str.contains(r'mosher-jordan') == True] 
    sorted_byprot = diningDf.nlargest(35, 'Protein')
    sorted_byprot.drop_duplicates(subset=['Menu_Item'], inplace = True)
    sorted_byprot = sorted_byprot.nlargest(15, 'Protein')
    return (sorted_byprot)


def lowest_sugars(diningDf, dining_hall):
    sorted_bysug = diningDf.nsmallest(35, 'Sugars')
    sorted_bysug.drop_duplicates(subset=['Menu_Item'], inplace = True)
    sorted_bysug = sorted_bysug.nlargest(15, 'Sugars')
    return (sorted_bysug)

print(high_protein(diningDf, dining_hall))

print(lowest_sugars(diningDf, dining_hall))

