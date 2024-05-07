from bs4 import BeautifulSoup
import os
import pandas as pd

# ---- FROM UTILS ---- #

def getStartDict() -> dict:
    nutritionDict = {
    "Dining_Hall": [],
    "Course": [],
    "Menu_Item": [],
    "Serving_Size": [],
    "Calories": [],
    "Total_Fat": [],
    "Saturated_Fat": [],
    "Trans_Fat": [],
    "Cholesterol": [],
    "Sodium": [],
    "Total_Carbohydrate": [],
    "Dietary_Fiber": [],
    "Sugars": [],
    "Protein": [],
    }
    return nutritionDict

def getDHalls() -> list:
    dHalls = ["South Quad", "North Quad", "East Quad", "Bursley", "Mosher Jordan", "Twigs at Oxford", "Markley"]
    return dHalls

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

# ---- FROM SCRAPE.PY ---- #

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

# ---- FROM FILTERING.PY ---- #

def vegan_options(diningDf, dining_hall):
    #find a way to sift by dhall and only return items in that dhall
    vegan_ops = diningDf[diningDf["Dining_Hall"].str.contains(r'mosher-jordan') == True] #was going to sift thru dhall but didnt have time
    vegan_ops = diningDf[diningDf["Menu_Item"].str.contains(r'Vegan') == True] #will it get uppercase vegan...
    vegan_ops.drop_duplicates(subset=['Menu_Item'], inplace = True)
    vegan_ops = vegan_ops.nlargest(15, 'Calories')
    #result = vegan_ops.to_html()
    return(vegan_ops)

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

# ---- ADDITIONAL FILTER FUNCTIONS ----#
#TODO: make dframe into class poss
def getTopItems(df: pd.DataFrame, hall: str, meal: int, count: int, filter: str) -> pd.DataFrame:
        temp_df = df.copy()
        if hall != "Any":
            temp_df = temp_df[temp_df["Dining_Hall"] == makeURL(hall)]
        if meal != "Any":
            temp_df = temp_df[temp_df["Course"] == meal]
    
        if filter == "Protein":
            return temp_df.nlargest(count, filter)
        
        return temp_df.nsmallest(count, filter)
