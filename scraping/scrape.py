from utils.soup import getSoup
from utils.funcs import *


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
        #TODO: check for formatting inconsistencies

    return label, value



def fillDictRow(menu_dict: dict, dining_hall: str, course: str, menu_item: str, nutrition_input: list) -> dict:
    '''
    Fills menu dictionary with corresponding row of values
    '''

    # create empty dictionary of single entries
    temp = dict()
    for key in menu_dict:
        temp[key] = None

    # add dining hall
    temp['Dining_Hall'] = dining_hall

    # add course
    temp['Course'] = course

    # add menu item name
    temp['Menu_Item'] = menu_item

    # add serving size
    servingSize = nutrition_input[0].split('(')
    servingSize = servingSize[1].split('g')[0]
    temp['Serving_Size'] = int(servingSize)

    # add calories
    calories = nutrition_input[2].split(' ')[1]
    temp['Calories'] = int(calories)

    # add facts from rows idx: 6-12
    for i in range(4, 13):
        labe, val = parseFact(nutrition_input[i])
        if labe in temp:
            temp[labe] = int(val)

    return temp



def getCourseItems(dining_hall: str, course: str, menu_dict: dict, courseHTML):
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

        if nutrDiv is not None:
            nutrRows = nutrDiv.find_all("tr")
            nutrRows = [x.find("td").text.strip() for x in nutrRows if x.find("td") is not None]

            # add item to dictionary
            tempDict = fillDictRow(menu_dict, dining_hall, course, itemName, nutrRows)
            for key in tempDict:
                menu_dict[key].append(tempDict[key])   



def getDhallItems(path: str, dining_hall_file: str, menu_dict: dict):
    dining_hall_str = dining_hall_file.split('.')[0]
    soup = getSoup(path, dining_hall_file)

    menuDiv = soup.find("div", { "id": "mdining-items"})
    meals = menuDiv.find_all("h3")
    meals = [x.text.strip() for x in meals]

    courses = menuDiv.find_all("ul", { "class": "courses_wrapper"})

    # loops through valid course_wrapper html
    for i in range(len(courses)):
        getCourseItems(dining_hall_str, meals[i], menu_dict, courses[i])


def makeURL(hall):
    return hall.lower().replace(" ", "-")

