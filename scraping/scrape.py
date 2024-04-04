import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scraping.soup import getSoup


def parseFact(fact_label: str):
    '''
    Takes nutrion row text and outputs reformatted label and quantity
    '''

    splits = fact_label.split(' ')
    labelSplit = splits[:-1]
    valueSplit = splits[-1]

    label = '_'.join(labelSplit)
    if 'm' in valueSplit:
        value = valueSplit.split('m')[0]
    else:
        value = valueSplit.split('g')[0]

    return label, value



def fillMenuDict(menu_dict: dict, dining_hall: str, course: str, menu_item: str, nutrition_input: list): # ** DICTIONARY PASSED BY REF
    '''
    Fills menu dictionary with corresponding row of values
    '''

    #TODO: might have to change how input is parsed through (could be more nutrition rows, NaN data, etc.)
    #TODO: check for formatting inconsistencies (insert null values if needed)

    # add dining hall
    menu_dict['Dining_Hall'].append(dining_hall)

    # add course
    menu_dict['Course'].append(course)

    # add menu item name
    menu_dict['Menu_Item'].append(menu_item)

    # add serving size
    servingSize = nutrition_input[0].split('(')
    servingSize = servingSize[1].split('g')[0]
    menu_dict['Serving_Size'].append(servingSize)

    # add calories
    calories = nutrition_input[2].split(' ')[1]
    menu_dict['Calories'].append(calories)

    # add facts from rows idx: 6-12
    for i in range(4, 13):
        labe, val = parseFact(nutrition_input[i])
        menu_dict[labe].append(val)



def getMenuItems(dining_hall: str, course: str, menu_dict: dict, courseHTML):
    '''
    Fills menu dictionary with all menu items from a singular course
    '''
    
    # list of all item sections (len = num of kitchens)
    itemClass = courseHTML.find_all("ul", { "class" : "items"}) 

    # list of all menu items (contains -- class: item-name, class: nutrition)
    menuItemDivs = [] 
    for kitchen in itemClass:
        temp = kitchen.find_all("li", recursive = False)
        menuItemDivs += temp

    # menu item loop
    for itemDiv in menuItemDivs:

        # get menu-item names
        itemName = itemDiv.find("div", {"class": "item-name"}).text.strip() 

        # get nutritional value list
        nutrDiv = itemDiv.find("table", { "class": "nutrition-facts"})
        nutrRows = nutrDiv.find_all("tr")
        nutrRows = [x.find("td").text.strip() for x in nutrRows if x.find("td") is not None]

        # add item to dictionary
        fillMenuDict(menu_dict, dining_hall, course, itemName, nutrRows)        
    

