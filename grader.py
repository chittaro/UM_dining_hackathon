import pandas as pd

# Define cals/gram per macros
CALS_FAT = 9
CALS_CRB = 4
CALS_PRO = 4

def scoreMenu(df: pd.DataFrame, dh: str) -> dict:
    '''Adds a column of total scores to the dataframe and returns a sorted df for that dining hall.'''

    # Declare empty list and dict
    totals = []
    scores = []

    # Filter by dining hall
    filtered_df = df[df["Dining_Hall"] == dh]

    # Iterate through rows and calculate scores
    for index, row in filtered_df.iterrows():
        scrs = calcScores(row)
        totals.append(scrs["Total"])
        scrs["Menu_Item"] = row["Menu_Item"]
        scores.append(scrs)

    # Assign totals to a new column in the df
    filtered_df["Nutrition_Score"] = totals
    filtered_df = filtered_df.sort_values(by=["Nutrition_Score"], ascending = False)
    print(filtered_df)

    # Return dict
    return filtered_df
    
def calcScores(row: pd.Series) -> dict:
    '''Calculates each category score (and total) for item. Returns dictionary with categories as keys and scores as vals.'''

    # Calculate subscores
    sc_tf = 1 if row["Trans_Fat"] == 0 else 0
    sc_sf = 1 - (CALS_FAT * row["Saturated_Fat"] / row["Calories"])
    sc_sd = 1 - (row["Sodium"] / row["Calories"])
    sc_pr = CALS_PRO * row["Protein"] / row["Calories"]
    sc_cb = 1 if row["Total_Carbohydrate"] == 0 else row["Dietary_Fiber"] / row["Total_Carbohydrate"]

    # Sum
    total = sc_tf + sc_sf + sc_sd + sc_pr + sc_cb

    # Return dict
    scores = {"Calories": row["Calories"],
              "Trans Fat": sc_tf,
              "Sat. Fat": sc_sf,
              "Sodium": sc_sd,
              "Protein": sc_pr,
              "Fiber": sc_cb,
              "Total": total}
    
    return scores
