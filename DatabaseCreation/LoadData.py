import pandas as pd
import pickle as pkl
import psycopg2 as psy
from psycopg2 import sql
import ast
from tqdm import tqdm

from CreateDatatables import InitializeDatabaseConnection, CloseDatabaseConnection
from Utils import CreateDictionnaryOutOfString, MergeDictionnary

def DeleteDouble(input):
    output=[]
    [output.append(element) for element in input if element not in output]
    return output

def LoadIngredientsTable():
    co = None
    raw_ingredients_df = None
    with open('../input/ingr_map.pkl', 'rb') as f:
        raw_ingredients_df = pkl.load(f)
    if raw_ingredients_df.empty:
        return
    raw_ingredients_df.drop('raw_ingr', axis=1, inplace=True)
    raw_ingredients_df.drop('raw_words', axis=1, inplace=True)
    raw_ingredients_df.drop('processed', axis=1, inplace=True)
    raw_ingredients_df.drop('len_proc', axis=1, inplace=True)
    raw_ingredients_df.drop('count', axis=1, inplace=True)
    raw_ingredients_df.drop_duplicates(inplace=True)
    
    try:
        co = InitializeDatabaseConnection()
        curs = co.cursor()

        print("Loading ingredients in Ingredients table...")
        with tqdm(total=raw_ingredients_df.shape[0]) as pbar:
            for row in raw_ingredients_df.itertuples():
                curs.execute('''INSERT INTO Ingredients VALUES (%s, %s);''',
                                        (row.id, row.replaced))
                pbar.update(1)
        
        co.commit()
        print("Ingredients loaded in Ingredients table !")
    
    except(Exception, psy.DatabaseError) as error:
        print(error)
        exit(error)
    
    finally:
        CloseDatabaseConnection(co)  
    

def LoadRecipesTable(valid_recipe_ids):
    co = None
    raw_recipes_data = pd.read_csv(r'../input/RAW_recipes.csv')
    raw_recipes_df = pd.DataFrame(raw_recipes_data)
    raw_recipes_df = raw_recipes_df.drop_duplicates()

    try:
        co = InitializeDatabaseConnection()
        curs = co.cursor()
        
        print("Loading recipes in Recipes table...")

        with tqdm(total=raw_recipes_df.shape[0]) as pbar:
            for row in raw_recipes_df.itertuples():
                recipe_id = row.id
                if (recipe_id not in valid_recipe_ids):
                    pbar.update(1)
                    continue
                description = str(row.description)
                if len(description) > 1024 :
                    description = description[:1024]
                description_dico = CreateDictionnaryOutOfString(description)
                curs.execute('''INSERT INTO Recipes (id, name, description, time, description_dico) VALUES (%s, %s, %s, %s, %s);''',
                                        (recipe_id, row.name, description, row.minutes, str(description_dico)))
                pbar.update(1)
            
        co.commit()
        print("Recipes loaded in Recipes table !")

    except(Exception, psy.DatabaseError) as error:
        print(error)
        exit(error)

    finally:
        CloseDatabaseConnection(co)

def CreateCommentsDictionnaryAndRating(valid_recipe_ids):
    output_dico = {}
    raw_interactions_data = pd.read_csv(r'../input/RAW_interactions.csv')
    raw_interactions_df = pd.DataFrame(raw_interactions_data)
    raw_interactions_df = raw_interactions_df.drop_duplicates()

    print("Creating comments word dictionnary out of interactions...")

    with tqdm(total=raw_interactions_df.shape[0]) as pbar:
        for row in raw_interactions_df.itertuples() :
            key = int(row.recipe_id)
            if (key not in valid_recipe_ids):
                pbar.update(1)
                continue

            if (output_dico.get(key) == None) :
                output_dico[key] = {
                    'comments_dicos': {},
                    'rating': []
                }
            current_dico_comment = CreateDictionnaryOutOfString(str(row.review))
            output_dico[key]['comments_dicos'] = MergeDictionnary(output_dico[key]['comments_dicos'], current_dico_comment)
            output_dico[key]['rating'].append(int(row.rating))

            pbar.update(1)
    
    print("Dictionnary created !")
    
    return output_dico


def LoadCommentsDictionnaryAndRating(valid_recipe_ids):
    comments_ratings_dictionnary = CreateCommentsDictionnaryAndRating(valid_recipe_ids)
    
    try:
        co = InitializeDatabaseConnection()
        curs = co.cursor()
        
        print("Loading comment dictionnary and ratings in Recipes table...")

        with tqdm(total=len(comments_ratings_dictionnary.keys())) as pbar:
            for key in comments_ratings_dictionnary:
                recipe_id = key
                dico_str = str(comments_ratings_dictionnary[key]['comments_dicos'])
                rating = str(comments_ratings_dictionnary[key]['rating'])

                curs.execute('''UPDATE Recipes SET comments_dico=%s, rating=%s WHERE id=%s;''',
                                        (dico_str, rating, key))
                
                pbar.update(1)
            
        co.commit()
        print("Ratings and comments dictionnary loaded in Recipes table!")

    except(Exception, psy.DatabaseError) as error:
        print(error)
        exit(error)

    finally:
        CloseDatabaseConnection(co)


