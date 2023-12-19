import pandas as pd
import psycopg2 as psy
from psycopg2 import sql
from DatabaseConnection import InitializeDatabaseConnection, CloseDatabaseConnection

def DeleteATable(co, curs, name):
    try:
        print("Deleting "+name+" table...")
        curs.execute(sql.SQL("DROP TABLE IF EXISTS {}").format(sql.Identifier(name)))
        co.commit()
        print("Table "+name+" deleted !")

    except(Exception, psy.DatabaseError) as error:
        print("Error during table "+name+" deletion !")
        exit(error)

def CleanDatabase():
    print("----- Cleaning database...")
    co = None

    try:
        co = InitializeDatabaseConnection()
        curs = co.cursor()
        
        DeleteATable(co, curs, 'composed')
        DeleteATable(co, curs, 'recipesteps')
        DeleteATable(co, curs, 'steps')
        DeleteATable(co, curs, 'recipes')
        DeleteATable(co, curs, 'ingredients')
        

    except(Exception, psy.DatabaseError) as error:
        print(error)
        exit(error)

    finally:
        CloseDatabaseConnection(co)

    print("----- Database cleaned !")

def CreateDatatables():
    print("----- Creating datatables...")
    co = None

    try:
        co = InitializeDatabaseConnection()
        curs = co.cursor()

        curs.execute('''
            CREATE TABLE Ingredients(
                id numeric PRIMARY KEY,
                name varchar(150) UNIQUE
            );''')
        curs.execute('''
            CREATE TABLE Recipes(
                id numeric PRIMARY KEY,
                name varchar(150),
                description varchar(1024),
                rating varchar,
                description_dico varchar(2048),
                comments_dico varchar,
                time numeric
            );''')
        curs.execute('''
            CREATE TABLE Composed(
                idRecipe numeric REFERENCES Recipes(id),
                idIngredient numeric REFERENCES Ingredients(id),
                PRIMARY KEY (idRecipe, idIngredient)
            );''')
        curs.execute('''
            CREATE TABLE Steps(
                action varchar(1024),
                idRecipe numeric REFERENCES Recipes(id),
                numStep numeric,
                PRIMARY KEY (idRecipe, numStep)
            );''')
        
        co.commit()

    except(Exception, psy.DatabaseError) as error:
        print(error)
        exit(error)

    finally:
        CloseDatabaseConnection(co)

    print("----- Datatables created !")
