import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Utils import GetPPRecipesCsv, GetRawRecipesCsv
from Utils import MakePie

pp_recipes_df = GetPPRecipesCsv()
raw_recipes_df = GetRawRecipesCsv()

pp_recipes_recipes_ids = []
for row in pp_recipes_df.itertuples():
    pp_recipes_recipes_ids.append(row.id)

raw_recipes_recipes_ids = []
for row in raw_recipes_df.itertuples():
    raw_recipes_recipes_ids.append(row.id)

dico = {'are_in_both': 0,
        'are_only_in_pp': 0,
        'are_only_in_raw': 0}

for id in pp_recipes_recipes_ids:
    if (id in raw_recipes_recipes_ids):
        dico['are_in_both'] += 1
    else:
        dico['are_only_in_pp'] += 1

for id in raw_recipes_recipes_ids:
    if (id not in pp_recipes_recipes_ids):
        dico['are_only_in_raw'] += 1

values = [dico['are_in_both'],
          dico['are_only_in_pp']+dico['are_only_in_raw']]
labels = ["Ids dans les 2 fichiers",
          "Ids seulement dans 1 fichier",]

MakePie(values, labels, "Etude sur la cohérence des ids de recette", "StatsIdsRecipesCoherence.png")