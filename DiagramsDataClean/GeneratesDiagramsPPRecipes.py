import numpy as np
import pandas as pd
import ast
import matplotlib.pyplot as plt
from Utils import GetPPRecipesCsv
from Utils import MakePie
from Utils import MakeBar


print("Generating data on PP_recipes.csv...")

pp_recipes_df = GetPPRecipesCsv()


# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
# &&&&&&&       Before cleaning dataset       &&&&&&&
# &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
dico_data = {}

# ----- id column
dico_data["id"] = {"total": 0,
                    "valid_datatype": 0,
                    "invalid_datatype": 0,
                    "null_or_empty": 0,
                    "data": [],
                    "original": 0,
                    "duplicated": 0}
for row in pp_recipes_df.itertuples():
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
Values = [
    dico_data["id"]["valid_datatype"],
    dico_data["id"]["invalid_datatype"],
    dico_data["id"]["null_or_empty"],
    dico_data["id"]["duplicated"]
]
Labels = [
    "Type valide",
    "Type invalide",
    "Vide ou Nulle",
    "Dupliquées"
]
MakeBar(Values, Labels, "Etude sur les données de la colonne 'id'", "StatsLinkIdBeforeCleaning.png")

# ----- ingredient_ids column
dico_data["ingredient_ids"] = {}
dico_data["ingredient_ids"]["no_ingr"] = 0
dico_data["ingredient_ids"]["null"] = 0
dico_data["ingredient_ids"]["total"] = 0
dico_data["ingredient_ids"]["line_with_duplicated_values"] = 0

dico_data_every_lines = {}

for row in pp_recipes_df.itertuples():
    dico_data["ingredient_ids"]["total"] += 1
    dico_data_every_lines[row.id] = {"valid_datatype": 0,
                                            "invalid_datatype": 0,
                                            "null_or_empty": 0,
                                            "data": [],
                                            "original": 0,
                                            "duplicated": 0}
    if (ast.literal_eval(row.ingredient_ids) == None):
        dico_data["ingredient_ids"]["null"] += 1
    elif (len(ast.literal_eval(row.ingredient_ids)) == 0):
        dico_data["ingredient_ids"]["no_ingr"] += 1
    else:
        for id_ingr in ast.literal_eval(row.ingredient_ids):
            if (id_ingr == None):
                dico_data_every_lines[row.id]["null_or_empty"] += 1
            elif (type(id_ingr) is int):
                dico_data_every_lines[row.id]["valid_datatype"] += 1
                if (id_ingr not in dico_data_every_lines[row.id]["data"]):
                    dico_data_every_lines[row.id]["data"].append(id_ingr)
                    dico_data_every_lines[row.id]["original"] += 1
                else:
                    dico_data_every_lines[row.id]["duplicated"] += 1
            else:
                dico_data_every_lines[row.id]["invalid_datatype"] += 1
        if dico_data_every_lines[row.id]["duplicated"] > 0:
            dico_data["ingredient_ids"]["line_with_duplicated_values"] += 1
Values = [
    dico_data["ingredient_ids"]["total"] - dico_data["ingredient_ids"]["line_with_duplicated_values"],
    dico_data["ingredient_ids"]["line_with_duplicated_values"]
]
Labels = [
    "Sans valeurs dupliquées",
    "Avec valeurs dupliquées"
]
MakePie(Values,
        Labels, 
        "Etude sur les données de la colonne 'ingredient_ids'", 
        "StatsLinkIngredientIdsBeforeCleaning.png")


print("Data on PP_recipes.csv generated !")