def LoadComposedTable(valid_recipe_ids):
    co = None
    pp_recipes_data = pd.read_csv(r'../input/PP_recipes.csv')
    pp_recipes_df = pd.DataFrame(pp_recipes_data)
    pp_recipes_df.drop('i', axis=1, inplace=True)
    pp_recipes_df.drop('calorie_level', axis=1, inplace=True)
    pp_recipes_df.drop('name_tokens', axis=1, inplace=True)
    pp_recipes_df.drop('techniques', axis=1, inplace=True)
    pp_recipes_df.drop('ingredient_tokens', axis=1, inplace=True)
    pp_recipes_df.drop('steps_tokens', axis=1, inplace=True)
    pp_recipes_df.drop_duplicates(inplace=True)
    
    try:
        co = InitializeDatabaseConnection()
        curs = co.cursor()

        print("Loading links ingredients-recipes...")
        with tqdm(total=pp_recipes_df.shape[0]) as pbar:
            for row in pp_recipes_df.itertuples():
                recipe_id = row.id
                if (recipe_id not in valid_recipe_ids):
                    pbar.update(1)
                    continue
                ingredient_ids = DeleteDouble(ast.literal_eval(row.ingredient_ids))
                for ingr_id in ingredient_ids:
                    curs.execute('''INSERT INTO Composed VALUES (%s, %s);''',
                                            (recipe_id, ingr_id))
                pbar.update(1)
        
        co.commit()
        print("Links ingredients-recipe loaded !")
    
    except(Exception, psy.DatabaseError) as error:
        print(error)
        exit(error)
    
    finally:
        CloseDatabaseConnection(co)


def LoadStepsTable(valid_recipe_ids):
    co = None
    raw_recipes_data = pd.read_csv(r'../input/RAW_recipes.csv')
    raw_recipes_df = pd.DataFrame(raw_recipes_data)
    raw_recipes_df = raw_recipes_df.drop_duplicates()

    try:
        co = InitializeDatabaseConnection()
        curs = co.cursor()

        print("Loading Steps...")
        with tqdm(total=raw_recipes_df.shape[0]) as pbar:
            for row in raw_recipes_df.itertuples():
                recipe_id = row.id
                if (recipe_id not in valid_recipe_ids):
                    pbar.update(1)
                    continue
                raw_steps = ast.literal_eval(row.steps)
                step_order = 1
                for raw_step in raw_steps:
                    curs.execute('''INSERT INTO Steps VALUES (%s, %s, %s);''',
                                            (raw_step, recipe_id, step_order))
                    step_order += 1
                pbar.update(1)

        co.commit()
        print("Steps loaded !")

    except(Exception, psy.DatabaseError) as error:
        print(error)
        exit(error)
    
    finally:
        CloseDatabaseConnection(co)

def GetValidRecipeIds():
    output_recipe_ids = []

    pp_recipes_data = pd.read_csv(r'../input/PP_recipes.csv')
    pp_recipes_df = pd.DataFrame(pp_recipes_data)
    pp_recipes_df.drop('i', axis=1, inplace=True)
    pp_recipes_df.drop('calorie_level', axis=1, inplace=True)
    pp_recipes_df.drop('name_tokens', axis=1, inplace=True)
    pp_recipes_df.drop('techniques', axis=1, inplace=True)
    pp_recipes_df.drop('ingredient_tokens', axis=1, inplace=True)
    pp_recipes_df.drop('steps_tokens', axis=1, inplace=True)
    pp_recipes_df.drop_duplicates(inplace=True)

    print("Loading valid recipe ids...")
    with tqdm(total=pp_recipes_df.shape[0]) as pbar:
            for row in pp_recipes_df.itertuples():
                recipe_id = row.id
                if (recipe_id not in output_recipe_ids):
                    output_recipe_ids.append(recipe_id)
                pbar.update(1)

    print("Valid recipe ids loaded !")
    return output_recipe_ids


def LoadData():
    LoadIngredientsTable()
    valid_recipe_ids = GetValidRecipeIds()
    LoadRecipesTable(valid_recipe_ids)
    LoadCommentsDictionnaryAndRating(valid_recipe_ids)
    LoadComposedTable(valid_recipe_ids)
    LoadStepsTable(valid_recipe_ids)