import numpy as np
import pandas as pd
import ast
import matplotlib.pyplot as plt
from Utils import GetRawRecipesCsv
from Utils import MakePie
from Utils import MakeBar


print("Generating data on RAW_recipes.csv...")

raw_recipes_df = GetRawRecipesCsv()

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# &&&&&&&       Before cleaning dataset       &&&&&&&
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
column_to_scan = ["id", "name", "description", "minutes", "steps"]
dico_data = {}
for name_row in column_to_scan:
    dico_data[name_row] = {"total": 0,
                            "valid_datatype": 0,
                            "invalid_datatype": 0,
                            "null_or_empty": 0}
# ----- id column
dico_data["id"]["data"] = []
dico_data["id"]["original"] = 0
dico_data["id"]["duplicated"] = 0
for row in raw_recipes_df.itertuples():
    dico_data["id"]["total"] += 1
    if (row.id == None):
        dico_data["id"]["null_or_empty"] += 1
    elif (type(row.id) is int):
        dico_data["id"]["valid_datatype"] += 1
        if (row.id == 0):
            dico_data["id"]["null_or_empty"] += 1
        elif (row.id not in dico_data["id"]["data"]):
            dico_data["id"]["data"].append(row.id)
            dico_data["id"]["original"] += 1
        else:
            dico_data["id"]["duplicated"] += 1
    else:
        dico_data["id"]["invalid_datatype"] += 1
dico_data["id"].pop("data")
print("Id column (before cleaning):", dico_data["id"])

# ----- name column
for row in raw_recipes_df.itertuples():
    dico_data["name"]["total"] += 1
    if (row.name == None):
        dico_data["name"]["null_or_empty"] += 1
    elif (type(row.name) is str):
        dico_data["name"]["valid_datatype"] += 1
        if (len(row.name) == 0):
            dico_data["name"]["null_or_empty"] += 1
    else:
        dico_data["name"]["invalid_datatype"] += 1
print("Name column (before cleaning):", dico_data["name"])

values = [dico_data["name"]["valid_datatype"],
            dico_data["name"]["invalid_datatype"]]
labels = ["Type valide", "Type non valide"]
MakePie(values, labels, "Colonne 'name', enquête de validité", "StatsRecipeNameBeforeCleaning.png")

# ----- description column
for row in raw_recipes_df.itertuples():
    dico_data["description"]["total"] += 1
    if (row.description == None):
        dico_data["description"]["null_or_empty"] += 1
    elif (type(row.description) is str):
        dico_data["description"]["valid_datatype"] += 1
        if (len(row.description) == 0):
            dico_data["description"]["null_or_empty"] += 1
    else:
        dico_data["description"]["invalid_datatype"] += 1
print("Description column (before cleaning):", dico_data["description"])

values = [dico_data["description"]["valid_datatype"],
            dico_data["description"]["invalid_datatype"]]
labels = ["Type valide", "Type non valide"]
MakePie(values, labels, "Colonne 'description', enquête de validité", "StatsRecipeDescriptionBeforeCleaning.png")

# ----- time column
dico_data["minutes"]["zero"] = 0
for row in raw_recipes_df.itertuples():
    dico_data["minutes"]["total"] += 1
    if (row.minutes == None):
        dico_data["minutes"]["null_or_empty"] += 1
    elif (type(row.minutes) is int):
        dico_data["minutes"]["valid_datatype"] += 1
        if (row.minutes == 0):
            dico_data["minutes"]["zero"] += 1
    else:
        dico_data["minutes"]["invalid_datatype"] += 1
print("Minutes column (before cleaning):", dico_data["minutes"])

values = [dico_data["minutes"]["valid_datatype"],
            dico_data["minutes"]["invalid_datatype"],
            dico_data["minutes"]["zero"]]
labels = ["Type valide", "Type non valide", "Valeur égales à zéro"]
MakeBar(values, labels, "Colonne 'minutes', enquête de validité", "StatsRecipeTimeBeforeCleaning.png")

# ----- steps column
dico_data["steps"]["no_steps"] = 0
dico_data["steps"]["steps"] = 0
for row in raw_recipes_df.itertuples():
    if (ast.literal_eval(row.steps) == None or len(ast.literal_eval(row.steps)) == 0):
        dico_data["steps"]["no_steps"] += 1
    else:
        dico_data["steps"]["steps"] += 1
        for step in ast.literal_eval(row.steps):
            dico_data["steps"]["total"] += 1
            if (row.steps == None):
                dico_data["steps"]["null_or_empty"] += 1
            elif (type(row.steps) is str):
                dico_data["steps"]["valid_datatype"] += 1
                if (len(row.steps) == 0):
                    dico_data["steps"]["null_or_empty"] += 1
            else:
                dico_data["steps"]["invalid_datatype"] += 1
print("Steps column (before cleaning):", dico_data["steps"])

values = [dico_data["steps"]["valid_datatype"],
            dico_data["steps"]["invalid_datatype"]]
labels = ["Type valide", "Type non valide"]
MakePie(values, labels, "Colonne 'steps', enquête de validité", "StatsRecipeStepsTypeBeforeCleaning.png")

values = [dico_data["steps"]["steps"],
            dico_data["steps"]["no_steps"]]
labels = ["Recettes avec des étapes", " Recettes sans étapes"]
MakeBar(values, labels, "Colonne 'steps', enquête sur la présence d'étapes", "StatsRecipeStepsExistenceBeforeCleaning.png")

# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# &&&&&&&        After cleaning dataset       &&&&&&&
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

print("Data on RAW_recipes.csv generated !")
