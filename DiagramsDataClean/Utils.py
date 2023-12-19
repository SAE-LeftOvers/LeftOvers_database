import pandas as pd
import pickle as pkl
import matplotlib.pyplot as plt

def GetIngrDataframe():
    raw_ingredients_df = None

    with open('../input/ingr_map.pkl', 'rb') as f:
        raw_ingredients_df = pkl.load(f)
    
    if raw_ingredients_df.empty:
        return raw_ingredients_df
    
    raw_ingredients_df.drop('raw_ingr', axis=1, inplace=True)
    raw_ingredients_df.drop('raw_words', axis=1, inplace=True)
    raw_ingredients_df.drop('processed', axis=1, inplace=True)
    raw_ingredients_df.drop('len_proc', axis=1, inplace=True)
    raw_ingredients_df.drop('count', axis=1, inplace=True)

    return raw_ingredients_df

def GetRawRecipesCsv():
    raw_recipes_data = pd.read_csv(r'../input/RAW_recipes.csv')
    raw_recipes_df = pd.DataFrame(raw_recipes_data)
    return raw_recipes_df

def MakePie(values, labels, fig_title, fich_title):
    plt.clf()
    plt.pie(values, labels=labels, autopct='%1.0f%%')
    plt.title(fig_title)
    plt.savefig("./output/"+fich_title)

def MakeBar(values, labels, fig_title, fich_title):
    plt.clf()
    fig, ax = plt.subplots()

    i = 0
    for value in values:
        labels[i] = labels[i] + "\n" + str(value)
        i += 1
    ax.bar(labels, values)

    ax.set_ylabel('Nombre')
    ax.set_title(fig_title)

    plt.savefig("./output/"+fich_title)

def GetPPRecipesCsv():
    pp_recipes_data = pd.read_csv(r'../input/PP_recipes.csv')
    pp_recipes_df = pd.DataFrame(pp_recipes_data)
    pp_recipes_df.drop('i', axis=1, inplace=True)
    pp_recipes_df.drop('calorie_level', axis=1, inplace=True)
    pp_recipes_df.drop('name_tokens', axis=1, inplace=True)
    pp_recipes_df.drop('techniques', axis=1, inplace=True)
    pp_recipes_df.drop('ingredient_tokens', axis=1, inplace=True)
    pp_recipes_df.drop('steps_tokens', axis=1, inplace=True)
    return pp_recipes_df