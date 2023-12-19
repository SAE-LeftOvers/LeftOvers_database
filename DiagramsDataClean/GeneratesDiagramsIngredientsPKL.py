import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Utils import GetIngrDataframe
from Utils import MakePie


print("Generating data on ingr.pkl...")

raw_ingredients_df = GetIngrDataframe()
raw_ingredients_df_drop_duplicates = raw_ingredients_df.drop_duplicates()

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# &&&&&     Replaced Column     &&&&&
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

data_replaced_column = {"valid_type": 0, 
                        "invalid_type": 0, 
                        "null_empty": 0,
                        "multiple_entry": 0,
                        "original_entry": 0,
                        "total": 0,
                        "data": []}
    
for row in raw_ingredients_df.itertuples():
    if (row.replaced == None):
        data_replaced_column["null_empty"] += 1
    elif (type(row.replaced) is str):
        data_replaced_column["valid_type"] += 1
        if (len(row.replaced) == 0):
            data_replaced_column["null_empty"] += 1
        else:
            if (row.replaced not in data_replaced_column["data"]):
                data_replaced_column["data"].append(row.replaced)
                data_replaced_column["original_entry"] += 1
            else:
                data_replaced_column["multiple_entry"] += 1
    else:
        data_replaced_column["invalid_type"] += 1
    data_replaced_column["total"] += 1
tmp = data_replaced_column.pop("data")
print("Replaced column (before cleaning):", data_replaced_column)

data_to_show = [data_replaced_column["multiple_entry"], 
                data_replaced_column["original_entry"],
                data_replaced_column["null_empty"]]
labels = [
    "Valeurs dupliquées",
    "Valeurs unique",
    "Valeurs nulle ou vide"
]

MakePie(data_to_show,
        labels,
        "Statistiques sur la colonne 'replaced'",
        "StatsIngrReplacedBeforeCleaning.png")


data_replaced_column_drop_duplicates = {"valid_type": 0, 
                                        "invalid_type": 0, 
                                        "null_empty": 0,
                                        "multiple_entry": 0,
                                        "original_entry": 0,
                                        "total": 0,
                                        "data": []}
    
for row in raw_ingredients_df_drop_duplicates.itertuples():
    if (row.replaced == None):
        data_replaced_column_drop_duplicates["null_empty"] += 1
    elif (type(row.replaced) is str):
        data_replaced_column_drop_duplicates["valid_type"] += 1
        if (len(row.replaced) == 0):
            data_replaced_column_drop_duplicates["null_empty"] += 1
        else:
            if (row.replaced not in data_replaced_column_drop_duplicates["data"]):
                data_replaced_column_drop_duplicates["data"].append(row.replaced)
                data_replaced_column_drop_duplicates["original_entry"] += 1
            else:
                data_replaced_column_drop_duplicates["multiple_entry"] += 1
    else:
        data_replaced_column_drop_duplicates["invalid_type"] += 1
    data_replaced_column_drop_duplicates["total"] += 1
    
tmp = data_replaced_column_drop_duplicates.pop("data")
print("Replaced column (after cleaning):", data_replaced_column_drop_duplicates)

data_to_show = [data_replaced_column_drop_duplicates["multiple_entry"], 
                data_replaced_column_drop_duplicates["original_entry"]]
labels = ["Valeurs dupliquées",
            "Valeurs unique"]
MakePie(data_to_show, 
        labels, 
        "Statistiques sur la colonne 'replaced' après suppression des lignes redondantes", 
        "StatsIngrReplacedAfterCleaning.png")


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# &&&&&        Id Column        &&&&&
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
data_id_column = {"valid_type": 0, 
                  "invalid_type": 0, 
                  "null_empty": 0,
                  "multiple_entry": 0,
                  "original_entry": 0,
                  "total": 0,
                  "data": []}
    
for row in raw_ingredients_df.itertuples():
    if (row.id == None):
        data_id_column["null"] += 1
    elif (type(row.id) is int):
        data_id_column["valid_type"] += 1
        if (row.id not in data_id_column["data"]):
            data_id_column["data"].append(row.id)
            data_id_column["original_entry"] += 1
        else:
            data_id_column["multiple_entry"] += 1
    else:
        data_id_column["invalid_type"] += 1
    data_id_column["total"] += 1
tmp = data_id_column.pop("data")
print("Id column (before cleaning):", data_id_column)

data_to_show = [data_id_column["multiple_entry"], 
                data_id_column["original_entry"],
                data_id_column["null_empty"]]
labels = ["Valeurs dupliquées",
            "Valeurs unique",
            "Valeurs nulles ou vide"]
MakePie(data_to_show,
        labels,
        "Statistiques sur la colonne 'id'",
        "StatsIngrIdBeforeCleaning.png")

data_id_column_drop_duplicates = {"valid_type": 0, 
                                        "invalid_type": 0, 
                                        "null_empty": 0,
                                        "multiple_entry": 0,
                                        "original_entry": 0,
                                        "total": 0,
                                        "data": []}
    
for row in raw_ingredients_df_drop_duplicates.itertuples():
    if (row.id == None):
        data_id_column_drop_duplicates["null_empty"] += 1
    elif (type(row.id) is int):
        data_id_column_drop_duplicates["valid_type"] += 1
        if (row.id not in data_id_column_drop_duplicates["data"]):
            data_id_column_drop_duplicates["data"].append(row.id)
            data_id_column_drop_duplicates["original_entry"] += 1
        else:
            data_id_column_drop_duplicates["multiple_entry"] += 1
    else:
        data_id_column_drop_duplicates["invalid_type"] += 1
    data_id_column_drop_duplicates["total"] += 1
    
tmp = data_id_column_drop_duplicates.pop("data")
print("Id column (after cleaning):", data_id_column_drop_duplicates)

data_to_show = [data_id_column_drop_duplicates["multiple_entry"], 
                data_id_column_drop_duplicates["original_entry"]]
labels = ["Valeurs dupliquées",
            "Valeurs unique"]
MakePie(data_to_show,
        labels,
        "Statistiques sur la colonne 'id' après suppression des lignes redondantes",
        "StatsIngrIdAfterCleaning.png")



print("ingr.pkl data generated !")